class YFinanceRequestError(Exception):
	pass

class YFinanceScrapeError(Exception):
	"""
	Raised when something goes wrong during
	data scraping from yahoo finance 
	"""
	pass