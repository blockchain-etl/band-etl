from bandetl.utils.string_utils import json_dumps


def map_block_events(block, block_events):
    for index, [event_type, event] in enumerate(block_events):
        yield {
            'type': 'block_event',
            'block_height': block.get('block_height'),
            'block_timestamp': block.get('block_timestamp'),
            'block_timestamp_truncated': block.get('block_timestamp_truncated'),
            'event_type': event.get('type'),
            'block_event_type': event_type,
            'index': index,
            # 'raw_json': json_dumps(event),
        }
