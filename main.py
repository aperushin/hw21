from dataclasses import dataclass, field

from exceptions import InsufficientCapacity, InsufficientSupply, ParseError


@dataclass
class Storage:
    items: dict = field(default_factory=dict)
    capacity: int = None

    def add(self, name: str, quantity: int) -> None:
        if (new_capacity := self.capacity - quantity) < 0:
            raise InsufficientCapacity()

        if name in self.items:
            self.items[name] += quantity
        else:
            self.items[name] = quantity

        self.capacity = new_capacity

    def remove(self, name, quantity):
        if name not in self.items or self.items[name] < quantity:
            raise InsufficientSupply()

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
class Store(Storage):

    capacity: int = 100


@dataclass
class Shop(Storage):

    capacity: int = 20

    def add(self, name: str, quantity: int) -> None:
        if ((new_capacity := self.capacity - quantity) < 0 or
                self.get_unique_items_count() == 5):
            raise InsufficientCapacity()

        if name in self.items:
            self.items[name] += quantity
        else:
            self.items[name] = quantity

        self.capacity = new_capacity


class Request:
    def __init__(
            self,
            shop: Shop,
            store: Store,
            origin: str,
            destination: str,
            amount: int,
            product: str):
        self.amount = amount
        self.product = product

        direction_map = {'магазин': shop, 'склад': store}
        self.origin = direction_map.get(origin)
        self.destination = direction_map.get(destination)

    def execute(self):
        self.origin.remove(self.product, self.amount)
        self.destination.add(self.product, self.amount)


def parse_request(request: str) -> dict:
    try:
        _, amount, product, _, origin, _, destination = request.split()
        amount = int(amount)
    except ValueError:
        raise ParseError()

    return {
        'origin': origin,
        'destination': destination,
        'amount': amount,
        'product': product,
    }


def main():
    store = Store()
    shop = Shop()

    store.add('печеньки', 5)
    store.add('собачки', 6)
    store.add('коробки', 3)

    shop.add('собачки', 2)
    shop.add('печеньки', 5)

    while True:
        print(f'На складе хранится:\n{store}')
        print(f'В магазине хранится:\n{shop}')

        user_input = input('Enter request: ')

        try:
            request_dict = parse_request(user_input)
        except ParseError:
            print('Invalid request')
            print('Example: "Доставить 3 печеньки из склад в магазин"')
            continue

        request = Request(store=store, shop=shop, **request_dict)
        try:
            request.execute()
        except InsufficientSupply:
            print('Нет в достаточном количестве, попробуйте заказать меньше')
            continue
        except InsufficientCapacity:
            print('Не хватает свободного места')
            continue





if __name__ == '__main__':
    main()
