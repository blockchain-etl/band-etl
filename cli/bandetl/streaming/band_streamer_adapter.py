import logging

from blockchainetl_common.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl_common.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter
from bandetl.enumeration.entity_type import EntityType
from bandetl.jobs.export_blocks_job import ExportBlocksJob

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
        blocks, transactions, messages, logs, block_events, oracle_requests = [], [], [], [], [], []
        if self._should_export(EntityType.BLOCK) or \
                self._should_export(EntityType.BLOCK_EVENT) or \
                self._should_export(EntityType.TRANSACTION) or \
                self._should_export(EntityType.LOG) or \
                self._should_export(EntityType.MESSAGE) or \
                self._should_export(EntityType.ORACLE_REQUEST):
            blocks, transactions, messages, logs, block_events, oracle_requests = self._export_blocks(start_block, end_block)

        logging.info('Exporting with ' + type(self.item_exporter).__name__)

        all_items = blocks + \
            transactions + \
            messages + \
            logs + \
            block_events + \
            oracle_requests

        self.calculate_item_ids(all_items)

        self.item_exporter.export_items(all_items)

    def _export_blocks(self, start_block, end_block):
        item_exporter = InMemoryItemExporter(item_types=EntityType.ALL_FOR_STREAMING)
        job = ExportBlocksJob(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            band_service=self.band_service,
            max_workers=self.max_workers,
            item_exporter=item_exporter,
            export_blocks=self._should_export(EntityType.BLOCK),
            export_logs=self._should_export(EntityType.LOG),
            export_block_events=self._should_export(EntityType.BLOCK_EVENT),
            export_oracle_requests=self._should_export(EntityType.ORACLE_REQUEST),
            export_messages=self._should_export(EntityType.MESSAGE),
            export_transactions=self._should_export(EntityType.TRANSACTION)
        )
        job.run()
        blocks = item_exporter.get_items(EntityType.BLOCK)
        transactions = item_exporter.get_items(EntityType.TRANSACTION)
        messages = item_exporter.get_items(EntityType.MESSAGE)
        logs = item_exporter.get_items(EntityType.LOG)
        block_events = item_exporter.get_items(EntityType.BLOCK_EVENT)
        oracle_requests = item_exporter.get_items(EntityType.ORACLE_REQUEST)
        return blocks, transactions, messages, logs, block_events, oracle_requests

    def _should_export(self, entity_type):
        if entity_type == EntityType.BLOCK \
                or entity_type == EntityType.BLOCK_EVENT \
                or entity_type == EntityType.LOG \
                or entity_type == EntityType.ORACLE_REQUEST \
                or entity_type == EntityType.MESSAGE \
                or entity_type == EntityType.TRANSACTION:
            return entity_type in self.entity_types

        raise ValueError('Unexpected entity type ' + entity_type)

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()
