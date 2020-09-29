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
|- sender: string
|- fee: string
|  +- amount: record
|  |  |- amount: integer
|  |  |- denom: string
|  |- gas: integer
|- memo: string
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
+- oracle_RemoveReporter: record
|  |- validator: string
|  |- reporter: string
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
+- cosmos_sdk_MsgBeginRedelegate: record
|  |- delegator_address: string
|  |- validator_src_address: string
|  |- validator_dst_address: string
|  +- amount: record
|  |  |- amount: integer
|  |  |- denom: string
+- cosmos_sdk_MsgCreateValidator: record
|  +- description: record
|  |  |- moniker: string
|  |  |- identity: string
|  |  |- website: string
|  |  |- security_contact: string
|  |  |- details: string
|  +- commission: record
|  |  |- rate: integer
|  |  |- max_rate: integer
|  |  |- max_change_rate: integer
|  |- min_self_delegation: integer
|  |- delegator_address: string
|  |- validator_address: string
|  |- pubkey: string
|  +- value: record
|  |  |- amount: integer
|  |  |- denom: string
+- cosmos_sdk_MsgDeposit: record
|  |- proposal_id: integer
|  |- depositor: string
|  +- amount: record (repeated)
|  |  |- amount: integer
|  |  |- denom: string
+- cosmos_sdk_MsgFundCommunityPool: record
|  |- depositor: string
|  +- amount: record (repeated)
|  |  |- amount: integer
|  |  |- denom: string
+- cosmos_sdk_MsgModifyWithdrawAddress: record
|  |- delegator_address: string
|  |- withdraw_address: string
+- cosmos_sdk_MsgSubmitEvidence: record
|  |- submitter: string
|  |- evidence: string
+- cosmos_sdk_MsgSubmitProposal: record
|  |- content: string
|  |- proposer: string
|  +- initial_deposit: record (repeated)
|  |  |- amount: integer
|  |  |- denom: string
+- cosmos_sdk_MsgUndelegate: record
|  |- delegator_address: string
|  |- validator_address: string
|  +- amount: record
|  |  |- amount: integer
|  |  |- denom: string
+- cosmos_sdk_MsgUnjail: record
|  |- address: string
+- cosmos_sdk_MsgVerifyInvariant: record
|  |- sender: string
|  |- invariant_module_name: string
|  |- invariant_route: string
+- cosmos_sdk_MsgVote: record
|  |- proposal_id: integer
|  |- voter: string
|  |- option: integer
+- cosmos_sdk_MsgWithdrawDelegationReward: record
|  |- delegator_address: string
|  |- validator_address: string
+- cosmos_sdk_MsgWithdrawValidatorCommission: record
|  |- validator_address: string
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
+- decoded_result: record
|  +- calldata: string
|  +- result: string
+- oracle_script: record
|  |- owner: string
|  |- name: string
|  |- description: string
|  |- filename: string
|  |- schema: string
|  |- source_code_url: string
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
```
