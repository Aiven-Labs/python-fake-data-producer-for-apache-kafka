from faker import Faker
import json
from kafka import KafkaProducer
import time
import random
import argparse
from faker.providers import BaseProvider

MAX_NUMBER_PIZZAS_IN_ORDER = 10
MAX_ADDITIONAL_TOPPINGS_IN_PIZZA = 5



# Creating a Faker instance and seeding to have the same results every time we execute the script
fake = Faker()
Faker.seed(4321)

# Adding a PizzaProvider with 3 methods:
#   * pizza_name to retrieve the name of the basic pizza,
#   * pizza_topping for additional toppings
#   * pizza_shop to retrieve one of the shops available

class PizzaProvider(BaseProvider):
    def pizza_name(self):
        valid_pizza_names = [
            'Margherita',
            'Marinara',
            'Diavola',
            'Mari & Monti',
            'Salami',
            'Peperoni'
        ]
        return valid_pizza_names[random.randint(0, len(valid_pizza_names)-1)]

    def pizza_topping(self):
        available_pizza_toppings = [
            'tomato',
            'mozzarella',
            'blue cheese',
            'salami',
            'green peppers',
            'ham',
            'olives',
            'anchovies',
            'artichokes',
            'olives',
            'garlic',
            'tuna',
            'onion',
            'pineapple',
            'strawberry',
            'banana'
        ]
        return available_pizza_toppings[random.randint(0, len(available_pizza_toppings)-1)]

    def pizza_shop(self):
        pizza_shops = [
            'Marios Pizza',
            'Luigis Pizza',
            'Circular Pi Pizzeria',
            'Ill Make You a Pizza You Can''t Refuse',
            'Mammamia Pizza',
            'Its-a me! Mario Pizza!'
        ]
        return pizza_shops[random.randint(0, len(pizza_shops)-1)]


# Adding the newly created PizzaProvider to the Faker instance
fake.add_provider(PizzaProvider)
print()
# Setting the Kafka Producer


# function produce_msgs starts producing messages with Faker
def produce_msgs(cert_folder="~/kafka-pizza/", hostname='hostname',
                 port='1234', nr_messages=-1, max_waiting_time_in_sec=5):
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
        # Setting the Key as the shop name
        key = fake.pizza_shop()
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
            'id': i,
            'shop': key,
            'name': fake.unique.name(),
            'phoneNumber': fake.unique.phone_number(),
            'address': fake.address(),
            'pizzas': pizzas
        }

        print("Sending: {}".format(message))
        # sending the message to Kafka
        producer.send("pizza-orders",
                      key={'shop': key},
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
    parser.add_argument('--nr-messages', help="Number of messages to produce (0 for unlimited)", required=True)
    parser.add_argument('--max_waiting_time', help="Max waiting time between messages (0 for none)", required=True)
    args = parser.parse_args()
    p_cert_folder =args.cert_folder
    p_hostname =args.host
    p_port =args.port
    produce_msgs(cert_folder=p_cert_folder,
                 hostname=p_hostname,
                 port=p_port,
                 nr_messages=int(args.nr_messages),
                 max_waiting_time_in_sec=int(args.max_waiting_time)
                 )
    print(args.nr_messages)

if __name__ == "__main__":
    main()
