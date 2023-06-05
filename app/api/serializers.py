from app.api import schema
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry
from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.stock_leader import StockLeader
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.composite_stock import CompositeStock
from app.domain.sector_performance import SectorPerformance
from app.domain.sector import Sector


def _sector_domain_model_to_schema(sector: Sector) -> schema.Sector:
    """
    We use this function because the values of schema.Sector.FOOD_BEV
    and schema.Sector.ALCOHL_TOB don't match the values of the domain Sector
    values. The reason they don't match is because having / in the enum causes
    problems in the endpoint
    """
    if sector == sector.FOOD_BEV:
        return schema.Sector.FOOD_BEV
    
    if sector == sector.ALCOHL_TOB:
        return schema.Sector.ALCOHL_TOB
    
    return schema.Sector(sector.value)


def serialize_economic_indicator_time_series_entry(
    time_series_entry: EconomicIndicatorTimeSeriesEntry
) -> schema.EconomicIndicatorTimeSeriesEntry:
    return schema.EconomicIndicatorTimeSeriesEntry(
        value=time_series_entry.value.value,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )


def serialize_index_time_series_entry(time_series_entry: IndexTimeSeriesEntry) -> schema.IndexTimeSeriesEntry:
    return schema.IndexTimeSeriesEntry(
        open_price=time_series_entry.open_price.value,
        high_price=time_series_entry.high_price.value,
        low_price=time_series_entry.low_price.value,
        close_price=time_series_entry.close_price.value,
        volume=time_series_entry.volume,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )


def serialize_stock_leader(stock_leader: StockLeader) -> schema.StockLeader:
    return schema.StockLeader(
        symbol=stock_leader.symbol,
        name=stock_leader.name,
        yield_pct=stock_leader.yield_pct.value,
        dividend_growth_pct=stock_leader.dividend_growth_pct.value
    )


def serialize_tech_leader(tech_leader: TechLeaderStock) -> schema.TechLeader:
    return schema.TechLeader(
        symbol=tech_leader.symbol,
        name=tech_leader.name,
        comp_rating=tech_leader.comp_rating.rating,
        eps_rating=tech_leader.eps_rating.rating,
        rs_rating=tech_leader.rs_rating.rating,
        annual_eps_change_pct=tech_leader.annual_eps_change_pct.value,
        last_qtr_eps_change_pct=tech_leader.last_qtr_eps_change_pct.value,
        next_qtr_eps_change_pct=tech_leader.next_qtr_eps_change_pct.value,
        last_qtr_sales_change_pct=tech_leader.last_qtr_sales_change_pct.value,
        return_on_equity=tech_leader.return_on_equity
    )


def serialize_stock(stock: CompositeStock) -> schema.Stock:
    return schema.Stock(
        overall_rating=stock.comp_rating.rating,
        eps_rating=stock.eps_rating.rating,
        rs_rating=stock.rs_rating.rating,
        name=stock.name,
        symbol=stock.symbol,
        fifty_two_wk_high=stock.fifty_two_wk_high.value,
        closing_price=stock.closing_price.value,
        vol_chg_pct=stock.vol_chg_pct.value,
        acc_dis_rating=stock.acc_dis_rating.rating,
        smr_rating=stock.smr_rating.rating,
        sector=_sector_domain_model_to_schema(stock.sector)
    )


def serialize_sector_performance(performance: SectorPerformance) -> schema.SectorPerformance:
    return schema.SectorPerformance(
        sector=_sector_domain_model_to_schema(performance.sector_name),
        daily_price_change_pct=performance.daily_price_change_pct.change_pct,
        start_of_year_price_change_pct=performance.start_of_year_price_change_pct.change_pct
    )
