from dataclasses import dataclass

@dataclass(frozen=True)
class SymbolAppearancesCount:
    symbol: str
    name: str
    count: int
