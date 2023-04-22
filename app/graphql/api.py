from typing import List

import strawberry as graphql

import app.graphql.schema as s
from app.graphql.resolvers import (
    top_composite_stocks_resolver,
    bottom_composite_stocks_resolver,
    reit_leaders_resolver,
    sector_stocks_resolver,
    sectors_performance_resolver,
    stock_historical_data_resolver,
    tech_leaders_stocks_resolver,
    top_low_priced_stocks_resolver,
    dividend_leaders_resolver,
    utility_leaders_resolver,
    small_mid_cap_leaders_index_resolver,
    large_mid_cap_leaders_index_resolver,
    appereances_count_per_stock_in_collection_resolver,
    search_symbol_in_collection_resolver,
    index_time_series_resolver,
    economic_indicator_time_series_resolver
)


@graphql.type
class Query:
    # top_composite_stocks: List[s.CompositeStock] = graphql.field(resolver=top_composite_stocks_resolver)
    # bottom_composite_stocks: List[s.CompositeStock] = graphql.field(resolver=bottom_composite_stocks_resolver)
    # stocks_with_sector: List[s.SectorStock] = graphql.field(resolver=stocks_with_sector_resolver)
    # sectors_performance: List[s.SectorPerformance] = graphql.field(resolver=sectors_performance_resolver)
    # tech_leaders: List[s.TechLeaderStock] = graphql.field(resolver=tech_leaders_stocks_resolver)
    # top_low_priced_stocks: List[s.LowPricedStock] = graphql.field(resolver=top_low_priced_stocks_resolver)
    # dividend_leaders: List[s.StockLeader] = graphql.field(resolver=dividend_leaders_resolver)
    # reit_leaders: List[s.StockLeader] = graphql.field(resolver=reit_leaders_resolver)
    # utility_leaders: List[s.StockLeader] = graphql.field(resolver=utility_leaders_resolver)
    # small_mid_cap_leaders_index: List[s.LeadersIndexStock] = graphql.field(resolver=small_mid_cap_leaders_index_resolver)
    # large_mid_cap_leaders_index: List[s.LeadersIndexStock] = graphql.field(resolver=large_mid_cap_leaders_index_resolver)
    # appereances_count_per_stock_in_collection: List[s.StockAppereancesCount] = graphql.field(resolver=appereances_count_per_stock_in_collection_resolver)
    # search_symbol_in_collection: List[
    #     Union[
    #         s.CompositeStock,
    #         s.StockLeader,
    #         s.TechLeaderStock,
    #         s.LeadersIndexStock
    #     ]
    # ] = graphql.field(resolver=search_symbol_in_collection_resolver)
    index_time_series: s.IndexTimeSeries = graphql.field(resolver=index_time_series_resolver)
    economic_indicator_time_series: s.EconomicIndicatorTimeSeries = graphql.field(resolver=economic_indicator_time_series_resolver)
    sectors_performance: List[s.SectorPerformance] = graphql.field(resolver=sectors_performance_resolver)
    sector_stocks: List[s.CompositeStock] = graphql.field(resolver=sector_stocks_resolver)
    stock_historical_data: List[s.CompositeStock] = graphql.field(resolver=stock_historical_data_resolver)

schema = graphql.Schema(query=Query)
