import datetime as dt
import sqlite3
from typing import Optional, List

import pandas as pd

PREDICTION_TIMEWINDOW_DAYS = 90

conn = sqlite3.connect('app/database/ibd.db')

from analytics.utils import (
    get_sectors_time_series,
    get_stock_time_series_df,
    calculate_time_series_pct_change
)
from analytics.machine_learning.price_prediction_with_fundamentals.utils import (
    get_stock_fundamental_df,
    add_timeseries_features
)

sectors_time_series = get_sectors_time_series()

def get_final_stock_data_df(symbol: str) -> pd.DataFrame:
    stock_fundamental_df = get_stock_fundamental_df(symbol)
    stock_time_series_df = get_stock_time_series_df(symbol)

    stock_sector = stock_fundamental_df.iloc[0, stock_fundamental_df.columns.get_loc('sector')]
    sector_time_series_df = sectors_time_series.get(stock_sector)

    # Create stock time series
    start_date = stock_fundamental_df['fiscal_date_ending'].iloc[0]
    end_date = dt.date.today().isoformat()
    final_stock_time_series_df = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq='MS'), columns=['Date'])
    final_stock_time_series_df['symbol'] = symbol
    final_stock_time_series_df['sector'] = stock_sector

    # Add target columns
    final_stock_time_series_df['price_pct_change_next_six_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=186
    )

    final_stock_time_series_df['price_pct_change_next_three_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=93
    )

    final_stock_time_series_df['price_pct_change_next_month'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=33
    )

    return add_timeseries_features(
        stock_prediction_data_df=final_stock_time_series_df,
        stock_fundamental_df=stock_fundamental_df,
        stock_time_series_df=stock_time_series_df,
        sector_time_series_df=sector_time_series_df
    )


def create_dataset(symbols: Optional[List[str]] = None):
    if not symbols:
        query = 'SELECT DISTINCT symbol FROM income_statement'
        rows = conn.execute(query).fetchall()
        symbols = [row[0] for row in rows]

    stock_dfs = []
    for symbol in symbols:
        try:
            stock_df = get_final_stock_data_df(symbol)
            stock_dfs.append(stock_df)
        except Exception:
            continue

    dataset_df = pd.concat(stock_dfs)
    dataset_df.to_sql('price_prediction_dataset_v3', conn, index=False, if_exists='replace')


create_dataset()
conn.close()
