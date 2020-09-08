import logging

from blockchainetl_common.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl_common.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter
from bandetl.enumeration.entity_type import EntityType
from bandetl.jobs.export_transactions_job import ExportTransactionsJob

from bandetl.streaming.item_id_calculator import ItemIdCalculator


class BandStreamerAdapter:
    def __init__(
            self,
            band_service,
            item_exporter=ConsoleItemExporter(),
            batch_size=100,
            max_workers=5,
            entity_types=tuple(EntityType.ALL_FOR_STREAMING)):
        self.band_service = band_service
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.entity_types = entity_types
        self.item_id_calculator = ItemIdCalculator()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        latest_block = self.band_service.get_latest_block()
        return int(latest_block['block']['header']['height'])

    def export_all(self, start_block, end_block):
        # Export blocks, actions and logs
        oracle_requests = []
        if self._should_export(EntityType.ORACLE_REQUEST):
            oracle_requests = self._export_blocks(start_block, end_block)

        logging.info('Exporting with ' + type(self.item_exporter).__name__)

        all_items = oracle_requests

        self.calculate_item_ids(all_items)

        self.item_exporter.export_items(all_items)

    def _export_blocks(self, start_block, end_block):
        item_exporter = InMemoryItemExporter(item_types=EntityType.ALL_FOR_STREAMING)
        job = ExportTransactionsJob(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            band_service=self.band_service,
            max_workers=self.max_workers,
            item_exporter=item_exporter,
        )
        job.run()
        oracle_requests = item_exporter.get_items(EntityType.ORACLE_REQUEST)
        return oracle_requests

    def _should_export(self, entity_type):
        # TODO
        return True

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()
