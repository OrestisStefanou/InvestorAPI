from app.domain.rating import Rating

class CompRating(Rating):
	"""
	Composite Rating: combines the EPS Rating, Relative Strength Rating,
	Industry Group Strength, SMR Rating and Acc/Dis Rating.
	Ranks 1 to 99, with 99 the best.
	"""
	pass