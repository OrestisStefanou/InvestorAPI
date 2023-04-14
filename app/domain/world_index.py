import enum

class WorldIndex(str, enum.Enum):
    S_P_500 = 'S&P 500'
    Dow_Jones_Ind_Avg = 'Dow Jones Industrial Average'
    Nasdaq_Composite = 'NASDAQ Composite'
    Nyse_Composite = 'NYSE COMPOSITE'
