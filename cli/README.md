# Band Protocol ETL CLI

[![Build Status](https://travis-ci.org/blockchain-etl/band-protocol-etl.svg?branch=master)](https://travis-ci.org/blockchain-etl/band-protocol-etl)
[![Telegram](https://img.shields.io/badge/telegram-join%20chat-blue.svg)](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

Band Protocol ETL CLI lets you convert Band Protocol data into JSON newline-delimited format.

[Full documentation available here](http://band-protocol-etl.readthedocs.io/).

## Quickstart

Install Band ETL CLI:

```bash
pip3 install band-etl
```

Export blocks, block_events, logs, messages, oracle_requests, transactions ([Schema](../docs/schema.md), [Reference](../docs/commands.md)):

```bash
> bandetl export_blocks \
--start-block 1 \
--end-block 100 \
--provider-uri https://poa-api-backup2.bandchain.org \
--provider-uri-tendermint http://poa-q2.d3n.xyz:26657 \
--output-dir output 
```

---

Stream blocks, block_events, logs, messages, oracle_requests, transactions to console ([Reference](../docs/commands.md#stream)):

```bash
> pip3 install band-etl[streaming]
> bandetl stream --start-block 500000 -e block,action,log --log-file log.txt \
--provider-uri https://poa-api-backup2.bandchain.org
```

Find other commands [here](https://band-etl.readthedocs.io/en/latest/commands/).

For the latest version, check out the repo and call 
```bash
> pip3 install -e . 
> python3 bandetl.py
```

## Useful Links

- [Schema](https://band-etl.readthedocs.io/en/latest/schema/)
- [Command Reference](https://band-etl.readthedocs.io/en/latest/commands/)
- [Documentation](https://band-etl.readthedocs.io/)

## Running Tests

```bash
> pip3 install -e .[dev,streaming]
> export BAND_PROVIDER_URI=https://poa-api-backup2.bandchain.org
> pytest -vv
```

### Running Tox Tests

```bash
> pip3 install tox
> tox
```

## Running in Docker

1. Install Docker https://docs.docker.com/install/

2. Build a docker image
        
        > docker build -t band-etl:latest .
        > docker image ls
        
3. Run a container out of the image

        > docker run -v $HOME/output:/band-etl/output band-etl:latest export_blocks -s 1 -e 5499999 -b 1000 -o out

4. Run streaming to console or Pub/Sub

        > docker build -t band-etl:latest -f Dockerfile .
        > echo "Stream to console"
        > docker run band-etl:latest stream --start-block 500000 --log-file log.txt
        > echo "Stream to Pub/Sub"
        > docker run -v /path_to_credentials_file/:/band-etl/ --env GOOGLE_APPLICATION_CREDENTIALS=/band-etl/credentials_file.json band-etl:latest stream --start-block 500000 --output projects/<your-project>/topics/mainnet
