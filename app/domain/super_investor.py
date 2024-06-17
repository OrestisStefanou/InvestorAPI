import enum
from dataclasses import dataclass

class SuperInvestor(str, enum.Enum):
    Warren_Buffet = 'Warren Buffet'
    Bill_Ackman = 'Bill Ackman'


@dataclass(frozen=True)
class SuperInvestorPortfolioHolding:
    stock: str
    pct_of_portfolio: float
    shares: float
    reported_price: str
    value: str


@dataclass(frozen=True)
class SuperInvestorPortfolioSectorAnalysisEntry:
    sector_name: str
    sector_pct: float


@dataclass(frozen=True)
class SuperInvestorPortfolio:
    super_investor: SuperInvestor
    holdings: list[SuperInvestorPortfolioHolding]
    sector_analysis: list[SuperInvestorPortfolioSectorAnalysisEntry]
