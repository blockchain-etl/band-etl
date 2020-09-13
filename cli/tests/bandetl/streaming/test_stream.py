# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
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

import os

import pytest
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

from bandetl.service.band_service import BandService
from bandetl.streaming.band_streamer_adapter import BandStreamerAdapter

import tests.resources
from bandetl.enumeration.entity_type import EntityType
from blockchainetl_common.jobs.exporters.composite_item_exporter import CompositeItemExporter
from blockchainetl_common.streaming.streamer import Streamer
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled
from tests.bandetl.helpers import get_band_rpc, get_tendermint_rpc

RESOURCE_GROUP = 'test_stream'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block, end_block, batch_size, resource_group, entity_types, provider_type", [
    (254191, 254191, 1, 'oracle_create_oracle_script', ['block', 'log', 'message', 'transaction', 'block_event'], 'mock'),
    (111280, 111280, 1, 'oracle_report', ['block', 'log', 'message', 'transaction', 'block_event', 'oracle_request'], 'mock'),
])
def test_stream(tmpdir, start_block, end_block, batch_size, resource_group, entity_types, provider_type):
    try:
        os.remove('last_synced_block.txt')
    except OSError:
        pass

    blocks_output_file = str(tmpdir.join('actual_blocks.json'))
    transactions_output_file = str(tmpdir.join('actual_transactions.json'))
    logs_output_file = str(tmpdir.join('actual_logs.json'))
    messages_output_file = str(tmpdir.join('actual_messages.json'))
    block_events_output_file = str(tmpdir.join('actual_block_events.json'))
    oracle_requests_output_file = str(tmpdir.join('actual_oracle_requests.json'))

    band_service = BandService(
        band_rpc=ThreadLocalProxy(
            lambda: get_band_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file))),
        tendermint_rpc=ThreadLocalProxy(
            lambda: get_tendermint_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file)))
    )

    streamer_adapter = BandStreamerAdapter(
        band_service=band_service,
        batch_size=batch_size,
        item_exporter=CompositeItemExporter(
            filename_mapping={
                'block': blocks_output_file,
                'transaction': transactions_output_file,
                'log': logs_output_file,
                'message': messages_output_file,
                'block_event': block_events_output_file,
                'oracle_request': oracle_requests_output_file,
            }
        ),
        entity_types=entity_types,
    )
    streamer = Streamer(
        blockchain_streamer_adapter=streamer_adapter,
        start_block=start_block,
        end_block=end_block,
        retry_errors=False
    )
    streamer.stream()

    if EntityType.BLOCK in entity_types:
        print('=====================')
        print(read_file(blocks_output_file))
        compare_lines_ignore_order(
            read_resource(resource_group, 'expected_blocks.json'), read_file(blocks_output_file)
        )

    if EntityType.LOG in entity_types:
        print('=====================')
        print(read_file(logs_output_file))
        compare_lines_ignore_order(
            read_resource(resource_group, 'expected_logs.json'), read_file(logs_output_file)
        )

    if EntityType.MESSAGE in entity_types:
        print('=====================')
        print(read_file(messages_output_file))
        compare_lines_ignore_order(
            read_resource(resource_group, 'expected_messages.json'), read_file(messages_output_file)
        )

    if EntityType.TRANSACTION in entity_types:
        print('=====================')
        print(read_file(transactions_output_file))
        compare_lines_ignore_order(
            read_resource(resource_group, 'expected_transactions.json'), read_file(transactions_output_file)
        )

    if EntityType.BLOCK_EVENT in entity_types:
        print('=====================')
        print(read_file(block_events_output_file))
        compare_lines_ignore_order(
            read_resource(resource_group, 'expected_block_events.json'), read_file(block_events_output_file)
        )

    if EntityType.ORACLE_REQUEST in entity_types:
        print('=====================')
        print(read_file(oracle_requests_output_file))
        compare_lines_ignore_order(
            read_resource(resource_group, 'expected_oracle_requests.json'), read_file(oracle_requests_output_file)
        )