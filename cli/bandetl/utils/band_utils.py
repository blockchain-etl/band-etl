import hashlib
import logging

from ecdsa import VerifyingKey, SECP256k1

from bandetl.utils.string_utils import base64_string_to_bytes
from pyband.wallet import PublicKey


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


def pubkey_acc_to_address(pubkey_bytes):
    if pubkey_bytes is None:
        return None

    verifying_key = VerifyingKey.from_string(
        pubkey_bytes, curve=SECP256k1, hashfunc=hashlib.sha256
    )

    pubkey = PublicKey(_error_do_not_use_init_directly=True)
    pubkey.verify_key = verifying_key

    return pubkey.to_address().to_acc_bech32()
