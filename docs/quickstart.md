# Quickstart

Install Band ETL CLI:

```bash
pip install band-etl
```

Export blocks, block_events, logs, messages, oracle_requests, transactions ([Schema](schema.md), [Reference](commands.md#export_blocks)):

```bash
bandetl export_blocks \
--start-block 1 \
--end-block 100 \
--provider-uri https://poa-api-backup2.bandchain.org \
--provider-uri-tendermint http://poa-q2.d3n.xyz:26657 \
--output-dir output
```

Find all commands [here](commands.md).
