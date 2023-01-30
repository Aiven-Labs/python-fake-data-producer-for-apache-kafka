from faker.providers import BaseProvider
import random
import time

NUMBER_HOSTS = 100000
NUMBER_CPU = 30


class MetricAdvancedProvider(BaseProvider):
    def hostname(self):
        return "hostname" + str(random.randint(0, NUMBER_HOSTS))

    def cpu_id(self):

        return "cpu" + str(random.randint(0, NUMBER_CPU))

    def usage(self):
        return random.random() * 30 + 70

    def produce_msg(self):
        hostname = self.hostname()
        ts = time.time()
        message = {
            "hostname": hostname,
            "cpu": self.cpu_id(),
            "usage": self.usage(),
            "occurred_at": int(ts * 1000),
        }
        key = {"hostname": hostname}
        return message, key
