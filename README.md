# Kafka Python Fake DataP Producer

## Description

**Kafka Python Fake Data Producer** is a complete demo app allowing you to quickly produce a fake Pizza-based streaming dataset and push it to an Apache Kafka topic.

* **Apache Kafka**: a [distributed streaming platform](https://kafka.apache.org/)
* **Topic**: all Kafka records are organised into topics, you can think of a topic like an event log.
* **Kafka Producer**: an entity/application that publishes data to Kafka

An Apache Kafka cluster can be [installed locally](https://kafka.apache.org/quickstart) or created in minutes using [Aiven.io console](https://console.aiven.io/signup?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post).

For more informations about the code building blogs check the [blog post](blogs.aiven.io)


## Installation

```
pip install faker
pip install kafka-python
```

## Usage

The Python code can be run in bash with the following

```
python main.py --cert-folder ~/Documents/kafkaCerts/kafka-test/ \
  --host kafka-<name>.aivencloud.com \
  --port 13041 \
  --topic-name pizza-orders \
  --nr-messages 0 \
  --max-waiting-time 0
```
Where
* `cert-folder`: points to the folder containing the Kafka certificates (see [blog post]() for more)
* `host`: the Kafka host
* `port`: the Kafka port
* `topic-name`: the Kafka topic name to write to (the topic needs to be pre-created or `kafka.auto_create_topics_enable` parameter enabled)
* `nr-messages`: the number of messages to send
* `max-waiting-time`: the maximum waiting time in seconds between messages

# Starting your Kafka Service with Aiven.io

Once created your account you can start your Kafka service with [Aiven.io's cli](https://github.com/aiven/aiven-client)

```
avn service create  \
  -t kafka <KAFKA_INSTANCE_NAME> \
  -p <AIVEN_PLAN_NAME> \
  --cloud  <CLOUD_PROVIDER> \
  --project <PROJECT_NAME> \
  -c kafka_rest=true \
  -c kafka.auto_create_topics_enable=true \
  -c schema_registry=true
```

Download the required certificates with
```
avn service user-creds-download <KAFKA_SERVICE_NAME> \
  --project <PROJECT_NAME>    \
  -d <DESTINATION_FOLDER_NAME> \
  --username avnadmin
```
And Kafka Service URI with

```
avn service get <KAFKA_SERVICE_NAME> \
  --project <PROJECT_NAME> \
  --format '{service_uri}'
```
For a more detailed description of services and required credentials, check the [blog post](blogs.aiven.io)

## No Pizza? No Problem!

The demo app produces pizza data, however is very simple to change the dataset produced to anything else.
The code is based on [Faker](https://faker.readthedocs.io/en/master/), an Open Source Python library to generate fake data.

To modify the data generated, change the `produce_pizza_order` function within the `main.py` file. The output of the function should be two python dictionaries, containing the event `key` and `message`

```
def produce_pizza_order (ordercount = 1):
    message = {
        'name': fake.unique.name(),
        'phoneNumber': fake.phone_number(),
        'address': fake.address()
      }
    key = {'order' = ordercount}
    return message, key
```

To customise your dataset, you can check Faker's providers in the [related doc](https://faker.readthedocs.io/en/master/providers.html)
