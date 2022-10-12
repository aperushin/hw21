import pytest
from parser import parse_request
from enums import StorageType
from exceptions import ParseError


class TestParser:
    def test_structure(self):
        result = parse_request('Доставить 3 печеньки из склад в магазин')
        assert isinstance(result.get('origin'), StorageType)
        assert isinstance(result.get('destination'), StorageType)
        assert isinstance(result.get('amount'), int)
        assert isinstance(result.get('product'), str)

    def test_invalid_length(self):
        with pytest.raises(ParseError):
            parse_request('Доставить 3 печеньки из склад в')

    def test_invalid_origin(self):
        with pytest.raises(ParseError):
            parse_request('Доставить 3 печеньки из aaaaa в магазин')

    def test_invalid_destination(self):
        with pytest.raises(ParseError):
            parse_request('Доставить 3 печеньки из магазин в аааа')

    def test_invalid_amount(self):
        with pytest.raises(ParseError):
            parse_request('Доставить три печеньки из склад в магазин')
