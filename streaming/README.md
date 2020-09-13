# Band ETL Streaming

Streams Band data to [Google Pub/Sub](https://cloud.google.com/pubsub) using 
[bandetl stream](https://github.com/blockchain-etl/band-etl/tree/develop/docs/commands.md#stream). 
Runs in Google Kubernetes Engine. 

Read [this article](https://medium.com/google-cloud/live-ethereum-and-bitcoin-data-in-google-bigquery-and-pub-sub-765b71cd57b5) 
explaining how to subscribe to public blockchain data in [Pub/Sub](https://cloud.google.com/pubsub/docs/overview). 

## Prerequisites

- Kubernetes 1.8+
- Helm 2.16
- PV provisioner support in the underlying infrastructure
- [gcloud](https://cloud.google.com/sdk/install)

## Setting Up

1. Create a GKE cluster:

    ```bash
    gcloud container clusters create band-etl-streaming \
    --zone us-central1-a \
    --num-nodes 1 \
    --disk-size 10GB \
    --machine-type n1-standard-1 \
    --network default \
    --subnetwork default \
    --scopes pubsub,storage-rw,logging-write,monitoring-write,service-management,service-control,trace
    
    gcloud container clusters get-credentials band-etl-streaming --zone us-central1-a
   
    # Make sure the user has "Kubernetes Engine Admin" role.
    helm init
    bash patch-tiller.sh
    ```

2. Create Pub/Sub topics and subscriptions:

    ```bash
    gcloud deployment-manager deployments create band-etl-pubsub-topics-0 --template deployment_manager_pubsub_topics.py
    gcloud deployment-manager deployments create band-etl-pubsub-subscriptions-0 --template deployment_manager_pubsub_subscriptions.py \
    --properties topics_project:<project_where_topics_deployed>
    ```

3. Create GCS bucket. Upload a text file with block number you want to start streaming from to 
`gs:/<YOUR_BUCKET_HERE>/band-etl/streaming/last_synced_block.txt`.

4. Create "band-etl-app" service account with roles:
    - Pub/Sub Editor
    - Storage Object Admin

    Download the key. Create a Kubernetes secret:

    ```bash
    kubectl create secret generic streaming-app-key --from-file=key.json=$HOME/Downloads/key.json
    ```
   
5. Copy [example_values.yaml](example_values.yaml) file to `values.yaml` and adjust it at least with 
    your bucket and project ID.

6. Install ETL apps via helm using chart from this repo and values we adjust on previous step, for example:

    ```bash
    helm install --name band-etl charts/band-etl-streaming --values values.yaml
    ``` 

7. Use `describe` command to troubleshoot, f.e.:

    ```bash
    kubectl describe pods
    kubectl describe node [NODE_NAME]
    ```

## Configuration

The following table lists the configurable parameters of the band-etl-streaming chart and their default values.

Parameter                                                | Description                                       | Default
-------------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
`stream.image.repository`                                | Stream image source repository name               | `blockchainetl/band-etl`
`stream.image.tag`                                       | Image release tag                                 | `1.0.1`
`stream.image.pullPolicy`                                | Image pull policy                                 | `IfNotPresent`
`stream.resources`                                       | CPU/Memory resource request/limit                 | `100m/128Mi, 350m/512Mi`
`stream.env.LAST_SYNCED_BLOCK_FILE_MAX_AGE_IN_SECONDS`   | The number of seconds since new blocks have been pulled from the node, after which the deployment is considered unhealthy                 | `600`
`config.PROVIDER_URI`                                    | URI of Band node                                  | `https://poa-api-backup2.bandchain.org`
`config.PROVIDER_URI_TENDERMINT`                         | URI of Tendermint node                            | `http://poa-q2.d3n.xyz:26657`
`config.STREAM_OUTPUT`                                   | Google Pub Sub topic path prefix                  | `projects/<your-project>/topics/crypto_band`
`config.GCS_PREFIX`                                      | Google Storage directory of last synced block file| `gs://<your-bucket>/band-etl/streaming`
`config.ENTITY_TYPES`                                    | The list of entity types to export                | ``
`config.LAG_BLOCKS`                                      | The number of blocks to lag behind the network    | `10`
`config.MAX_WORKERS`                                     | The number of workers                             | `4`
`lsb_file`                                               | Last synced block file name                       | `last_synced_block.txt`

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```bash
$ helm install --name band-etl --values values.yaml charts/band-etl-streaming
```

### Creating a Cloud Source Repository for Configuration Files

Below are the commands for creating a Cloud Source Repository to hold values.yaml: 

```bash
REPO_NAME=${PROJECT}-streaming-config-${ENVIRONMENT_INDEX} && echo "Repo name ${REPO_NAME}"
gcloud source repos create ${REPO_NAME}
gcloud source repos clone ${REPO_NAME} && cd ${REPO_NAME}

# Put values.yaml to the root of the repo

git add values.yaml && git commit -m "Initial commit"
git push
```

Check a [separate file](ops.md) for operations.