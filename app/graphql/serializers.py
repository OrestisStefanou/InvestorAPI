from app.graphql import schema as s
from app.domain.composite_stock import CompositeStock
from app.domain.stock_leader import StockLeader
from app.domain.composite_stock import StockWithSector
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry


def serialize_composite_stock(comp_stock: CompositeStock) -> s.CompositeStock:
    return s.CompositeStock(
        comp_rating=comp_stock.comp_rating.rating,
        eps_rating=comp_stock.eps_rating.rating,
        rs_rating=comp_stock.rs_rating.rating,
        acc_dis_rating=comp_stock.acc_dis_rating.rating,
        fifty_two_wk_high=comp_stock.fifty_two_wk_high.value,
        name=comp_stock.name,
        symbol=comp_stock.symbol,
        closing_price=comp_stock.closing_price.value,
        price_change_pct=comp_stock.price_change_pct.value,
        vol_chg_pct=comp_stock.vol_chg_pct.value,
        registered_date=comp_stock.registered_date
    )


def serialize_stock_leader(stock_leader: StockLeader) -> s.StockLeader:
    return s.StockLeader(
            name=stock_leader.name,
            symbol=stock_leader.symbol,
            closing_price=stock_leader.closing_price.value,
            yield_pct=stock_leader.yield_pct.value,
            dividend_growth_pct=stock_leader.dividend_growth_pct.value,
            registered_date=stock_leader.registered_date
    )


def serialize_stock_with_sector(stock: StockWithSector) -> s.SectorStock:
    return s.SectorStock(
            comp_rating=stock.comp_rating.rating,
            eps_rating=stock.eps_rating.rating,
            rs_rating=stock.rs_rating.rating,
            acc_dis_rating=stock.acc_dis_rating.rating,
            fifty_two_wk_high=stock.fifty_two_wk_high.value,
            name=stock.name,
            symbol=stock.symbol,
            closing_price=stock.closing_price.value,
            price_change_pct=stock.price_change_pct.value,
            vol_chg_pct=stock.vol_chg_pct.value,
            smr_rating=stock.smr_rating.rating,
            sector_name=stock.sector_name,
            sector_daily_price_change_pct=stock.sector_daily_price_change_pct.value,
            sector_start_of_year_price_change_pct=stock.sector_start_of_year_price_change_pct.value,
            registered_date=stock.registered_date
    )



def serialize_tech_leader_stock(stock: TechLeaderStock) -> s.TechLeaderStock:
    return s.TechLeaderStock(
        comp_rating=stock.comp_rating.rating,
        eps_rating=stock.eps_rating.rating,
        rs_rating=stock.rs_rating.rating,
        name=stock.name,
        symbol=stock.symbol,
        closing_price=stock.price.value,
        annual_eps_change_pct=stock.annual_eps_change_pct.value,
        last_qtr_eps_change_pct=stock.last_qtr_eps_change_pct.value,
        next_qtr_eps_change_pct=stock.next_qtr_eps_change_pct.value,
        last_qtr_sales_change_pct=stock.last_qtr_sales_change_pct.value,
        return_on_equity=stock.return_on_equity,
        registered_date=stock.registered_date
    )


def serialize_low_priced_stock(stock: CompositeStock) -> s.LowPricedStock:
    return s.LowPricedStock(
        comp_rating=stock.comp_rating.rating,
        eps_rating=stock.eps_rating.rating,
        rs_rating=stock.rs_rating.rating,
        acc_dis_rating=stock.acc_dis_rating.rating,
        year_high=stock.year_high.value,
        name=stock.name,
        symbol=stock.symbol,
        closing_price=stock.closing_price.value,
        price_change_pct=stock.price_change_pct.value,
        vol_chg_pct=stock.vol_chg_pct.value
    )


def serialize_leaders_index_stock(stock: StockLeader) -> s.LeadersIndexStock:
    return s.LeadersIndexStock(
        comp_rating=stock.comp_rating.rating,
        rs_rating=stock.rs_rating.rating,
        stock_name=stock.name,
        stock_symbol=stock.symbol,
        closing_price=stock.closing_price.value,
        registered_date=stock.registered_date
    )


def serialize_stock_appearances_count(appearance: SymbolAppearancesCount) -> s.StockAppereancesCount:
    return s.StockAppereancesCount(
        symbol=appearance.symbol,
        name=appearance.name,
        count=appearance.count
    )


def serialize_index_time_series_entry(time_series_entry: IndexTimeSeriesEntry) -> s.IndexTimeSeriesEntry:
    return s.IndexTimeSeriesEntry(
        open_price=time_series_entry.open_price.value,
        high_price=time_series_entry.high_price.value,
        low_price=time_series_entry.low_price.value,
        close_price=time_series_entry.close_price.value,
        volume=time_series_entry.volume,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )

def serialize_economic_indicator_time_series_entry(
    time_series_entry: EconomicIndicatorTimeSeriesEntry
) -> s.EconomicIndicatorTimeSeriesEntry:
    return s.EconomicIndicatorTimeSeriesEntry(
        value=time_series_entry.value.value,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )
