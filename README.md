# Band ETL

[![Build Status](https://travis-ci.org/blockchain-etl/band-etl.svg?branch=master)](https://travis-ci.org/blockchain-etl/band-etl)
[![Telegram](https://img.shields.io/badge/telegram-join%20chat-blue.svg)](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

## Overview

Band ETL allows you to setup an ETL pipeline in Google Cloud Platform for ingesting Band blockchain data 
into BigQuery and Pub/Sub. It comes with [CLI tools](/cli) for exporting Band data into JSON newline-delimited files
partitioned by day. 

Data is available for you to query right away in 
[Google BigQuery](https://console.cloud.google.com/bigquery?page=dataset&d=mainnet&p=band-etl).

## Architecture

![band_etl_architecture.svg](band_etl_architecture.svg)

[Google Slides version](https://docs.google.com/presentation/d/1VFMR4f8lghnpGZWZTevRTv6Zn9n9IUWHRnNrQsNE-8Y/edit#slide=id.p89)

1. The nodes are run in a Kubernetes cluster. 
    Refer to [Band Node in Kubernetes](https://github.com/blockchain-etl/band-kubernetes) for deployment instructions.

2. [Airflow DAGs](https://airflow.apache.org/) export and load Band data to BigQuery daily. 
    Refer to [Band ETL Airflow](/airflow) for deployment instructions.
  
3. Band data is polled periodically from the nodes and pushed to Google Pub/Sub. 
    Refer to [Band ETL Streaming](/streaming) for deployment instructions.  
  
4. Band data is pulled from Pub/Sub, transformed and streamed to BigQuery. 
    Refer to [Band ETL Dataflow](/dataflow) for deployment instructions.  
 
## Setting Up

1. Follow the instructions in [Band Node in Kubernetes](https://github.com/blockchain-etl/band-kubernetes) to deploy
    an Band node in GKE. Wait until it's fully synced. Make note of the Load Balancer IP from the node deployment, it
    will be used in Airflow and Streamer components below.

2. Follow the instructions in [Band ETL Airflow](/airflow) to deploy a Cloud Composer cluster for 
    exporting and loading historical Band data. It may take several hours for the export DAG to catch up. During this
    time "load" and "verify_streaming" DAGs will fail. 

3. Follow the instructions in [Band ETL Streaming](/streaming) to deploy the Streamer component. For the value in 
    `last_synced_block.txt` specify the last block number of the previous day. You can query it in BigQuery:
    `SELECT height FROM mainnet.blocks ORDER BY height DESC LIMIT 1`.

4. Follow the instructions in [Band ETL Dataflow](/dataflow) to deploy the Dataflow component. Monitor 
    "verify_streaming" DAG in Airflow console, once the Dataflow job catches up the latest block, the DAG will succeed.