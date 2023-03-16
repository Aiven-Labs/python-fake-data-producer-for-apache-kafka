import time
from faker.providers import BaseProvider
import json
import os
import sys


nr_item = 0
base_timestamp = int(time.time() * 1000)
f = open(os.path.join(sys.path[0], "data_rolling.json"))
data = json.load(f)

# Adding a RollingProvider with 1 method:
#   * getcode to retrieve the username


class RollingProvider(BaseProvider):
    def produce_msg(self):

        global nr_item
        global base_timestamp
        item = data[nr_item]

        # message composition
        message = {
            "val": item["value"],
            "ts": base_timestamp + int(item["timestamp"]),
        }
        key = {"ts": base_timestamp + int(item["timestamp"])}
        if nr_item == 1732:
            print("Waiting next iteration")
            time.sleep(30)
            nr_item = 0
            base_timestamp = int(time.time() * 1000)
        else:
            nr_item = nr_item + 1
        return message, key
