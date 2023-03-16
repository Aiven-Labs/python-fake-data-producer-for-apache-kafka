import random
import time
from faker.providers import BaseProvider

# Adding a PizzaProvider with 3 methods:
#   * pizza_name to retrieve the name of the basic pizza,
#   * pizza_topping for additional toppings
#   * pizza_shop to retrieve one of the shops available


class PizzaProvider(BaseProvider):
    def pizza_name(self):
        valid_pizza_names = [
            "Margherita",
            "Marinara",
            "Diavola",
            "Mari & Monti",
            "Salami",
            "Peperoni",
        ]
        return random.choice(valid_pizza_names)

    def pizza_topping(self):
        available_pizza_toppings = [
            "🍅 tomato",
            "🧀 blue cheese",
            "🥚 egg",
            "🫑 green peppers",
            "🌶️ hot pepper",
            "🥓 bacon",
            "🫒 olives",
            "🧄 garlic",
            "🐟 tuna",
            "🧅 onion",
            "🍍 pineapple",
            "🍓 strawberry",
            "🍌 banana",
        ]
        return random.choice(available_pizza_toppings)

    def pizza_shop(self):
        pizza_shops = [
            "Marios Pizza",
            "Luigis Pizza",
            "Circular Pi Pizzeria",
            "Ill Make You a Pizza You Can" "t Refuse",
            "Mammamia Pizza",
            "Its-a me! Mario Pizza!",
        ]
        return random.choice(pizza_shops)

    def produce_msg(
        self,
        FakerInstance,
        ordercount=1,
        max_pizzas_in_order=5,
        max_toppings_in_pizza=3,
    ):
        shop = FakerInstance.pizza_shop()
        # Each Order can have 1-10 pizzas in it
        pizzas = []
        for pizza in range(random.randint(1, max_pizzas_in_order)):
            # Each Pizza can have 0-5 additional toppings on it
            toppings = []
            for topping in range(random.randint(0, max_toppings_in_pizza)):
                toppings.append(FakerInstance.pizza_topping())
            pizzas.append(
                {
                    "pizzaName": FakerInstance.pizza_name(),
                    "additionalToppings": toppings,
                }
            )
        # message composition
        message = {
            "id": ordercount,
            "shop": shop,
            "name": FakerInstance.unique.name(),
            "phoneNumber": FakerInstance.unique.phone_number(),
            "address": FakerInstance.address(),
            "pizzas": pizzas,
            "timestamp": int(time.time() * 1000),
        }
        key = {"shop": shop}
        return message, key
