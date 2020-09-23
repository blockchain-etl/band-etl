
from bandetl.utils.band_utils import decode_oracle_request_calldata, decode_oracle_response_result
from bandetl.utils.string_utils import json_dumps
from pyband.obi import PyObi


def map_oracle_requests(block, oracle_request_id, oracle_request, oracle_script):
    mapped_oracle_request = map_oracle_request(oracle_request, oracle_script)
    return {**mapped_oracle_request, **{
        'type': 'oracle_request',
        'oracle_request_id': oracle_request_id,
        'block_height': block.get('block_height'),
        'block_timestamp': block.get('block_timestamp'),
        'block_timestamp_truncated': block.get('block_timestamp_truncated'),
    }}


def map_oracle_request(oracle_request, oracle_script):
    schema = oracle_script['result']['schema']

    obi = PyObi(schema)

    calldata = oracle_request['result']['result']['request_packet_data'].get('calldata')
    response_result = oracle_request['result']['result']['response_packet_data'].get('result')

    decoded_calldata = decode_oracle_request_calldata(obi, calldata)
    decoded_response_result = decode_oracle_response_result(obi, response_result)

    return {**oracle_request['result'], **{
        'oracle_script': oracle_script['result'],
        'decoded_result': {
            'calldata': json_dumps(decoded_calldata),
            'result': json_dumps(decoded_response_result),
        }
    }}
