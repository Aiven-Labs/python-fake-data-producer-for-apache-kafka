from faker.providers import BaseProvider
import random
import time


class MetricProvider(BaseProvider):
    def hostname(self):
        validIds = [
            "doc",
            "grumpy",
            "sleepy",
            "bashful",
            "happy",
            "sneezy",
            "dopey",
        ]
        return validIds[random.randint(0, len(validIds) - 1)]

    def cpu_id(self):
        validIds = ["cpu1", "cpu2", "cpu3", "cpu4", "cpu5"]
        return validIds[random.randint(0, len(validIds) - 1)]

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
