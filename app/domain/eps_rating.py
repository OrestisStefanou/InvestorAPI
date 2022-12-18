from app.domain.rating import Rating

class EpsRating(Rating):
    """
    Earnings Per Share (EPS) rating: compares a stocks last 2 quarters 
    and 3 year EPS growth to all stocks. Ranks 1 to 99, with 99 the best.
    Rating of 90 means it outperformed 90% of all stocks.
    """
    pass
