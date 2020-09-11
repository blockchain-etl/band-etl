from bandetl.utils.string_utils import json_dumps


def map_transaction(block, tx):
    return {
        'type': 'transaction',
        'transaction_type': tx.get('type'),
        'block_height': block.get('block_height'),
        'block_timestamp': block.get('block_timestamp'),
        'block_timestamp_truncated': block.get('block_timestamp_truncated'),
        'gas_wanted': tx.get('gas_wanted'),
        'gas_used': tx.get('gas_used'),
        # 'raw_json': json_dumps(tx),
    }