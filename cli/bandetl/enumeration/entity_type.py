class EntityType:
    BLOCK = 'block'
    TRANSACTION = 'transaction'
    LOG = 'log'
    MESSAGE = 'message'
    BLOCK_EVENT = 'block_event'
    ORACLE_REQUEST = 'oracle_request'

    ALL_FOR_STREAMING = [BLOCK, TRANSACTION, LOG, MESSAGE, BLOCK_EVENT, ORACLE_REQUEST]
