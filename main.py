from faker import Faker
import json
from kafka import KafkaProducer
import time
import random
import argparse
from pizzaproducer import PizzaProvider

MAX_NUMBER_PIZZAS_IN_ORDER = 10
MAX_ADDITIONAL_TOPPINGS_IN_PIZZA = 5



# Creating a Faker instance and seeding to have the same results every time we execute the script
fake = Faker()
Faker.seed(4321)



# Adding the newly created PizzaProvider to the Faker instance
fake.add_provider(PizzaProvider)

# creating function to generate the pizza Order
def produce_pizza_order (ordercount = 1):
    shop = fake.pizza_shop()
    # Each Order can have 1-10 pizzas in it
    pizzas = []
    for pizza in range(random.randint(1, MAX_NUMBER_PIZZAS_IN_ORDER)):
        # Each Pizza can have 0-5 additional toppings on it
        toppings = []
        for topping in range(random.randint(0, MAX_ADDITIONAL_TOPPINGS_IN_PIZZA)):
            toppings.append(fake.pizza_topping())
        pizzas.append({
            'pizzaName': fake.pizza_name(),
            'additionalToppings': toppings
        })
    # message composition
    message = {
        'id': ordercount,
        'shop': shop,
        'name': fake.unique.name(),
        'phoneNumber': fake.unique.phone_number(),
        'address': fake.address(),
        'pizzas': pizzas
    }
    key = {'shop': shop}
    return message, key


# function produce_msgs starts producing messages with Faker
def produce_msgs(cert_folder="~/kafka-pizza/",
                 hostname='hostname',
                 port='1234',
                 topic_name='pizza-orders',
                 nr_messages=-1,
                 max_waiting_time_in_sec=5):
    producer = KafkaProducer(
        bootstrap_servers=hostname+":"+port,
        security_protocol="SSL",
        ssl_cafile=cert_folder+"/ca.pem",
        ssl_certfile=cert_folder+"/service.cert",
        ssl_keyfile=cert_folder+"/service.key",
        value_serializer=lambda v: json.dumps(v).encode('ascii'),
        key_serializer=lambda v: json.dumps(v).encode('ascii')
    )
    if nr_messages <= 0:
        nr_messages = float('inf')
    i = 0
    while i < nr_messages:
        message, key = produce_pizza_order(i)

        print("Sending: {}".format(message))
        # sending the message to Kafka
        producer.send(topic_name,
                      key=key,
                      value=message)
        # Sleeping time
        sleep_time = random.randint(0, max_waiting_time_in_sec * 10)/10
        print("Sleeping for..."+str(sleep_time)+'s')
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
    parser.add_argument('--cert-folder', help="Path to folder containing required Kafka certificates", required=True)
    parser.add_argument('--host', help="Kafka Host (obtained from Aiven console)", required=True)
    parser.add_argument('--port', help="Kafka Port (obtained from Aiven console)", required=True)
    parser.add_argument('--topic-name', help="Topic Name", required=True)
    parser.add_argument('--nr-messages', help="Number of messages to produce (0 for unlimited)", required=True)
    parser.add_argument('--max-waiting-time', help="Max waiting time between messages (0 for none)", required=True)
    args = parser.parse_args()
    p_cert_folder =args.cert_folder
    p_hostname =args.host
    p_port =args.port
    p_topic_name=args.topic_name
    produce_msgs(cert_folder=p_cert_folder,
                 hostname=p_hostname,
                 port=p_port,
                 topic_name=p_topic_name,
                 nr_messages=int(args.nr_messages),
                 max_waiting_time_in_sec=int(args.max_waiting_time)
                 )
    print(args.nr_messages)

if __name__ == "__main__":
    main()
