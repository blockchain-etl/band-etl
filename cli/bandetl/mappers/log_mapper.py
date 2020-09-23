from bandetl.utils.string_utils import json_dumps


def map_logs(block, tx):
    for log_index, log in enumerate(tx.get('logs', [])):
        yield {
            'type': 'log',
            'block_height': block.get('block_height'),
            'block_timestamp': block.get('block_timestamp'),
            'block_timestamp_truncated': block.get('block_timestamp_truncated'),
            'txhash': tx.get('txhash'),
            'log_index': log_index,
            'msg_index': log.get('msg_index'),
            'log': log.get('log'),
            'events': log.get('events'),
        }