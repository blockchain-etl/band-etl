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

import pytest

from bandetl.jobs.export_blocks_job import ExportBlocksJob
from bandetl.jobs.exporters.band_item_exporter import BandItemExporter
from bandetl.service.band_service import BandService
from tests.bandetl.helpers import get_band_rpc, get_tendermint_rpc
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

import tests.resources
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_blocks_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block, end_block, resource_group ,provider_type", [
    (53, 53, 'cosmos_sdk_msgmultisend', 'mock'),
    skip_if_slow_tests_disabled([53, 53, 'cosmos_sdk_msgmultisend', 'online']),
    (94, 94, 'oracle_add_reporter', 'mock'),
    skip_if_slow_tests_disabled([94, 94, 'oracle_add_reporter', 'online']),
    (29025, 29025, 'oracle_create_datasource', 'mock'),
    skip_if_slow_tests_disabled([29025, 29025, 'oracle_create_datasource', 'online']),
    (568661, 568661, 'oracle_report', 'mock'),
    skip_if_slow_tests_disabled([568661, 568661, 'oracle_report', 'online']),
    (571845, 571845, 'oracle_request', 'mock'),
    skip_if_slow_tests_disabled([571845, 571845, 'oracle_request', 'online']),
])
def test_export_blocks_job(tmpdir, start_block, end_block, resource_group, provider_type):
    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        band_service=BandService(
            get_band_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file)),
            get_tendermint_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file)),
        ),
        max_workers=5,
        item_exporter=BandItemExporter(str(tmpdir)),
    )
    job.run()

    all_files = ['blocks.json',
                 'logs.json',
                 'block_events.json',
                 'messages.json',
                 'transactions.json',
                 'oracle_requests.json']

    for file in all_files:
        print(read_file(str(tmpdir.join(file))))
        compare_lines_ignore_order(
            read_resource(resource_group, f'expected_{file}'), read_file(str(tmpdir.join(file)))
        )
