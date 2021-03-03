from faker import Faker
import json
from kafka import KafkaProducer
import time
import random
import argparse
from pizzaproducer import PizzaProvider
import threading
import numpy as np, numpy.random
from multiprocessing import Process, Value
#from asyncio import LifoQueue
from flask import Flask





MAX_NUMBER_PIZZAS_IN_ORDER = 5
MAX_ADDITIONAL_TOPPINGS_IN_PIZZA = 5

app = Flask(__name__)
flask_app = Flask(__name__)
task_started = False
#q = LifoQueue(maxsize=0)
val = Value('d',0)
p = False
nr_msg_sent = 0
p_cert_folder=""
p_hostname=""
p_port=""
p_topic_name=""
p_nr_threads=1
p_nr_messages=-1
p_max_waiting_time=0


key_schema = {
    "type": "struct",
    "fields": [{
        "type": "string",
        "optional": False,
        "field": "id"
    }],
    "optional": False,
    "name": "foobar"
}

msg_schema = {
    "type": "struct",
    "fields": [{
        "type": "int32",
        "optional": False,
        "field": "id"
    }, {
        "type": "string",
        "optional": False,
        "field": "shop"
    }, {
        "type": "string",
        "optional": False,
        "field": "name"
    }, {
        "type": "string",
        "optional": False,
        "field": "phoneNumber"
    }, {
        "type": "string",
        "optional": False,
        "field": "address"
    },{
        "type": "string",
        "optional": False,
        "field": "city"
    },{
        "type": "float",
        "optional": False,
        "field": "lat"
    },{
        "type": "float",
        "optional": False,
        "field": "long"
    },{
        "type": "int64",
        "optional": False,
        "name": "org.apache.kafka.connect.data.Timestamp",
        "field": "order_time"
    },
    {
        "type": "float",
        "optional": False,
        "field": "total_amount"
    },
    {
        "type": "string",
        "optional": False,
        "field": "card_number"
    },
    {
        "optional": False,
        "field": "pizzas",
        "type": "array",
        "items":
            {
                "type": "struct",
                "optional": False,
                "fields": [
                    {
                        "type": "string",
                        "optional": False,
                        "field": "pizzaName",
                    }
                    ,{
                        "type": "array",
                        "optional": True,
                        "field": "additionalToppings",
                        "items": {"type": "string"}
                    }
                ]
            }
    }
    ],
    "optional": False,
    "name": "foobar"
}



# Creating a Faker instance and seeding to have the same results every time we execute the script
fake = Faker('it_IT')
Faker.seed(4321)



# Adding the newly created PizzaProvider to the Faker instance
fake.add_provider(PizzaProvider)

