class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id

class DuplicateProductError(Exception):
    def __init__(self, name: str):
        self.name = name
