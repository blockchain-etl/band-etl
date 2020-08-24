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

cosmos_sdk_msgmultisend: STRUCT
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

oracle_request: STRUCT
├── oracle_script_id: STRING
├── calldata: BYTES
├── ask_count: STRING
├── min_count: STRING
├── client_id: STRING
├── sender: STRING
  
TODO
```

