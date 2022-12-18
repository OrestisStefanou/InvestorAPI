class IbdRequestError(Exception):
	pass

class IbdScrapeError(Exception):
	"""
	Raised when something goes wrong during
	data scraping from ibd 
	"""
	pass