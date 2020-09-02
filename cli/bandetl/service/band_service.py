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


class BandService(object):
    def __init__(self, band_rpc, tendermint_rpc=None):
        self.band_rpc = band_rpc
        self.tendermint_rpc = tendermint_rpc

    def get_block(self, block_id):
        return self.band_rpc.get_block(block_id)

    def get_block_results(self, block_id):
        if self.tendermint_rpc is None:
            raise ValueError('tendermint_rpc was omitted when creating BandService. Cannot call get_block_results')
        return self.tendermint_rpc.get_block_results(block_id)

    def get_genesis_block(self):
        return self.get_block(1)

    def get_latest_block(self):
        return self.get_block('latest')

    def get_blocks(self, block_number_batch):
        if not block_number_batch:
            return []

        return [self.get_block(x) for x in block_number_batch]

    def get_transactions(self, block_number):
        return self.band_rpc.get_transactions(block_number)

    def get_oracle_request(self, request_id):
        return self.band_rpc.get_oracle_request(request_id)

    def get_oracle_script(self, oracle_script_id):
        return self.band_rpc.get_oracle_script(oracle_script_id)