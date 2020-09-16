from bandetl.utils.band_utils import pubkey_acc_to_address
from bandetl.utils.string_utils import base64_string_to_bytes, to_int


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
        'fee': get_fee(tx),
        'memo': tx.get('tx', EMPTY_OBJECT).get('value', EMPTY_OBJECT).get('memo')
    }


def get_fee(tx):
    fee = tx.get('tx', EMPTY_OBJECT).get('value', EMPTY_OBJECT).get('fee', EMPTY_OBJECT)
    amount_list = [map_amount(amt) for amt in fee.get('amount', EMPTY_LIST)]
    return {
        'amount': amount_list,
        'gas': to_int(fee.get('gas'))
    }


def map_amount(amount):
    return {
        'denom': amount.get('denom'),
        'amount': to_int(amount.get('amount'))
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
