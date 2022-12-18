from typing import Optional, Union

class Price:
    def __init__(self, price: Union[str, float, int]) -> None:
        try:
            float_price = float(price)
        except Exception:
            float_price = None
        
        self._price = float_price
    
    @property
    def value(self) -> Optional[float]:
        return self._price