# creating function to generate the pizza Order
def produce_pizza_order (ordercount = 1):
    shop = fake.pizza_shop()
    # Each Order can have 1-10 pizzas in it
    pizzas = []
    nr_pizzas = random.randint(1, MAX_NUMBER_PIZZAS_IN_ORDER)
    for pizza in range(nr_pizzas):
        # Each Pizza can have 0-5 additional toppings on it
        toppings = []
        for topping in range(random.randint(0, MAX_ADDITIONAL_TOPPINGS_IN_PIZZA)):
            toppings.append(fake.pizza_topping())
        pizzas.append({
            'pizzaName': fake.pizza_name(),
            'additionalToppings': toppings
        })
    lat_mu = 0.5
    lat_sigma = 0.2
    long_mu = 0.5
    long_sigma = 0.2
    cities_distribution = np.random.dirichlet(np.ones(9)/100,size=1)[0]
    milan_distribution = random.random() /100 +0.2
    cities_distribution = cities_distribution * (1-milan_distribution)
    cities_distribution = np.insert(cities_distribution,0,milan_distribution)
    if ordercount % 2000 == 0:
        lat_mu = random.random() * 5000 - 14.5
        lat_sigma = random.random() / 100 + 0.001
        long_mu = random.random() * 5000 - 14.5
        long_sigma = random.random() / 100 + 0.001
    if ordercount % 10000 == 0:
        cities_distribution = np.random.dirichlet(np.ones(9)/100,size=1)[0]
        #milan_distribution = random.random() /100 +0.2
        cities_distribution = cities_distribution * (1-milan_distribution)
        cities_distribution = np.insert(cities_distribution,0,milan_distribution)
        print(milan_distribution)
    city_lat_long = fake.pizza_location(cities_distribution, lat_mu, lat_sigma, long_mu, long_sigma)
    # message composition
    msg_payload = {
        'id': ordercount,
        'shop': shop,
        'name': fake.name(),
        'phoneNumber': fake.phone_number(),
        'address': fake.street_address(),
        'city': city_lat_long['city'],
        'lat': city_lat_long['coord'][0],
        'long': city_lat_long['coord'][1],
        'order_time': int(time.time() * 1000),
        'total_amount': (random.random()+0.5) * nr_pizzas * 10,
        'card_number': fake.credit_card_number(),
        'pizzas': pizzas
    }
    #print(int(time.time() * 1000))
    key_payload = {'id': shop + str(ordercount)}

    message = {
        "schema": msg_schema,
        "payload": msg_payload
    }
    key = {
        "schema": key_schema,
        "payload": key_payload
    }
    return message, key
    #return msg_payload,key_payload

# function produce_msgs starts producing messages with Faker
def produce_msgs(
        cert_folder="~/kafka-pizza/",
        hostname='hostname',
        port='1234',
        topic_name='pizza-orders',
        nr_messages=-1,
        max_waiting_time_in_sec=5,
        thread_nr = 1,
        val = ""):

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
    global nr_msg_sent
    while i < nr_messages:
        message, key = produce_pizza_order(i)

        #print("Sending: {}".format(message))
        if (i % 10000) == 0:
            print(str(thread_nr) +":"+str(i))
        # sending the message to Kafka
        producer.send(topic_name,
                      key=key,
                      value=message)
        # Sleeping time
        #sleep_time = random.randint(0, max_waiting_time_in_sec * 10)/10
        #print("Sleeping for..."+str(sleep_time)+'s')
        #time.sleep(sleep_time)
        #q.put(i,False)
        val.value=int(i)
        # Force flushing of all messages
        if (i % 1000) == 0:
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
    parser.add_argument('--nr-threads', help="Number of threads (1 by default)", required=True)
    parser.add_argument('--flask-port', help="Flask Port", required=True)
    args = parser.parse_args()
    global p_cert_folder, p_hostname, p_port, p_topic_name, p_nr_threads, p_nr_messages, p_max_waiting_time
    p_cert_folder =args.cert_folder
    p_hostname =args.host
    p_port =args.port
    p_topic_name=args.topic_name
    p_nr_threads=int(args.nr_threads)
    p_nr_messages=args.nr_messages
    p_max_waiting_time=args.max_waiting_time
    p_flask_port=int(args.flask_port)
    #health_check()
    app.run(host='0.0.0.0',port=p_flask_port, debug=True)



def start_background_process():
    val = Value('d',0)

    process = Process(target=produce_msgs, args=(
                                        p_cert_folder,
                                        p_hostname,
                                        p_port,
                                        p_topic_name,
                                        int(int(p_nr_messages)/p_nr_threads),
                                        int(p_max_waiting_time),
                                        1,
                                        val
                                    )
                                  )
    process.start()
    return val, process



@app.route('/')
def health_check():
    global val, p, task_started, nr_msg_sent
    print(task_started)
    if not task_started:
        val, p = start_background_process()
        task_started = True
    pizzas_ordered = int(val.value)
    return '<table><tr><td><img src="https://ftisiot.net/images/2021/pizza-chef.png"></td><td><font size=20> Pizzas ordered: <b>{}</b></td></tr></table>'.format(pizzas_ordered)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
