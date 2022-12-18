class ClosingPrice(object):
	def __init__(self, price: str, change_pct: str):
		self._price = price
		self._change_pct = change_pct
	
	@property
	def price(self) -> str:
		return self._price
	
	@property
	def change_pct(self) -> str:
		return self._change_pct
	