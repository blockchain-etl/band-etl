from bandetl.utils.datetime_utils import truncate_timestamp_to_microseconds


def map_block(data):
    header = data.get('block').get('header')
    block_timestamp = header.get('time')
    block_timestamp_truncated = truncate_timestamp_to_microseconds(block_timestamp)
    return {
        'type': 'block',
        'block_hash': data['block_id']['hash'],
        'block_height': header.get('height'),
        'block_timestamp': block_timestamp,
        'block_timestamp_truncated': block_timestamp_truncated,
        'proposer_address': header['proposer_address'],
        'last_commit_hash': header['last_commit_hash'],
        'data_hash': header['data_hash'],
        'validators_hash': header['validators_hash'],
        'next_validators_hash': header['next_validators_hash'],
        'consensus_hash': header['consensus_hash'],
        'app_hash': header['app_hash'],
        'last_results_hash': header['last_results_hash'],
        'evidence_hash': header['evidence_hash'],
        'signatures': data['block']['last_commit']['signatures'],
    }