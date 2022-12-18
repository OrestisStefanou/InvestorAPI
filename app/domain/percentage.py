from typing import Optional, Union

class Percentage:
    def __init__(self, percentage: Union[str, float, int]) -> None:
        try:
            float_pct = float(percentage)
        except Exception:
            float_pct = None
        
        self._percentage = float_pct
    
    @property
    def value(self) -> Optional[float]:
        return self._percentage