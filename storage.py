from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from exceptions import InsufficientSupplyError, InsufficientCapacityError, ShopCapacityError


@dataclass
class Storage(ABC):
    """
    Abstract base class for storage objects
    """

    items: dict = field(default_factory=dict)
    capacity: int = None

    @abstractmethod
    def _check_capacity(self, item_name: str, new_capacity: int) -> None:
        """
        Check available storage capacity, raise an error if insufficient
        """
        pass

    def add(self, name: str, quantity: int) -> None:
        """
        Add an item to stored items
        """

        new_capacity = self.capacity - quantity

        # Raise an error if capacity is insufficient
        self._check_capacity(name, new_capacity)

        if name in self.items:
            self.items[name] += quantity
        else:
            self.items[name] = quantity

        self.capacity = new_capacity

    def remove(self, name, quantity):
        """
        Remove an item from stored items
        """
        if name not in self.items or self.items[name] < quantity:
            raise InsufficientSupplyError()

        if self.items[name] == quantity:
            self.items.pop(name)
        else:
            self.items[name] -= quantity

        self.capacity += quantity

    def get_free_space(self):
        return self.capacity

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)

    def __str__(self):
        result = [f'- {v} {k}' for k, v in self.items.items()]
        return '\n'.join(result)


@dataclass
class Warehouse(Storage):

    capacity: int = 100

    def _check_capacity(self, item_name: str, new_capacity: int):
        """
        Check available storage capacity, raise an error if insufficient
        """
        if new_capacity < 0:
            raise InsufficientCapacityError()


@dataclass
class Shop(Storage):

    capacity: int = 20

    def _check_capacity(self, item_name: str, new_capacity: int):
        """
        Check available storage capacity, raise an error if insufficient
        """
        if new_capacity < 0:
            raise InsufficientCapacityError()

        if (item_name not in self.items and
                self.get_unique_items_count() == 5):
            raise ShopCapacityError()
