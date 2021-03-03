import random
from faker.providers import BaseProvider
from numpy.random import choice

valid_pizza_names = [
    'Margherita',
    'Marinara',
    'Diavola',
    'Mari & Monti',
    'Salami',
    'Peperoni'
]

pizza_names_prob = [0.4, 0.1, 0.3, 0.1, 0.05, 0.05]

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

pizza_shops = [
    'Marios Pizza',
    'Luigis Pizza',
    'Circular Pi Pizzeria',
    'Ill Make You a Pizza You Can''t Refuse',
    'Mammamia Pizza',
    'Its-a me! Mario Pizza!'
]

pizza_cities = [
    {'city': 'Milano',  'lat_min': 45.433, 'lat_max': 45.50849, 'long_min': 9.13, 'long_max': 9.25},
    {'city': 'Sesto San Giovanni', 'lat_min': 45.52360727042132, 'lat_max': 45.54044235328984, 'long_min': 9.223522343848357, 'long_max': 9.259227908655275},
    {'city': 'Cologno Monzese', 'lat_min': 45.525716443539345, 'lat_max': 45.542490781065446, 'long_min': 9.26560056173535, 'long_max': 9.292808888763702},
    {'city': 'Segrate', 'lat_min': 45.483223431508925, 'lat_max': 45.50225519881404, 'long_min': 9.26360914677784, 'long_max': 9.303505107364003},
    {'city': 'Assago', 'lat_min': 45.39789474680953, 'lat_max': 45.410640101954044, 'long_min': 9.120122090055112, 'long_max': 9.145785464760085},
    {'city': 'Buccinasco', 'lat_min': 45.414794205101764, 'lat_max': 45.424373221535184, 'long_min': 9.100054926491662, 'long_max': 9.130739396247609},
    {'city': 'Rho', 'lat_min': 45.52114017009117, 'lat_max': 45.53959917911793, 'long_min': 9.022161913576964, 'long_max': 9.059240769337995},
    {'city': 'Pero', 'lat_min': 45.506552446798494, 'lat_max': 45.51497316996082, 'long_min': 9.07511613141445, 'long_max': 9.093827220664231},
    {'city': 'Cormano', 'lat_min': 45.53691330980241, 'lat_max': 45.54992779862655, 'long_min': 9.15655602433142, 'long_max': 9.178442848912585},
    {'city': 'Cinisello Balsamo', 'lat_min': 45.55104133535123, 'lat_max': 45.56354177735186, 'long_min': 9.203655666178399, 'long_max': 9.244768564117136},
]

#pizza_cities_prob = [0.4, 0.1, 0.03, 0.01, 0.14, 0.07, 0.05, 0.11, 0.04, 0.05]

# Adding a PizzaProvider with 3 methods:
#   * pizza_name to retrieve the name of the basic pizza,
#   * pizza_topping for additional toppings
#   * pizza_shop to retrieve one of the shops available
class PizzaProvider(BaseProvider):
    def pizza_name(self):
        return choice(valid_pizza_names, size=1, replace=False, p=pizza_names_prob)[0]

    def pizza_topping(self):
        return available_pizza_toppings[random.randint(0, len(available_pizza_toppings)-1)]

    def pizza_shop(self):
        return pizza_shops[random.randint(0, len(pizza_shops)-1)]

    def pizza_coord(self, lat_max, lat_min, long_max, long_min, lat_mu, lat_sigma,long_mu, long_sigma):
        return [
            round(random.gauss(mu=lat_mu, sigma=lat_sigma) * (lat_max - lat_min) + lat_min, 2),
            round(random.gauss(mu=long_mu, sigma=long_sigma) * (long_max - long_min) + long_min, 2)
        ]

    def pizza_location(self,cities_distribution, lat_mu, lat_sigma,long_mu, long_sigma):
        sel_city = choice(pizza_cities, size=1, replace=False, p=cities_distribution)[0]
        sel_dot = {'city': sel_city['city'],
                   'coord': self.pizza_coord(lat_max=sel_city['lat_max'],
                                             lat_min=sel_city['lat_min'],
                                             long_max=sel_city['long_max'],
                                             long_min=sel_city['long_min'],
                                             lat_mu=lat_mu,
                                             lat_sigma=lat_sigma,
                                             long_mu=long_mu,
                                             long_sigma=long_sigma,
                                             )
                   }
        return sel_dot

