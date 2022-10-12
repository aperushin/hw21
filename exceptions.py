class InsufficientCapacityError(Exception):
    pass


class ShopCapacityError(InsufficientCapacityError):
    pass


class InsufficientSupplyError(Exception):
    pass


class ParseError(Exception):
    pass
