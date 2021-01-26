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
python main.py --cert-folder ~/Documents/kafkaCerts/kafka-test/ --host kafka-2e15adc9-dev-advocates.aivencloud.com --port 13041 --nr-messages 0 --max_waiting_time 0
```
Where
* `cert-folder`: points to the folder containing the Kafka certificates (see [blog post]() for more)
* `host`: the Kafka host
* `port`: the Kafka port
* `nr-messages`: the number of messages to send
* `max_waiting_time`: the maximum waiting time in seconds between messages
