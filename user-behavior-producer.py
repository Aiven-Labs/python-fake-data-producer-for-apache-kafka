import json
from kafka import KafkaProducer
from faker import Faker
from faker.providers import BaseProvider
import random
import time
import datetime

FAKER_SEED = 1111


class UserBehaviorProvider(BaseProvider):

    def user_id(self):
        validIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return validIds[random.randint(0, len(validIds) - 1)]

    def item_id(self):
        validIds = [21, 22, 23, 24, 25, 26, 27, 28, 29]
        return validIds[random.randint(0, len(validIds) - 1)]

    def behavior(self):
        behaviorNames = ['view', 'cart', 'buy']
        return behaviorNames[random.randint(0, len(behaviorNames) - 1)]
        
    def group_name(self):
        groupNames = ['A', 'B']
        return groupNames[random.randint(0, len(groupNames) - 1)]

    def view_id(self):
        viewIds = [111, 222, 555]
        return viewIds[random.randint(0, len(viewIds) - 1)]


def produce_msgs(cert_folder="~/kafka-behavior/",
                 hostname='hostname',
                 port='1234',
                 topic_name='behavior',
                 nr_messages=-1,
                 max_waiting_time_in_sec=5):
    fake = Faker()
    Faker.seed(FAKER_SEED)
    fake.add_provider(UserBehaviorProvider)             
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
    	ts = time.time() - random.randint(-5, 5)
        b = fake.behavior()
        view_id = None
        if b == 'view':
            view_id = fake.view_id()
        message = {
            'user_id': fake.user_id(),
            'item_id': fake.item_id(),
            'behavior': b,
            'view_id': view_id,
            'group_name': fake.group_name(),
            'occurred_at': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        }
        producer.send(topic_name, key="all_users", value=message)
        print(message)
        sleep_time = random.randint(0, max_waiting_time_in_sec * 5) / 5
        print("Sleeping for..." + str(sleep_time) + 's')
        time.sleep(sleep_time)

        # Force flushing of all messages
        if (i % 5) == 0:
            producer.flush()
        i = i + 1
        
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
