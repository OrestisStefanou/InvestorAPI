class AlphaVantageRequestError(Exception):
	pass

class AlphaVantageParsingError(Exception):
	"""
	Raised when something goes wrong during
	data scraping from yahoo finance 
	"""
	pass