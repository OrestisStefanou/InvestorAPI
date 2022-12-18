class Rating(object):
    def __init__(self, rating: int) -> None:
        if rating < 1 or rating > 99:
            raise ValueError("EPS rating can take values between 1 and 99")
        
        self._rating = rating
    
    @property
    def rating(self) -> int:
        return self._rating