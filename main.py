from faker import Faker
import json
from kafka import KafkaProducer
import time
import sys
import random
import argparse
from pizzaproducer import PizzaProvider
from userbehaviorproducer import UserBehaviorProvider
from stockproducer import StockProvider
from realstockproducer import RealStockProvider
from metricproducer import MetricProvider
from userbets import UserBetsProvider


MAX_NUMBER_PIZZAS_IN_ORDER = 10
MAX_ADDITIONAL_TOPPINGS_IN_PIZZA = 5



# Creating a Faker instance and seeding to have the same results every time we execute the script
fake = Faker()
Faker.seed(4321)


# function produce_msgs starts producing messages with Faker
def produce_msgs(security_protocol='SSL',
                 cert_folder = '~/kafka-pizza/',
                 hostname = 'hostname',
                 port = '1234',
                 topic_name = 'pizza-orders',
                 nr_messages = -1,
                 max_waiting_time_in_sec = 5,
                 subject = 'pizza'):
    if security_protocol.upper() == 'PLAINTEXT':
        producer = KafkaProducer(
            bootstrap_servers=hostname + ':' + port,
            security_protocol='PLAINTEXT',
            value_serializer=lambda v: json.dumps(v).encode('ascii'),
            key_serializer=lambda v: json.dumps(v).encode('ascii')
        )
    elif security_protocol.upper() == 'SSL':
        producer = KafkaProducer(
            bootstrap_servers=hostname + ':' + port,
            security_protocol='SSL',
            ssl_cafile=cert_folder+'/ca.pem',
            ssl_certfile=cert_folder+'/service.cert',
            ssl_keyfile=cert_folder+'/service.key',
            value_serializer=lambda v: json.dumps(v).encode('ascii'),
            key_serializer=lambda v: json.dumps(v).encode('ascii')
        )
    else:
        sys.exit("This security protocol is not supported!")

    if nr_messages <= 0:
        nr_messages = float('inf')
    i = 0
    
    if subject == 'stock':
        fake.add_provider(StockProvider)
    elif subject == 'realstock':
        fake.add_provider(RealStockProvider)
    elif subject == 'metric':
        fake.add_provider(MetricProvider)
    elif subject == 'userbehaviour':
        fake.add_provider(UserBehaviorProvider)
    elif subject == 'bet':
        fake.add_provider(UserBetsProvider)
    else:
        fake.add_provider(PizzaProvider)
    while i < nr_messages:
        if subject in ['stock', 'userbehaviour', 'realstock', 'metric','bet']:
            message, key = fake.produce_msg()
        else:
            message, key = fake.produce_msg(fake, i, MAX_NUMBER_PIZZAS_IN_ORDER, MAX_ADDITIONAL_TOPPINGS_IN_PIZZA)

        print('Sending: {}'.format(message))
        # sending the message to Kafka
        producer.send(topic_name,
                      key=key,
                      value=message)
        # Sleeping time
        sleep_time = random.randint(0, int(max_waiting_time_in_sec * 10000))/10000
        print('Sleeping for...'+str(sleep_time)+'s')
        time.sleep(sleep_time)

        # Force flushing of all messages
        if (i % 100) == 0:
            producer.flush()
        i = i + 1
    producer.flush()

# calling the main produce_msgs function: parameters are:
#   * nr_messages: number of messages to produce
#   * max_waiting_time_in_sec: maximum waiting time in sec between messages

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--security-protocol', help='Security protocol for Kafka (PLAINTEXT, SSL)', required=True)
    parser.add_argument('--cert-folder', help='Path to folder containing required Kafka certificates. Required --security-protocol equal SSL', required=False)
    parser.add_argument('--host', help='Kafka Host (obtained from Aiven console)', required=True)
    parser.add_argument('--port', help='Kafka Port (obtained from Aiven console)', required=True)
    parser.add_argument('--topic-name', help='Topic Name', required=True)
    parser.add_argument('--nr-messages', help='Number of messages to produce (0 for unlimited)', required=True)
    parser.add_argument('--max-waiting-time', help='Max waiting time between messages (0 for none)', required=True)
    parser.add_argument('--subject', help='What type of content to produce (possible choices are [pizza, userbehaviour, stock, realstock, metric] pizza is the default', required=False)
    args = parser.parse_args()
    p_security_protocol = args.security_protocol
    p_cert_folder =args.cert_folder
    p_hostname =args.host
    p_port =args.port
    p_topic_name=args.topic_name
    p_subject=args.subject
    produce_msgs(security_protocol=p_security_protocol,
                 cert_folder=p_cert_folder,
                 hostname=p_hostname,
                 port=p_port,
                 topic_name=p_topic_name,
                 nr_messages=int(args.nr_messages),
                 max_waiting_time_in_sec=float(args.max_waiting_time),
                 subject=p_subject
                 )
    print(args.nr_messages)

if __name__ == '__main__':
    main()
