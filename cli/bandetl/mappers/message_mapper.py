from bandetl.utils.string_utils import json_dumps


def map_messages(block, tx):
    for index, raw_msg in enumerate(tx.get('tx', {}).get('value', {}).get('msg', [])):
        message_type = raw_msg.get('type')
        normalized_message_type = normalize_message_type(message_type)

        yield {
            'type': 'message',
            'block_height': block.get('block_height'),
            'block_timestamp': block.get('block_timestamp'),
            'block_timestamp_truncated': block.get('block_timestamp_truncated'),
            'txhash': tx.get('txhash'),
            'message_type': message_type,
            'normalized_message_type': normalized_message_type,
            normalized_message_type: raw_msg.get('value'),
            'index': index,
            # 'raw_json': json_dumps(raw_msg),
        }


def normalize_message_type(message_type):
    return message_type.replace('-', '_').replace('/', '_')
