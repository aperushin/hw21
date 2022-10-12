from exceptions import (
    InsufficientCapacityError,
    ShopCapacityError,
    InsufficientSupplyError,
    ParseError
)
from parser import parse_request
from request import Request
from storage import Warehouse, Shop


def main():
    # Create warehouse and shop instances
    warehouse = Warehouse()
    shop = Shop()

    # Fill warehouse with items
    warehouse.add('печеньки', 5)
    warehouse.add('собачки', 6)
    warehouse.add('коробки', 3)

    # Fill shop with items
    shop.add('собачки', 2)
    shop.add('печеньки', 5)

    while True:
        print(f'На складе хранится:\n{warehouse}')
        print(f'В магазине хранится:\n{shop}')

        # Get request from user
        user_input = input('Enter request: ')

        try:
            request_dict = parse_request(user_input)
        except ParseError:
            print('Invalid request')
            print('Example: "Доставить 3 печеньки из склад в магазин"')
            continue

        # Create Request instance
        request = Request(warehouse=warehouse, shop=shop, **request_dict)

        # Execute request
        try:
            request.execute()
        except InsufficientSupplyError:
            print('Нет в достаточном количестве, попробуйте заказать меньше')
        except ShopCapacityError:
            print('В магазин недостаточно места, попробуйте что то другое')
        except InsufficientCapacityError:
            print('Не хватает свободного места')
        else:
            # Ask if user wants to continue, if not, exit the loop
            user_input = input('Another request? Y/N')
            if user_input.lower() == 'n':
                break


if __name__ == '__main__':
    main()
