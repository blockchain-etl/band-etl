import dateutil


def truncate_timestamp_to_microseconds(block_timestamp):
    timestamp = dateutil.parser.isoparse(block_timestamp)
    truncated_timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return truncated_timestamp
