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

from bandetl.mappers.block_event_mapper import map_block_events
from bandetl.mappers.block_mapper import map_block
from bandetl.mappers.log_mapper import map_logs
from bandetl.mappers.message_mapper import map_messages
from bandetl.mappers.oracle_request_mapper import map_oracle_requests
from bandetl.mappers.transaction_mapper import map_transaction
from bandetl.utils.string_utils import base64_string_to_bytes


class ExportBlocksJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            band_service,
            max_workers,
            item_exporter,
            batch_size=1,
            export_blocks=True,
            export_block_events=True,
            export_logs=True,
            export_messages=True,
            export_oracle_requests=True,
            export_transactions=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.band_service = band_service

        self.export_blocks = export_blocks
        self.export_block_events = export_block_events
        self.export_logs = export_logs
        self.export_messages = export_messages
        self.export_oracle_requests = export_oracle_requests
        self.export_transactions = export_transactions

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
            self._export_blocks(block_number)

    def _export_blocks(self, block_number):
        block = map_block(self.band_service.get_block(block_number))

        # TODO: Refactor

        items = []

        if self.export_blocks:
            items.append(block)

        if self.export_transactions:
            transactions = self.band_service.get_transactions(block_number)
            for tx in transactions.get('txs', []):
                items.append(map_transaction(block, tx))

                if self.export_logs:
                    items.extend(list(map_logs(block, tx)))

                if self.export_messages:
                    items.extend(list(map_messages(block, tx)))

        if self.export_block_events or self.export_oracle_requests:
            block_results = self.band_service.get_block_results(block_number)
            block_events = list(yield_block_events(block_results))

            if self.export_block_events:
                items.extend(list(map_block_events(block, block_events)))

            if self.export_oracle_requests:
                for event_type, event in block_events:
                    if event_type == 'end' and event.get('type') == 'resolve':
                        resolve_event = parse_resolve_event(event)
                        oracle_request_id = resolve_event.get('request_id')
                        if oracle_request_id is not None:
                            oracle_request = self.band_service.get_oracle_request(oracle_request_id)
                            oracle_request_result = oracle_request.get('result', {})
                            oracle_script = self.band_service.get_oracle_script(
                                oracle_request_result.get('request').get('oracle_script_id'))

                            items.append(map_oracle_requests(block, oracle_request_id, oracle_request, oracle_script))

        for item in items:
            self.item_exporter.export_item(item)

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()


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
