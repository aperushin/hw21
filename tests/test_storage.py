import pytest
from storage import Warehouse, Shop
from exceptions import InsufficientCapacityError, InsufficientSupplyError


class TestStore:
    @pytest.fixture(autouse=True)
    def store_empty(self):
        return Warehouse()
    
    @pytest.fixture(autouse=True)
    def store_filled(self):
        store = Warehouse()
        store._items = {'test': 1}
        store.capacity = Warehouse._capacity - 1
        return store
        
    def test_add_item(self, store_empty):
        store_empty.add('test', 1)
        assert store_empty.items == {'test': 1}
    
    def test_capacity_decrease(self, store_empty):
        store_empty.add('test', 1)
        assert store_empty.capacity == Warehouse._capacity - 1
        
    def test_add_insufficient(self, store_empty):
        with pytest.raises(InsufficientCapacityError):
            store_empty.add('test', Warehouse._capacity + 1)
        
    def test_remove(self, store_filled):
        store_filled.remove('test', 1)
        assert store_filled.items == {}
        
    def test_remove_no_item(self, store_empty):
        with pytest.raises(InsufficientSupplyError):
            store_empty.remove('test', 1)

    def test_remove_not_enough_item(self, store_filled):
        with pytest.raises(InsufficientSupplyError):
            store_filled.remove('test', 2)
            
    def test_capacity_increase(self, store_filled):
        store_filled.remove('test', 1)
        assert store_filled.capacity == Warehouse._capacity


class TestShop:
    @pytest.fixture(autouse=True)
    def shop_empty(self):
        return Shop()

    @pytest.fixture(autouse=True)
    def shop_filled(self):
        shop = Shop()
        shop._items = {
            'test1': 1,
            'test2': 1,
            'test3': 1,
            'test4': 1,
            'test5': 1
        }
        shop._capacity -= 5
        return shop

    def test_add_too_many_unique(self, shop_filled):
        with pytest.raises(InsufficientCapacityError):
            shop_filled.add('test6', 1)

    def test_add_at_unique_limit(self, shop_filled):
        shop_filled.add('test1', 1)
        assert shop_filled.items['test1'] == 2

    def test_add_insufficient(self, shop_empty):
        with pytest.raises(InsufficientCapacityError):
            shop_empty.add('test', Shop._capacity + 1)
