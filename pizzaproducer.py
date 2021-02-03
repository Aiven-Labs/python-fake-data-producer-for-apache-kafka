import random
from faker.providers import BaseProvider

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
