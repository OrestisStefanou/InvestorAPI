class SmrRating(object):
	"""
    Combines sales, profit margins and return on equity 
    into an A to E rating
	"""
	def __init__(self, rating: str):
		self._rating = rating
	
	@property
	def rating(self) -> str:
		return self._rating
