# Band Protocol ETL CLI

[![Build Status](https://travis-ci.org/blockchain-etl/band-protocol-etl.svg?branch=master)](https://travis-ci.org/blockchain-etl/band-protocol-etl)
[![Telegram](https://img.shields.io/badge/telegram-join%20chat-blue.svg)](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

Band Protocol ETL CLI lets you convert Band Protocol data into JSON newline-delimited format.

[Full documentation available here](http://band-protocol-etl.readthedocs.io/).

## Quickstart

curl -X GET https://poa-api.bandchain.org/blocks/569102

curl -X GET https://poa-api.bandchain.org/txs?tx.height=568661

## Questions

- Project name choice: Band ETL (band-etl) or Band Protocol ETL (band-protocol-etl)?  
- Cosmos SDK uses "cosmos-sdk/StdTx" as a standard transaction type, but it allows to implement custom tx types.
Does Band define any custom transaction types. 