import pytest
from main import Store, Shop
from exceptions import InsufficientCapacity, InsufficientSupply


class TestStore:
    @pytest.fixture(autouse=True)
    def store_empty(self):
        return Store()
    
    @pytest.fixture(autouse=True)
    def store_filled(self, ):
        store = Store()
        store.items = {'test': 1}
        store.capacity = Store.capacity - 1
        return store
        
    def test_add_item(self, store_empty):
        store_empty.add('test', 1)
        assert store_empty.items == {'test': 1}
    
    def test_capacity_decrease(self, store_empty):
        store_empty.add('test', 1)
        assert store_empty.capacity == Store.capacity - 1
        
    def test_add_insufficient(self, store_empty):
        with pytest.raises(InsufficientCapacity):
            store_empty.add('test', Store.capacity + 1)
        
    def test_remove(self, store_filled):
        store_filled.remove('test', 1)
        assert store_filled.items == {}
        
    def test_remove_no_item(self, store_empty):
        with pytest.raises(InsufficientSupply):
            store_empty.remove('test', 1)

    def test_remove_not_enough_item(self, store_filled):
        with pytest.raises(InsufficientSupply):
            store_filled.remove('test', 2)
            
    def test_capacity_increase(self, store_filled):
        store_filled.remove('test', 1)
        assert store_filled.capacity == Store.capacity


class TestShop:
    @pytest.fixture(autouse=True)
    def shop_empty(self):
        return Shop()

    def test_add_too_many_unique(self, shop_empty):
        shop_empty.items = {
            'test1': 1,
            'test2': 1,
            'test3': 1,
            'test4': 1,
            'test5': 1
        }

        with pytest.raises(InsufficientCapacity):
            shop_empty.add('test6', 1)

    def test_add_insufficient(self, shop_empty):
        with pytest.raises(InsufficientCapacity):
            shop_empty.add('test', Shop.capacity + 1)
