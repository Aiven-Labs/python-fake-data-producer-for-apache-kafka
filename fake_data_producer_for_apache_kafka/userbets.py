import random
import time
from faker.providers import BaseProvider

MIN_AMOUNT = 2  # Min betting amount
MAX_AMOUNT = 1000  # Max betting amount

ALPHA = 50

# Adding a UserBets with 3 methods:
#   * username to retrieve the username,
#   * bet_amount to retrieve the amount
#   * betting_channel_event to retrieve event and channel


class UserBetsProvider(BaseProvider):
    def username(self):
        valid_usernames = [
            "nopineappleonpizza",
            "catanzaro99",
            "thedoctor",
            "bettingexpert01",
            "losingmoney66",
            "manutd007",
            "manutd009",
            "citylife1",
            "lysa_X",
            "aiventest",
        ]
        return random.choice(valid_usernames)

    def bet_amount(self):
        # return int(random.triangular(MIN_AMOUNT, MID_AMOUNT, MAX_AMOUNT))
        return (
            int((random.paretovariate(ALPHA) - 1) * (MAX_AMOUNT - MIN_AMOUNT))
            + 1
        )

    def bet_category_event(self):
        valid_events = [
            {
                "category": "Sport",
                "subcategory": "Football",
                "event": "ManUTD vs Chelsea",
            },
            {
                "category": "Sport",
                "subcategory": "Box",
                "event": "Chicken Legs vs Power Kick",
            },
            {
                "category": "Sport",
                "subcategory": "Curling",
                "event": "Italy vs England",
            },
            {
                "category": "Sport",
                "subcategory": "Netball",
                "event": "Sydney vs Camberra",
            },
            {
                "category": "Lottery",
                "subcategory": "Bingo",
                "event": "Uk Bingo",
            },
            {
                "category": "Lottery",
                "subcategory": "WinForLife",
                "event": "Win For Life America",
            },
            {
                "category": "Event",
                "subcategory": "Music",
                "event": "Rick Astley #1 in World Charts",
            },
            {
                "category": "Event",
                "subcategory": "Politics",
                "event": "Mickey Mouse new Italian President",
            },
            {
                "category": "Event",
                "subcategory": "Celebrities",
                "event": "Donald Duck and Marge Simpson Wedding",
            },
        ]
        return random.choice(valid_events)

    def produce_msg(self):
        username = self.username()
        bet_amount = self.bet_amount()
        bet_event = self.bet_category_event()

        # message composition
        message = {
            "username": username,
            "event": {
                "category": bet_event["category"],
                "subcategory": bet_event["subcategory"],
                "name": bet_event["event"],
            },
            "amount": bet_amount,
            "timestap": int(time.time() * 1000),
        }
        key = {"event": bet_event["event"]}
        return message, key
