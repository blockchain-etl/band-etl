# MIT License
#
# Copyright (c) 2020 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob
from blockchainetl_common.utils import validate_range

from bandetl.utils.datetime_utils import truncate_timestamp_to_microseconds
from bandetl.utils.string_utils import json_dumps, to_int, base64_string_to_bytes


class ExportTransactionsJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            band_service,
            max_workers,
            item_exporter,
            batch_size=1):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.band_service = band_service

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        for block_number in block_number_batch:
            self._export_transactions(block_number)

    def _export_transactions(self, block_number):
        transactions = self.band_service.get_transactions(block_number)
        block = self.band_service.get_block(block_number)
        block_results = self.band_service.get_block_results(block_number)
        block_timestamp = block.get('block').get('header').get('time')

        block_timestamp_truncated = truncate_timestamp_to_microseconds(block_timestamp)

        # TODO: Refactor

        items = []

        items.append({
            'type': 'block',
            'block_hash': block['block_id']['hash'],
            'block_height': block_number,
            'block_timestamp': block_timestamp,
            'block_timestamp_truncated': block_timestamp_truncated,
            'proposer_address': block['block']['header']['proposer_address'],
            'last_commit_hash': block['block']['header']['last_commit_hash'],
            'data_hash': block['block']['header']['data_hash'],
            'validators_hash': block['block']['header']['validators_hash'],
            'next_validators_hash': block['block']['header']['next_validators_hash'],
            'consensus_hash': block['block']['header']['consensus_hash'],
            'app_hash': block['block']['header']['app_hash'],
            'last_results_hash': block['block']['header']['last_results_hash'],
            'evidence_hash': block['block']['header']['evidence_hash'],
            'signatures': block['block']['last_commit']['signatures'],
        })

        for tx in transactions.get('txs', []):
            items.append({
                'type': 'transaction',
                'transaction_type': tx.get('type'),
                'block_height': block_number,
                'block_timestamp': block_timestamp,
                'block_timestamp_truncated': block_timestamp_truncated,
                'gas_wanted': tx.get('gas_wanted'),
                'gas_used': tx.get('gas_used'),
                'raw_json': json_dumps(tx),
            })

            for log_index, log in enumerate(tx.get('logs', [])):
                items.append({
                    'type': 'log',
                    'block_height': block_number,
                    'block_timestamp': block_timestamp,
                    'block_timestamp_truncated': block_timestamp_truncated,
                    'txhash': tx.get('txhash'),
                    'log_index': log_index,
                    'msg_index': log.get('msg_index'),
                    'log': log.get('log'),
                    'events': log.get('events'),
                    'raw_json': json_dumps(log),
                })

            for msg in tx.get('tx', {}).get('value', {}).get('msg', []):
                message_type = msg.get('type')
                normalized_message_type = normalize_message_type(message_type)

                items.append({
                    'type': 'message',
                    'block_height': block_number,
                    'block_timestamp': block_timestamp,
                    'block_timestamp_truncated': block_timestamp_truncated,
                    'txhash': tx.get('txhash'),
                    'message_type': message_type,
                    'normalized_message_type': normalized_message_type,
                    normalized_message_type: msg.get('value'),
                    'raw_json': json_dumps(msg),
                })

        block_events = list(yield_block_events(block_results))
        for event_type, event in block_events:
            items.append({
                'type': 'block_event',
                'block_height': block_number,
                'block_timestamp': block_timestamp,
                'block_timestamp_truncated': block_timestamp_truncated,
                'event_type': event.get('type'),
                'block_event_type': event_type,
                'raw_json': json_dumps(event),
            })

        for event_type, event in block_events:
            if event_type == 'end' and event.get('type') == 'resolve':
                resolve_event = parse_resolve_event(event)
                if resolve_event.get('request_id') is not None:
                    oracle_request = self.band_service.get_oracle_request(resolve_event.get('request_id'))
                    oracle_request_result = oracle_request.get('result', {})
                    oracle_script = self.band_service.get_oracle_script(
                        oracle_request_result.get('request').get('oracle_script_id'))

                    mapped_oracle_request = map_oracle_request(oracle_request, oracle_script)
                    items.append({**mapped_oracle_request, **{
                        'type': 'oracle_request',
                        'block_height': block_number,
                        'block_timestamp': block_timestamp,
                        'block_timestamp_truncated': block_timestamp_truncated,
                        'raw_json': json_dumps(oracle_request),
                    }})

        for item in items:
            self.item_exporter.export_item(item)

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()


def normalize_message_type(message_type):
    return message_type.replace('-', '_').replace('/', '_')


def yield_block_events(block_results):
    result = block_results.get('result', {})
    begin_block_events = result.get('begin_block_events')
    if begin_block_events is not None:
        for event in begin_block_events:
            yield 'begin', event

    end_block_events = result.get('end_block_events')
    if end_block_events is not None:
        for event in end_block_events:
            yield 'end', event


def parse_resolve_event(event):
    attributes = event.get('attributes')
    resolve = {}
    if len(attributes) > 0:
        request_id_as_bytes = attributes[0].get('value')
        request_id = int(base64_string_to_bytes(request_id_as_bytes))
        resolve['request_id'] = request_id
    return resolve


def map_oracle_request(oracle_request_result, oracle_script):
    return {**oracle_request_result.get('result'), **{
        'oracle_script': oracle_script.get('result')
    }}
