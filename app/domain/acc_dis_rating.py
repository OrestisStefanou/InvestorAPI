class AccDisRating(object):
	"""
	Shows if a stock is under accumulation (buying) or 
	distribution (selling) in the last 3 months.
	A=buying, E=selling
	"""
	def __init__(self, rating: str):
		self._rating = rating
	
	@property
	def rating(self) -> str:
		return self._rating
