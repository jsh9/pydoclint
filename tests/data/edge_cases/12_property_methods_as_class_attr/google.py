class House:
    """
    A house

    Attributes:
        price (float): House price
        _privateProperty (str): A private property

    Args:
        price_0 (float): House price
    """

    def __init__(self, price_0: float) -> None:
        self._price = price_0

    @property
    def price(self) -> float:
        """The house price"""
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price > 0 and isinstance(new_price, float):
            self._price = new_price
        else:
            print('Please enter a valid price')

    @price.deleter
    def price(self):
        del self._price

    @property
    def _privateProperty(self) -> str:
        return 'secret'
