from bandetl.utils.band_utils import from_val_to_acc_address
from bandetl.utils.string_utils import to_int


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
    msgs = tx.get('tx', EMPTY_OBJECT).get('value', EMPTY_OBJECT).get('msg', EMPTY_LIST)
    if len(msgs) == 0:
        return None

    first_msg = msgs[0]
    return get_sender_from_message(first_msg)


def get_sender_from_message(msg):
    msg_type = msg.get('type')
    msg_value = msg.get('value')

    if msg_type == 'oracle/Activate':
        return from_val_to_acc_address(msg_value.get('validator'))
    if msg_type == 'oracle/AddReporter':
        return from_val_to_acc_address(msg_value.get('validator'))
    if msg_type == 'oracle/CreateDataSource':
        return msg_value.get('sender')
    if msg_type == 'oracle/CreateOracleScript':
        return msg_value.get('sender')
    if msg_type == 'oracle/EditDataSource':
        return msg_value.get('sender')
    if msg_type == 'oracle/EditOracleScript':
        return msg_value.get('sender')
    if msg_type == 'oracle/Report':
        return msg_value.get('reporter')
    if msg_type == 'oracle/Request':
        return msg_value.get('sender')
    if msg_type == 'oracle/RemoveReporter':
        return from_val_to_acc_address(msg_value.get('validator'))

    if msg_type == 'cosmos-sdk/MsgDelegate':
        return msg_value.get('delegator_address')
    if msg_type == 'cosmos-sdk/MsgEditValidator':
        return from_val_to_acc_address(msg_value.get('address'))
    if msg_type == 'cosmos-sdk/MsgMultiSend':
        inputs = msg_value.get('inputs')
        if inputs:
            return inputs[0].get('address')
    if msg_type == 'cosmos-sdk/MsgSend':
        return msg_value.get('from_address')
    if msg_type == 'cosmos-sdk/MsgBeginRedelegate':
        return msg_value.get('delegator_address')
    if msg_type == 'cosmos-sdk/MsgCreateValidator':
        return msg_value.get('delegator_address')
    if msg_type == 'cosmos-sdk/MsgDeposit':
        return msg_value.get('depositor')
    if msg_type == 'cosmos-sdk/MsgFundCommunityPool':
        return msg_value.get('depositor')
    if msg_type == 'cosmos-sdk/MsgModifyWithdrawAddress':
        return msg_value.get('delegator_address')
    if msg_type == 'cosmos-sdk/MsgSubmitEvidence':
        return msg_value.get('submitter')
    if msg_type == 'cosmos-sdk/MsgSubmitProposal':
        return msg_value.get('proposer')
    if msg_type == 'cosmos-sdk/MsgUndelegate':
        return msg_value.get('delegator_address')
    if msg_type == 'cosmos-sdk/MsgUnjail':
        return from_val_to_acc_address(msg_value.get('address'))
    if msg_type == 'cosmos-sdk/MsgVerifyInvariant':
        return msg_value.get('sender')
    if msg_type == 'cosmos-sdk/MsgVote':
        return msg_value.get('voter')
    if msg_type == 'cosmos-sdk/MsgWithdrawDelegationReward':
        return msg_value.get('delegator_address')
    if msg_type == 'cosmos-sdk/MsgWithdrawValidatorCommission':
        return from_val_to_acc_address(msg_value.get('validator_address'))
    return None


EMPTY_OBJECT = {}
EMPTY_LIST = []
