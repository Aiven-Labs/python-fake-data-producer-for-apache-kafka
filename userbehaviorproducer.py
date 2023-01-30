from faker.providers import BaseProvider
import random
import time
import datetime


class UserBehaviorProvider(BaseProvider):
    def user_id(self):
        userIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return random.choice(userIds)

    def item_id(self):
        validIds = [21, 22, 23, 24, 25, 26, 27, 28, 29]
        return random.choice(validIds)

    def behavior(self):
        behaviorNames = ["view", "cart", "buy"]
        return random.choice(behaviorNames)

    def group_name(self):
        groupNames = ["A", "B"]
        return random.choice(groupNames)

    def view_id(self):
        viewIds = [111, 222, 555]
        return random.choice(viewIds)

    def produce_msg(self):
        ts = time.time() - random.randint(-5, 5)
        b = self.behavior()
        view_id = None
        if b == "view":
            view_id = self.view_id()
        message = {
            "user_id": self.user_id(),
            "item_id": self.item_id(),
            "behavior": b,
            "view_id": view_id,
            "group_name": self.group_name(),
            "occurred_at": datetime.datetime.fromtimestamp(ts).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        key = {"user": "all_users"}
        return message, key
