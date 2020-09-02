## blocks

```
|- block_hash: string
|- block_height: integer (required)                  
|- block_timestamp: string (required)
|- block_timestamp_truncated: timestamp (required)
|- proposer_address: string
|- last_commit_hash: string
|- data_hash: string
|- validators_hash: string
|- next_validators_hash: string
|- consensus_hash: string
|- app_hash: string
|- last_results_hash: string
|- evidence_hash: string
+- signatures: record (repeated)
|  |- block_id_flag: integer
|  |- validator_address: string
|  |- timestamp: timestamp
|  |- signature: bytes
```

## transactions

```
|- block_height: integer (required)                  
|- block_timestamp: string (required)
|- block_timestamp_truncated: timestamp (required)
|- txhash: string
|- type: string
|- gas_wanted: numeric
|- gas_used: numeric
```

## logs

```
|- block_height: integer (required)                  
|- block_timestamp: string (required)
|- block_timestamp_truncated: timestamp (required)
|- txhash: string
|- log_index: integer
|- msg_index: integer
|- log: string
+- events: record (repeated)
|  |- type: string
|  +- attributes: (repeated)
|  |  |- key: string
|  |  |- value: string
```

## messages

```
|- block_height: integer (required)                  
|- block_timestamp: string (required)
|- block_timestamp_truncated: timestamp (required)
|- txhash: string (required)
|- message_type: string (required)
+- oracle_Activate: record
|  |- validator: string
+- oracle_AddReporter: record
|  |- reporter: string
|  |- validator: string
+- oracle_CreateDataSource: record
|  |- executable: bytes
|  |- description: string
|  |- name: string
|  |- sender: string
|  |- owner: string
+- oracle_CreateOracleScript: record
|  |- sender: string
|  |- schema: string
|  |- description: string
|  |- name: string
|  |- code: bytes
|  |- owner: string
+- oracle_EditDataSource: record
|  |- sender: string
|  |- executable: string
|  |- description: string
|  |- name: string
|  |- owner: string
|  |- data_source_id: integer
+- oracle_EditOracleScript: record
|  |- sender: string
|  |- source_code_url: string
|  |- schema: string
|  |- description: string
|  |- name: string
|  |- code: bytes
|  |- owner: string
|  |- oracle_script_id: integer
+- oracle_Report: record
|  |- validator: string
|  |- reporter: string
|  +- raw_reports: record (repeated)
|  |  |- exit_code: integer
|  |  |- data: string
|  |  |- external_id: integer
|  |- request_id: integer
+- oracle_Request: record
|  |- sender: string
|  |- ask_count: integer
|  |- calldata: string
|  |- min_count: integer
|  |- oracle_script_id: integer
+- cosmos_sdk_MsgDelegate: record
|  +- amount: record
|  |  |- amount: integer
|  |  |- denom: string
|  |- validator_address: string
|  |- delegator_address: string
+- cosmos_sdk_MsgEditValidator: record
|  |- commission_rate: string
|  |- address: string
|  |- min_self_delegation: string
|  +- description: record
|  |  |- details: string
|  |  |- security_contact: string
|  |  |- website: string
|  |  |- identity: string
|  |  |- moniker: string
+- cosmos_sdk_MsgMultiSend: record
|  +- outputs: record (repeated)
|  |  +- coins: record (repeated)
|  |  |  |- amount: integer
|  |  |  |- denom: string
|  |  |- address: string
|  +- inputs: record (repeated)
|  |  +- coins: record (repeated)
|  |  |  |- amount: integer
|  |  |  |- denom: string
|  |  |- address: string
+- cosmos_sdk_MsgSend: record
|  |- to_address: string
|  +- amount: record (repeated)
|  |  |- amount: integer
|  |  |- denom: string
|  |- from_address: string
```

All message types:

```
oracle_Activate 
oracle_AddReporter
oracle_CreateDataSource
oracle_CreateOracleScript
oracle_EditDataSource
oracle_EditOracleScript
oracle_Report
oracle_Request
oracle_RemoveReporter -
oracle_OracleRequestPacketData -
oracle_OracleResponsePacketData -


cosmos_sdk_MsgBeginRedelegate
cosmos_sdk_MsgCreateValidator
cosmos_sdk_MsgDelegate +
cosmos_sdk_MsgDeposit
cosmos_sdk_MsgEditValidator +
cosmos_sdk_MsgFundCommunityPool
cosmos_sdk_MsgModifyWithdrawAddress
cosmos_sdk_MsgMultiSend +
cosmos_sdk_MsgSend +
cosmos_sdk_MsgSubmitEvidence
cosmos_sdk_MsgSubmitProposal
cosmos_sdk_MsgUndelegate
cosmos_sdk_MsgUnjail
cosmos_sdk_MsgVerifyInvariant
cosmos_sdk_MsgVote
cosmos_sdk_MsgWithdrawDelegationReward
cosmos_sdk_MsgWithdrawValidatorCommission
```

## oracle_requests

```
|- block_height: integer                     
|- block_timestamp: string
|- block_timestamp_truncated: timestamp
+- request: record
|  |- oracle_script_id: integer
|  |- calldata: string
|  |- requested_validators: string (repeated)
|  |- min_count: integer
|  |- request_height: integer
|  |- request_time: timestamp
|  +- raw_requests: record (repeated)
|  |  |- external_id: integer
|  |  |- data_source_id: integer
|  |  |- calldata: string
+- reports: record (repeated)
|  +- raw_reports: record (repeated)
|  |  |- exit_code: integer
|  |  |- data: bytes
|  |  |- external_id: integer
|  |- in_before_resolve: boolean
|  |- validator: string
+- result: record
|  +- request_packet_data: record
|  |  |- oracle_script_id: integer
|  |  |- calldata: string
|  |  |- ask_count: integer
|  |  |- min_count: integer
|  +- response_packet_data: record
|  |  |- request_id: integer
|  |  |- ans_count: integer
|  |  |- request_time: integer
|  |  |- resolve_time: integer
|  |  |- resolve_status: integer
|  |  |- result: string
+- oracle_script: record
|  |- owner: string
|  |- name: string
|  |- description: string
|  |- filename: string
|  |- schema: string
|  |- source_code_url: string
|- raw_json: string
```

## block_events

```
 |- block_height: integer               
 |- block_timestamp: string
 |- block_timestamp_truncated: timestamp
 |- event_type: string (required)
 |- block_event_type: string (required)
 +- attributes: record (repeated)
 |  |- key: string
 |  |- value: string
 |- raw_json: string (required)
```

TODO: Add schema for messages from x/oracle/types/types.proto for Band types, x/bank/types/tx.pb.go etc. for  
Cosmos SDK types.