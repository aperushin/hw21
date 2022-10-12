from exceptions import ParseError
from enums import StorageType


def parse_request(request: str) -> dict:
    try:
        _, amount, product, _, origin, _, destination = request.split()
        amount = int(amount)
        origin = StorageType(origin)
        destination = StorageType(destination)
    except ValueError:
        raise ParseError()

    return {
        'origin': origin,
        'destination': destination,
        'amount': amount,
        'product': product,
    }
