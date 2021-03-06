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

import json

from bandetl.service.band_service import BandService
from blockchainetl_common.graph.graph_operations import Point
import dateutil.parser

from bandetl.utils.string_utils import to_int


class BlockTimestampGraph(object):
    def __init__(self, band_rpc):
        self._band_service = BandService(band_rpc)

    def get_first_point(self):
        block = self._band_service.get_genesis_block()
        return block_to_point(block)

    def get_last_point(self):
        block = self._band_service.get_latest_block()
        return block_to_point(block)

    def get_point(self, block_number):
        block = self._band_service.get_block(block_number)
        return block_to_point(block)

    def get_points(self, block_numbers):
        blocks = self._band_service.get_blocks(block_numbers)
        return [block_to_point(block) for block in blocks]


def block_to_point(block):
    block_header = block.get('block', {}).get('header')
    if not block_header or not block_header.get('time'):
        raise ValueError('header or header.time is empty in block: ' + json.dumps(block))

    block_timestamp_utc = dateutil.parser.parse(block_header['time']).timestamp()
    return Point(to_int(block_header['height']), block_timestamp_utc)
