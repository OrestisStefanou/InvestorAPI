from typing import List, Dict, Optional

from app.domain.world_index import WorldIndex
from app.domain.economic_indicator import EconomicIndicator
from app.domain.sector import Sector
from app.services.tech_leaders_stocks import TechLeadersStocksService
from app.services.top_comp_stocks import TopCompositeStocksService
from app.services.stocks_with_sector import StocksWithSectorService
from app.services.dividend_leaders import DividendLeadersService
from app.services.reit_leaders import ReitLeadersService
from app.services.utility_leaders import UtilityLeadersService
from app.services.leaders_index import SmallMidCapLeadersIndexService, LargeMidCapLeadersIndexService
from app.services.aggregate_service import AggregateService
from app.services.time_series import TimeSeriesService
import app.graphql.schema as s
from app.graphql.serializers import(
    serialize_composite_stock,
    serialize_stock_leader,
    serialize_tech_leader_stock,
    serialize_leaders_index_stock,
    serialize_stock_appearances_count,
    serialize_index_time_series_entry,
    serialize_economic_indicator_time_series_entry
)


_collection_to_service: Dict[s.Collection, AggregateService] = {
    s.Collection.TopCompositeStocks: TopCompositeStocksService,
    s.Collection.DividendLeaders: DividendLeadersService,
    s.Collection.ReitLeaders: ReitLeadersService,
    s.Collection.UtilityLeaders: UtilityLeadersService,
    s.Collection.TechLeaders: TechLeadersStocksService,
    s.Collection.LargeMidCapLeadersIndex: LargeMidCapLeadersIndexService,
    s.Collection.SmallMidCapLeadersIndex: SmallMidCapLeadersIndexService
}


async def top_composite_stocks_resolver(limit: int = 200) -> List[s.CompositeStock]:
    top_comp_stocks = TopCompositeStocksService.get_latest_top_comp_stocks(limit=limit)
    return [
        serialize_composite_stock(comp_stock)
        for comp_stock in top_comp_stocks[:limit]
    ]


async def reit_leaders_resolver() -> List[s.StockLeader]:
    reit_leaders = ReitLeadersService.get_latest_reit_leaders()

    return [
        serialize_stock_leader(reit_leader)
        for reit_leader in reit_leaders
    ]
 

async def sector_stocks_resolver(sector: s.Sector) -> List[s.CompositeStock]:
    sector_stocks = StocksWithSectorService.get_sector_stocks(
        sector=Sector(sector.value)
    )

    return [
        serialize_composite_stock(stock)
        for stock in sector_stocks
    ]


async def stock_historical_data_resolver(stock_symbol: str) -> List[s.CompositeStock]:
    stock_historical_data = StocksWithSectorService.get_stock_historical_data(
        stock_symbol=stock_symbol
    )

    return [
        serialize_composite_stock(stock)
        for stock in stock_historical_data
    ]


async def sectors_performance_resolver(sector: Optional[s.Sector] = None) -> List[s.SectorPerformance]:
    sectors_performance = StocksWithSectorService.get_sectors_performance(
        sector=Sector(sector.value) if sector else None
    )
    return [
        s.SectorPerformance(
            sector_name=s.Sector(sector_perf.sector_name.value),
            daily_price_change_pct=sector_perf.daily_price_change_pct.change_pct,
            start_of_year_price_change_pct=sector_perf.start_of_year_price_change_pct.change_pct,
            registered_date=sector_perf.registered_date,
            registered_date_ts=sector_perf.registered_date_ts
        )
        for sector_perf in sectors_performance

    ]


async def tech_leaders_stocks_resolver() -> List[s.TechLeaderStock]:
    tech_leaders_stocks = TechLeadersStocksService.get_latest_tech_leaders_stocks()

    return [
        serialize_tech_leader_stock(stock)
        for stock in tech_leaders_stocks
    ]


async def dividend_leaders_resolver() -> List[s.StockLeader]:
    dividend_leaders = DividendLeadersService.get_latest_dividend_leaders()

    return [
        serialize_stock_leader(dividend_leader)
        for dividend_leader in dividend_leaders
    ]


async def utility_leaders_resolver() -> List[s.StockLeader]:
    utility_leaders = UtilityLeadersService.get_latest_utility_leaders()

    return [
        serialize_stock_leader(utility_leader)
        for utility_leader in utility_leaders
    ]


async def small_mid_cap_leaders_index_resolver() -> List[s.LeadersIndexStock]:
    small_mid_cap_leaders_index = SmallMidCapLeadersIndexService.get_latest_leaders_index()

    return [
        serialize_leaders_index_stock(stock)
        for stock in small_mid_cap_leaders_index
    ]


async def large_mid_cap_leaders_index_resolver() -> List[s.LeadersIndexStock]:
    large_mid_cap_leaders_index = LargeMidCapLeadersIndexService.get_latest_leaders_index()

    return [
        serialize_leaders_index_stock(stock)
        for stock in large_mid_cap_leaders_index
    ]


async def appereances_count_per_stock_in_collection_resolver(
    collection: s.Collection,
    limit: int = 100
) -> List[s.StockAppereancesCount]:    
    service = _collection_to_service.get(collection)
    
    appereances_count = service.get_appereances_count_for_each_symbol(
        limit=limit,
    )

    return [
        serialize_stock_appearances_count(appearance)
        for appearance in appereances_count
    ]


async def index_time_series_resolver(
    index: s.WorldIndex
) -> s.IndexTimeSeries:
    index_time_series = TimeSeriesService.get_index_time_series(
        index=WorldIndex(index.value)
    )

    return s.IndexTimeSeries(
        index=index,
        time_series=[
            serialize_index_time_series_entry(time_serie)
            for time_serie in index_time_series
        ]
    )

async def economic_indicator_time_series_resolver(
    indicator: s.EconomicIndicator
) -> s.EconomicIndicatorTimeSeries:
    indicator_time_series = TimeSeriesService.get_economic_indicator_time_series(
        indicator=EconomicIndicator(indicator.value)
    )
    
    return s.EconomicIndicatorTimeSeries(
        indicator=indicator,
        unit=indicator_time_series[0].unit,
        time_series=[
            serialize_economic_indicator_time_series_entry(time_serie)
            for time_serie in indicator_time_series
        ]
    )
