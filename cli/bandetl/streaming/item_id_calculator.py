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

import json
import logging


class ItemIdCalculator:

    def calculate(self, item):
        if item is None or not isinstance(item, dict):
            return None

        item_type = item.get('type')

        if item_type == 'oracle_request' and item.get('oracle_request_id') is not None:
            return concat(item_type, item.get('oracle_request_id'))
        elif item_type == 'block' and item.get('block_hash') is not None:
            return concat(item_type, item.get('block_hash'))
        elif item_type == 'transaction' and item.get('txhash') is not None:
            return concat(item_type, item.get('txhash'))
        elif item_type == 'message' and item.get('txhash') is not None and item.get('index') is not None:
            return concat(item_type, item.get('txhash'), item.get('index'))
        elif item_type == 'block_event' and item.get('block_height') is not None and item.get('index') is not None:
            return concat(item_type, item.get('block_height'), item.get('index'))
        elif item_type == 'log' and item.get('txhash') is not None and item.get('log_index') is not None:
            return concat(item_type, item.get('txhash'), item.get('log_index'))

        logging.warning('item_id for item {} is None'.format(json.dumps(item)))

        return None


def concat(*elements):
    return '_'.join([str(elem) for elem in elements])
