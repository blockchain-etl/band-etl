from bandetl.utils.band_utils import pubkey_acc_to_address
from bandetl.utils.string_utils import base64_string_to_bytes


def map_transaction(block, tx):
    address = get_sender_from_transaction(tx)

    return {
        'type': 'transaction',
        'transaction_type': tx.get('tx', EMPTY_OBJECT).get('type'),
        'txhash': tx.get('txhash'),
        'block_height': block.get('block_height'),
        'block_timestamp': block.get('block_timestamp'),
        'block_timestamp_truncated': block.get('block_timestamp_truncated'),
        'gas_wanted': tx.get('gas_wanted'),
        'gas_used': tx.get('gas_used'),
        'sender': address,
    }


def get_sender_from_transaction(tx):
    signatures = tx.get('tx', EMPTY_OBJECT).get('value', EMPTY_OBJECT).get('signatures', EMPTY_LIST)
    if len(signatures) > 0:
        first_signature = signatures[0]
        pub_key = first_signature.get('pub_key', EMPTY_OBJECT).get('value')
        if pub_key:
            pub_key_bytes = base64_string_to_bytes(pub_key)
            address = pubkey_acc_to_address(pub_key_bytes)
            return address
        else:
            return None
    else:
        return None


EMPTY_OBJECT = {}
EMPTY_LIST = []
