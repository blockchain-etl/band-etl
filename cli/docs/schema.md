## blocks

```
hash: STRING
height: INTEGER
timestamp: TIMESTAMP
proposer_address: STRING
last_commit_hash: STRING
data_hash: STRING
validators_hash: STRING
next_validators_hash: STRING
consensus_hash: STRING
app_hash: STRING
last_results_hash: STRING
evidence_hash: STRING
signatures: REPEATED
├── block_id_flag: INTEGER
├── validator_address: STRING
├── timestamp: TIMESTAMP
├── signature: BYTES
```

## transactions

```
transactions (table name, not part of column names)
height: INTEGER
txhash: STRING
timestamp: TIMESTAMP
type: STRING
gas_wanted: NUMERIC
gas_used: NUMERIC
```

## logs

```
logs (table name, not part of column names)
height: INTEGER
txhash: STRING
timestamp: TIMESTAMP
log_index: INTEGER
msg_index: INTEGER
log: STRING
events: STRUCT (REPEATED)
├── type: STRING
├── attributes: REPEATED
    ├── key: STRING
    ├── value: STRING
```

## messages

```
messages (table name, not part of column names)
height: INTEGER
txhash: STRING
timestamp: TIMESTAMP
msg_index: INTEGER
type: STRING

oracle_Request: STRUCT
├── oracle_script_id: STRING
├── calldata: BYTES
├── ask_count: STRING
├── min_count: STRING
├── client_id: STRING
├── sender: STRING

oracle_Report

oracle_CreateDataSource

oracle_EditDataSource

oracle_CreateOracleScript

oracle_EditOracleScript

oracle_Activate

oracle_AddReporter

oracle_RemoveReporter

oracle_OracleRequestPacketData

oracle_OracleResponsePacketData

cosmos_sdk_MsgSend

cosmos_sdk_MsgMultiSend: STRUCT
├── inputs: STRUCT (REPEATED)
    ├── address: STRING
    ├── coins: STRUCT (REPEATED)
        ├── denom: STRING
        ├── amount: STRING
├── outputs: STRUCT (REPEATED)
    ├── address: STRING
    ├── coins: STRUCT (REPEATED)
        ├── denom: STRING
        ├── amount: STRING

cosmos_sdk_MsgVerifyInvariant

cosmos_sdk_MsgWithdrawDelegationReward

cosmos_sdk_MsgWithdrawValidatorCommission

cosmos_sdk_MsgModifyWithdrawAddress

cosmos_sdk_MsgFundCommunityPool

cosmos_sdk_MsgSubmitEvidence

cosmos_sdk_MsgSubmitProposal

cosmos_sdk_MsgDeposit

cosmos_sdk_MsgVote

cosmos_sdk_MsgUnjail

cosmos_sdk_MsgCreateValidator

cosmos_sdk_MsgEditValidator

cosmos_sdk_MsgDelegate

cosmos_sdk_MsgUndelegate

cosmos_sdk_MsgBeginRedelegate

```

TODO: Add schema for messages from x/oracle/types/types.proto for Band types, x/bank/types/tx.pb.go etc. for  
Cosmos SDK types.