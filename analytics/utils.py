import datetime as dt
import sqlite3
from typing import Optional

import pandas as pd

def get_interest_rate_df(conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
    if conn is None:
        conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db') # FIX THE PATH HERE

    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Interest_Rate'
    '''

    interest_rate_df = pd.read_sql(query, conn)
    return interest_rate_df


def get_treasury_yield_df(conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
    if conn is None:
        conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db') # FIX THE PATH HERE

    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Treasury_Yield'
    '''

    treasury_yield_df = pd.read_sql(query, conn)
    return treasury_yield_df


def get_stock_time_series_df(symbol: str, conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
    if conn is None:
        conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db') # FIX THE PATH HERE

    query = f'''
    SELECT  *
    FROM stock_time_series
    WHERE symbol = '{symbol}'
    ORDER BY registered_date_ts DESC
    '''
    
    stock_time_series_df = pd.read_sql(query, conn)
    return stock_time_series_df


def get_sector_time_series_df(sector: str, conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
    if conn is None:
        conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db') # FIX THE PATH HERE

    query = f'''
    SELECT AVG(sts.close_price) AS sector_price, substr(sts.registered_date, 4, 7) AS month_year
    FROM stock_time_series as sts
    INNER JOIN stock_overview as so
    ON sts.symbol = so.symbol
    WHERE so.sector = '{sector}'
    GROUP BY month_year
    ORDER BY sts.registered_date_ts ASC
    '''

    sector_df = pd.read_sql(query, conn)
    sector_df['Date'] = pd.to_datetime(sector_df['month_year'], format='%m-%Y')
    return sector_df


def calculate_time_series_pct_change(
    start_date: str,
    time_series_df: pd.DataFrame,
    target_column: str,
    days: int
) -> Optional[int]:
    """
    Given a start calculate what was the pct change
    between <start_date> and <start_date> + <days> time
    """
    if days < 0:
        lower_bound = pd.Timestamp(start_date) - pd.DateOffset(days=abs(days))
        upper_bound = pd.Timestamp(start_date) 
    else:
        lower_bound = pd.Timestamp(start_date)
        upper_bound = lower_bound + pd.DateOffset(days=days)
    
    time_series_df['registered_date_ts'] = pd.to_datetime(time_series_df['registered_date_ts'], unit='s')
    # Filter the DataFrame
    filtered_df = time_series_df[
        (time_series_df['registered_date_ts'] >= lower_bound) & 
        (time_series_df['registered_date_ts'] <= upper_bound)
    ]

    if len(filtered_df) == 0:
        return None

    # Sort the filtered DataFrame by timestamp
    filtered_df = filtered_df.sort_values(by='registered_date_ts')

    # Calculate pct change between first and last row
    pct_change = ((filtered_df[target_column].iloc[-1] - filtered_df[target_column].iloc[0]) / filtered_df[target_column].iloc[0])
    return pct_change


def calculate_sector_pct_change(
    start_date: dt.datetime,
    time_series_df: pd.DataFrame,
    days: int
) -> Optional[int]:
    """
    Given a start calculate what was the pct change
    between <start_date> and <start_date> +/- <days> time
    """
    if days < 0:
        lower_bound = start_date - pd.DateOffset(days=abs(days))
        upper_bound = start_date 
    else:
        lower_bound = start_date
        upper_bound = lower_bound + pd.DateOffset(days=days)
    
    # Filter the DataFrame
    filtered_df = time_series_df[
        (time_series_df['Date'] >= lower_bound) & 
        (time_series_df['Date'] <= upper_bound)
    ]

    if len(filtered_df) == 0:
        return None

    # Sort the filtered DataFrame by timestamp
    filtered_df = filtered_df.sort_values(by='Date')

    # Calculate pct change between first and last row
    pct_change = ((filtered_df['sector_price'].iloc[-1] - filtered_df['sector_price'].iloc[0]) / filtered_df['sector_price'].iloc[0])
    return pct_change


def find_time_series_most_recent_value(
    start_date: str,
    time_series_df: pd.DataFrame,
    target_column: str,
    days: int 
) -> Optional[int]:
    """
    Given a start_date find the most recent value
    between <start_date> and <start_date> +/- <days> time
    """
    if days < 0:
        lower_bound = pd.Timestamp(start_date) - pd.DateOffset(days=abs(days))
        upper_bound = pd.Timestamp(start_date) 
    else:
        lower_bound = pd.Timestamp(start_date)
        upper_bound = lower_bound + pd.DateOffset(days=days)
    
    time_series_df['registered_date_ts'] = pd.to_datetime(time_series_df['registered_date_ts'], unit='s')
    # Filter the DataFrame
    filtered_df = time_series_df[
        (time_series_df['registered_date_ts'] >= lower_bound) & 
        (time_series_df['registered_date_ts'] <= upper_bound)
    ]

    if len(filtered_df) == 0:
        return None

    # Sort the filtered DataFrame by timestamp
    filtered_df = filtered_df.sort_values(by='registered_date_ts')
    return filtered_df[target_column].iloc[-1]


def calculate_time_series_volatility(
    start_date: str,
    time_series_df: pd.DataFrame,
    target_column: str,
    days: int
) -> Optional[int]:
    """
    Given a start calculate what was the volatility
    between <start_date> and <start_date> +/- <days> time
    """
    if days < 0:
        lower_bound = pd.Timestamp(start_date) - pd.DateOffset(days=abs(days))
        upper_bound = pd.Timestamp(start_date) 
    else:
        lower_bound = pd.Timestamp(start_date)
        upper_bound = lower_bound + pd.DateOffset(days=days)
    
    time_series_df['registered_date_ts'] = pd.to_datetime(time_series_df['registered_date_ts'], unit='s')
    # Filter the DataFrame
    filtered_df = time_series_df[
        (time_series_df['registered_date_ts'] >= lower_bound) & 
        (time_series_df['registered_date_ts'] <= upper_bound)
    ]

    if len(filtered_df) == 0:
        return None

    # Sort the filtered DataFrame by timestamp
    filtered_df = filtered_df.sort_values(by='registered_date_ts')

    volatility = filtered_df[target_column].pct_change().std()
    return volatility


def find_latest_financials_data(
    start_date,
    financials_time_series_df: pd.DataFrame,
    days: int = 30 * 6
):
    """
    Returns the most recent financials data of a stock from 'start_date'(Going backwards)
    """
    upper_bound = start_date
    lower_bound = start_date - pd.DateOffset(days=days)
    
    financials_time_series_df['fiscal_date_ending'] = pd.to_datetime(financials_time_series_df['fiscal_date_ending'], format='%Y-%m-%d')
    # Filter the DataFrame
    filtered_df = financials_time_series_df[
        (financials_time_series_df['fiscal_date_ending'] >= lower_bound) & 
        (financials_time_series_df['fiscal_date_ending'] <= upper_bound)
    ]

    if len(filtered_df) == 0:
        return None

    # Sort the filtered DataFrame by timestamp
    filtered_df = filtered_df.sort_values(by='fiscal_date_ending')

    columns_to_return = [col_name for col_name in filtered_df.columns if str(col_name).endswith('_arctan_pct_change')]    
    return filtered_df[columns_to_return].iloc[-1]
