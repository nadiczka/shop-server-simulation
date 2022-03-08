from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from copy import deepcopy
import re


class Product:
    """
    Single product. It has two attributes: name and price.
    :name: should match regex ^[a-zA-Z]{{{n}}}\\d{{2,3}}$, where n is a natural number.
    Otherwise it will not be added to list of products of server.
    :price: price of product
    """
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __hash__(self):
        return hash((self.name, self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


class Server(ABC):
    """
    Abstract class of a single shop server.
    It allows to return max 3 entries (defined as n_max_returned_entries).
    """
    n_max_returned_entries = 3

    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_entries(self, n_letters: Optional[int]) -> List[Product]:
        pass


class ListServer(Server):
    """
    Type of server which stores products in one list.
    :products: List of products.
    """
    def __init__(self, productlist: List[Product]):
        super().__init__()
        self.products = deepcopy(productlist)

    def get_entries(self, n_letters: Optional[int] = None) -> List[Product]:
        if n_letters is None:
            n_letters = 1

        new_list = []

        for el in self.products:
            if re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), el.name):
                new_list.append(el)

        if len(new_list) <= self.n_max_returned_entries:
            second_list = sorted(new_list, key=lambda el: el.price)
            return second_list
        else:
            raise TooManyProductsFoundError


class MapServer(Server):
    """
    Type of server which stores products in one dict.
    :products: Dict of products, where keys are products names and values whole products.
    """
    def __init__(self, productlist: List[Product]):
        super().__init__()
        productdict = dict()
        for el in productlist:
            productdict[el.name] = el
        self.products = deepcopy(productdict)

    def get_entries(self, n_letters: Optional[int] = None) -> List[Product]:
        if n_letters is None:
            n_letters = 1

        new_list = []

        for el in self.products.values():
            if re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), el.name):
                new_list.append(el)

        if len(new_list) <= self.n_max_returned_entries:
            second_list = sorted(new_list, key=lambda el: el.price)
            return second_list
        else:
            raise TooManyProductsFoundError


class Client:
    """
    Single shop. It contains one server with some products.
    Can count total price of products on server which amount of letters is equal n_letters.
    :city_server: Server of a shop.
    """
    def __init__(self, city_centre: Server):
        self.city_server = city_centre

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            count = 0
            store = self.city_server.get_entries(n_letters)
            if len(store) == 0:
                return None
            for el in store:
                count = count + el.price
            return count
        
        except TooManyProductsFoundError:
            return None


class ServerError(Exception):
    pass


class TooManyProductsFoundError(ServerError):
    pass

