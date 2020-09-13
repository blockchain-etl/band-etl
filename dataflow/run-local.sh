#!/usr/bin/env bash

mvn -Pdirect-runner compile exec:java \
-Dexec.mainClass=io.blockchainetl.band.BandPubSubToBigQueryPipeline \
-Dexec.args="--chainConfigFile=chainConfig.json \
--tempLocation=gs://band-etl-dev-dataflow-0/ \
--outputErrorsTable=crypto_band.errors"

