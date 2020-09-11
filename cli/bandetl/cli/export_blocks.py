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

import click
from bandetl.jobs.export_blocks_job import ExportBlocksJob
from bandetl.jobs.exporters.band_item_exporter import BandItemExporter
from bandetl.rpc.band_rpc import BandRpc

from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

from bandetl.rpc.tendermint_rpc import TendermintRpc
from bandetl.service.band_service import BandService

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, show_default=True, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-p', '--provider-uri', default='https://poa-api-backup2.bandchain.org', show_default=True, type=str,
              help='The URI of the remote Band node.')
@click.option('-p', '--provider-uri-tendermint', default='http://poa-q2.d3n.xyz:26657', show_default=True, type=str,
              help='The URI of the Tendermint RPC.')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int, help='The maximum number of workers.')
@click.option('-o', '--output-dir', default=None, type=str, help='The output directory for block data.')
@click.option('-f', '--output-format', default='json', show_default=True, type=click.Choice(['json']),
              help='The output format.')
def export_blocks(start_block, end_block, provider_uri, provider_uri_tendermint, max_workers, output_dir, output_format):
    """Export blocks."""

    band_rpc = ThreadLocalProxy(lambda: BandRpc(provider_uri))
    tendermint_rpc = ThreadLocalProxy(lambda: TendermintRpc(provider_uri_tendermint))

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        band_service=BandService(band_rpc, tendermint_rpc),
        max_workers=max_workers,
        item_exporter=BandItemExporter(output_dir, output_format=output_format)
    )
    job.run()
