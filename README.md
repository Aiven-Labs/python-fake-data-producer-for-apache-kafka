# kafka-python-fake-data-producer
An Apache Kafka fake data producer with Python and Faker. For more info about the setup check the [blog post]()


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
