from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from exceptions import InsufficientSupplyError, InsufficientCapacityError, ShopCapacityError


@dataclass
class Storage(ABC):
    """
    Abstract base class for storage objects
    """

    @property
    @abstractmethod
    def items(self) -> dict:
        pass

    @property
    @abstractmethod
    def capacity(self) -> int:
        pass

    @abstractmethod
    def remove(self, name, quantity):
        """
        Remove an item from stored items
        """
        pass

    @abstractmethod
    def get_free_space(self) -> int:
        pass

    @abstractmethod
    def get_items(self) -> dict:
        pass

    @abstractmethod
    def get_unique_items_count(self) -> int:
        pass

    @abstractmethod
    def __str__(self):
        pass


@dataclass
class Warehouse(Storage):

    _items: dict = field(default_factory=dict)
    _capacity: int = 20

    @property
    def items(self) -> dict:
        return self._items

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    def add(self, name: str, quantity: int) -> None:
        """
        Add an item to stored items
        """
        if (new_capacity := self.capacity - quantity) < 0:
            raise InsufficientCapacityError()

        if name in self._items:
            self._items[name] += quantity
        else:
            self._items[name] = quantity

        self.capacity = new_capacity

    def remove(self, name, quantity):
        """
        Remove an item from stored items
        """
        if name not in self._items or self._items[name] < quantity:
            raise InsufficientSupplyError()

        if self._items[name] == quantity:
            self._items.pop(name)
        else:
            self._items[name] -= quantity

        self.capacity += quantity

    def get_free_space(self):
        return self.capacity

    def get_items(self):
        return self._items

    def get_unique_items_count(self):
        return len(self._items)

    def __str__(self):
        result = [f'- {v} {k}' for k, v in self._items.items()]
        return '\n'.join(result)


@dataclass
class Shop(Storage):

    _items: dict = field(default_factory=dict)
    _capacity: int = 20

    @property
    def items(self) -> dict:
        return self._items

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    def add(self, name: str, quantity: int) -> None:
        """
        Add an item to stored items
        """
        if (new_capacity := self.capacity - quantity) < 0:
            raise InsufficientCapacityError()

        if (name not in self._items and
                self.get_unique_items_count() == 5):
            raise ShopCapacityError()

        if name in self._items:
            self._items[name] += quantity
        else:
            self._items[name] = quantity

        self.capacity = new_capacity

    def remove(self, name, quantity):
        """
        Remove an item from stored items
        """
        if name not in self._items or self._items[name] < quantity:
            raise InsufficientSupplyError()

        if self._items[name] == quantity:
            self._items.pop(name)
        else:
            self._items[name] -= quantity

        self.capacity += quantity

    def get_free_space(self):
        return self.capacity

    def get_items(self):
        return self._items

    def get_unique_items_count(self):
        return len(self._items)

    def __str__(self):
        result = [f'- {v} {k}' for k, v in self._items.items()]
        return '\n'.join(result)
