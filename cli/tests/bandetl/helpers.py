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

import os

from bandetl.rpc.band_rpc import BandRpc
from bandetl.rpc.tendermint_rpc import TendermintRpc
from tests.bandetl.mock_band_rpc import MockBandRpc
from tests.bandetl.mock_tendermint_rpc import MockTendermintRpc


def get_band_rpc(provider_type, read_resource_lambda=None):
    if provider_type == "mock":
        if read_resource_lambda is None:
            raise ValueError('read_resource_lambda must not be None for provider type {}'.format(provider_type))
        rpc = MockBandRpc(read_resource_lambda)

    elif provider_type == "online":
        env_variable_name = "BAND_PROVIDER_URI"
        provider_uri = os.environ.get(env_variable_name)
        if provider_uri is None or len(provider_uri) == 0:
            raise ValueError('{} is required environment variable'.format(env_variable_name))

        rpc = BandRpc(provider_uri)

    else:
        raise ValueError('Unknown provider_type ' + provider_type)

    return rpc


def get_tendermint_rpc(provider_type, read_resource_lambda=None):
    if provider_type == "mock":
        if read_resource_lambda is None:
            raise ValueError('read_resource_lambda must not be None for provider type {}'.format(provider_type))
        rpc = MockTendermintRpc(read_resource_lambda)

    elif provider_type == "online":
        env_variable_name = "TENDERMINT_PROVIDER_URI"
        provider_uri = os.environ.get(env_variable_name)
        if provider_uri is None or len(provider_uri) == 0:
            raise ValueError('{} is required environment variable'.format(env_variable_name))

        rpc = TendermintRpc(provider_uri)

    else:
        raise ValueError('Unknown provider_type ' + provider_type)

    return rpc
