from dateutil import parser


def truncate_timestamp_to_microseconds(block_timestamp):
    timestamp = parser.parse(block_timestamp)
    truncated_timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return truncated_timestamp
