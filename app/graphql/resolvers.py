from typing import List, Dict, Union

from app.services.tech_leaders_stocks import TechLeadersStocksService
from app.services.top_comp_stocks import TopCompositeStocksService
from app.services.bottom_comp_stocks import BottomCompositeStocksService
from app.services.stocks_with_sector import StocksWithSectorService
from app.services.dividend_leaders import DividendLeadersService
from app.services.top_low_priced_stocks import TopLowPricedStocksService
from app.services.reit_leaders import ReitLeadersService
from app.services.utility_leaders import UtilityLeadersService
from app.services.leaders_index import SmallMidCapLeadersIndexService, LargeMidCapLeadersIndexService
from app.services.aggregate_service import AggregateService
import app.graphql.schema as s
from app.graphql.serializers import(
    serialize_composite_stock,
    serialize_stock_leader,
    serialize_stock_with_sector,
    serialize_tech_leader_stock,
    serialize_low_priced_stock,
    serialize_leaders_index_stock,
    serialize_stock_appearances_count
)


_collection_to_service: Dict[s.Collection, AggregateService] = {
    s.Collection.TopCompositeStocks: TopCompositeStocksService,
    s.Collection.BottomCompositeStocks: BottomCompositeStocksService,
    s.Collection.DividendLeaders: DividendLeadersService,
    s.Collection.ReitLeaders: ReitLeadersService,
    s.Collection.UtilityLeaders: UtilityLeadersService,
    s.Collection.TechLeaders: TechLeadersStocksService,
    s.Collection.LargeMidCapLeadersIndex: LargeMidCapLeadersIndexService,
    s.Collection.SmallMidCapLeadersIndex: SmallMidCapLeadersIndexService
}

_collection_to_serializer = {
    s.Collection.TopCompositeStocks: serialize_composite_stock,
    s.Collection.BottomCompositeStocks: serialize_composite_stock,
    s.Collection.DividendLeaders: serialize_stock_leader,
    s.Collection.ReitLeaders: serialize_stock_leader,
    s.Collection.UtilityLeaders: serialize_stock_leader,
    s.Collection.TechLeaders: serialize_tech_leader_stock,
    s.Collection.LargeMidCapLeadersIndex: serialize_leaders_index_stock,
    s.Collection.SmallMidCapLeadersIndex: serialize_leaders_index_stock
}


async def top_composite_stocks_resolver(day: int, month: int, year: int, limit: int = 200) -> List[s.CompositeStock]:
    top_comp_stocks = await TopCompositeStocksService.get_top_200_comp_stocks_for_date(day, month, year)
    return [
        serialize_composite_stock(comp_stock)
        for comp_stock in top_comp_stocks[:limit]
    ]


async def bottom_composite_stocks_resolver(day: int, month: int, year: int, limit: int = 200) -> List[s.CompositeStock]:
    bottom_comp_stocks = await BottomCompositeStocksService.get_bottom_200_comp_stocks_for_date(day, month, year)
    return [
        serialize_composite_stock(comp_stock)
        for comp_stock in bottom_comp_stocks[:limit]
    ]


async def reit_leaders_resolver(day: int, month: int, year: int) -> List[s.StockLeader]:
    reit_leaders = await ReitLeadersService.get_reit_leaders_for_date(
        day, month, year
    )

    return [
        serialize_stock_leader(reit_leader)
        for reit_leader in reit_leaders
    ]
 

async def stocks_with_sector_resolver(day: int, month: int, year: int, sector: str = None) -> List[s.SectorStock]:
    stocks_with_sector = await StocksWithSectorService.get_stocks_with_sector_for_date(
        day, month, year, sector
    )

    return [
        serialize_stock_with_sector(stock)
        for stock in stocks_with_sector
    ]


async def sectors_performance_resolver(day: int, month: int, year: int) -> List[s.SectorPerformance]:
    sectors = StocksWithSectorService.get_sectors_performance(day, month, year)

    return [
        s.SectorPerformance(
            sector_name=sector.sector_name,
            daily_price_change_pct=sector.daily_price_change_pct.value,
            start_of_year_price_change_pct=sector.start_of_year_price_change_pct.value
        )
        for sector in sectors

    ]


async def tech_leaders_stocks_resolver(day: int, month: int, year: int) -> List[s.TechLeaderStock]:
    tech_leaders_stocks = await TechLeadersStocksService.get_tech_leaders_stocks_for_date(
        day, month, year
    )

    return [
        serialize_tech_leader_stock(stock)
        for stock in tech_leaders_stocks
    ]


async def top_low_priced_stocks_resolver(day: int, month: int, year: int) -> List[s.LowPricedStock]:
    low_priced_stocks = await TopLowPricedStocksService.get_top_low_priced_stocks_for_date(
        day, month, year
    )
  
    return [
        serialize_low_priced_stock(stock)
        for stock in low_priced_stocks
    ]


async def dividend_leaders_resolver(day: int, month: int, year: int) -> List[s.StockLeader]:
    dividend_leaders = await DividendLeadersService.get_dividend_leaders_for_date(
        day, month, year
    )

    return [
        serialize_stock_leader(dividend_leader)
        for dividend_leader in dividend_leaders
    ]


async def utility_leaders_resolver(day: int, month: int, year: int) -> List[s.StockLeader]:
    utility_leaders = await UtilityLeadersService.get_utility_leaders_for_date(
        day, month, year
    )

    return [
        serialize_stock_leader(utility_leader)
        for utility_leader in utility_leaders
    ]


async def small_mid_cap_leaders_index_resolver(day: int, month: int, year: int) -> List[s.LeadersIndexStock]:
    small_mid_cap_leaders_index = await SmallMidCapLeadersIndexService.get_leaders_index_for_date(
        day, month, year
    )

    return [
        serialize_leaders_index_stock(stock)
        for stock in small_mid_cap_leaders_index
    ]


async def large_mid_cap_leaders_index_resolver(day: int, month: int, year: int) -> List[s.LeadersIndexStock]:
    large_mid_cap_leaders_index = await LargeMidCapLeadersIndexService.get_leaders_index_for_date(
        day, month, year
    )

    return [
        serialize_leaders_index_stock(stock)
        for stock in large_mid_cap_leaders_index
    ]


async def appereances_count_per_stock_in_collection_resolver(
    collection: s.Collection,
    min_count: int = 1,
    limit: int = 100
) -> List[s.StockAppereancesCount]:    
    service = _collection_to_service.get(collection)
    
    appereances_count = service.get_appereances_count_for_each_symbol(
        limit=limit,
        min_count=min_count
    )

    return [
        serialize_stock_appearances_count(appearance)
        for appearance in appereances_count
    ]


async def search_symbol_in_collection_resolver(
    symbol: str,
    collection: s.Collection
) -> List[Union[s.CompositeStock, s.StockLeader, s.TechLeaderStock, s.LeadersIndexStock]]:    
    service = _collection_to_service.get(collection)
    serializer = _collection_to_serializer.get(collection)

    results = service.search_by_symbol(
        symbol=symbol,
    )

    return [
        serializer(stock)
        for stock in results
    ]
