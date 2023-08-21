# Quickstart with Gitpod

This workspace comes with some pre-installed stuff for you : 

* Python requirements have already been installed
* avn CLI has already been installed
* jq has benn installed

First make sure to have an Aiven account, otherwise you are just a few clicks away of creating one [here](https://console.aiven.io/signup?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post)

Then make sure to get an personal access token, check this [video](https://www.youtube.com/watch?v=64G2QIMYOL4) to learn how to get one. 

Open a terminal, you'll need to copy-paste or re-type all the bash commands below.

Now you can login : 

```bash
avn user login --token

```

Create a `certs` folder : 

```bash
mkdir certs
```

Set your variables :
```bash
KAFKA_INSTANCE_NAME=my-kafka-demo
CLOUD_REGION=aws-eu-south-1
AIVEN_PLAN_NAME=startup-2
DESTINATION_FOLDER_NAME=certs
```

If you haven't yet, create a Aiven for Apache Kafka service : 

```bash
avn service create $KAFKA_INSTANCE_NAME     \
    -t kafka                                \
    --cloud $CLOUD_REGION                   \
    -p $AIVEN_PLAN_NAME                     \
    -c kafka.auto_create_topics_enable=true \
    -c kafka_rest=true                    

```

Retrieve your host and port from the console and set them : 
And retrieve the Apache Kafka Service URI with

```bash

KAFKA_HOST=$(avn service get $KAFKA_INSTANCE_NAME --json | jq -r '.service_uri_params.host')
KAFKA_PORT=$(avn service get $KAFKA_INSTANCE_NAME --json | jq -r '.service_uri_params.port')

```

You can wait for the newly created Apache Kafka instance to be ready with : 

```bash
avn service wait $KAFKA_INSTANCE_NAME
```

Now get your certificates : 

```bash
avn service user-creds-download $KAFKA_INSTANCE_NAME \
  -d $DESTINATION_FOLDER_NAME \
  --username avnadmin
```

And finally run the demo : 

```bash

python main.py \
  --security-protocol ssl \
  --cert-folder $DESTINATION_FOLDER_NAME\
  --host $KAFKA_HOST \
  --port $KAFKA_PORT \
  --topic-name pizza-orders \
  --nr-messages 0 \
  --max-waiting-time 2 \
  --subject pizza

```

You should see a continuous flow of data being pushed to Apache Kafka, to the topic defined by the `--topic-name` parameter. You can either use the Aiven console, or tools like [kcat](https://docs.aiven.io/docs/products/kafka/howto/kcat) to browse the data.
