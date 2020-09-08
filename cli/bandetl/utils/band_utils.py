import logging

from bandetl.utils.string_utils import base64_string_to_bytes


def decode_oracle_request_calldata(obi, calldata):
    if calldata is None:
        return None
    try:
        calldata_bytes = base64_string_to_bytes(calldata)
        decoded_calldata = obi.decode_input(calldata_bytes)
        return decoded_calldata
    except Exception:
        logging.exception('An exception occurred while decoding calldata {}.'.format(calldata))
        return None


def decode_oracle_response_result(obi, result):
    if result is None:
        return None
    try:
        result_bytes = base64_string_to_bytes(result)
        decoded_calldata = obi.decode_output(result_bytes)
        return decoded_calldata
    except Exception:
        logging.exception('An exception occurred while decoding response result {}.'.format(result))
        return None