from enums import StorageType
from storage import Shop, Warehouse


class Request:
    def __init__(
            self,
            shop: Shop,
            warehouse: Warehouse,
            origin: StorageType,
            destination: StorageType,
            amount: int,
            product: str):
        self.amount = amount
        self.product = product

        direction_map = {
            StorageType.SHOP: shop,
            StorageType.WAREHOUSE: warehouse
        }
        self.origin = direction_map.get(origin)
        self.destination = direction_map.get(destination)
        self.origin_type = origin
        self.destination_type = destination

    def execute(self):
        self.origin.remove(self.product, self.amount)
        try:
            self.destination.add(self.product, self.amount)
        except Exception as e:
            # Rollback
            self.origin.add(self.product, self.amount)
            raise e
