"""
This file does not do anything special.
It can be use for manual tests of classes dependences or how everything work.
"""

from servers import *

products = [
    Product('P12', 1),
    Product('PP234', 2),
    Product('PP235', 1),
    Product('AC10', 5),
    Product('GH120', 3),
    Product('AMN32', 2),
]

server = ListServer(products)
productsOfLen1InServerList = server.get_entries()
productsOfLen2InServerList = server.get_entries(2)

print(productsOfLen2InServerList)
