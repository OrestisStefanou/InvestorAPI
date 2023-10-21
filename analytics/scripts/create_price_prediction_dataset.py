import sqlite3
from typing import Optional, List

import pandas as pd

PREDICTION_TIMEWINDOW_DAYS = 90

conn = sqlite3.connect('app/database/ibd.db')

def get_stock_fundamental_df(symbol: str) -> pd.DataFrame:
    query = f'''
        SELECT income_statement.*, balance_sheet.*, cash_flow.*, stock_overview.sector
        FROM income_statement
        INNER JOIN balance_sheet
        ON income_statement.fiscal_date_ending = balance_sheet.fiscal_date_ending  AND balance_sheet.symbol = '{symbol}'
        INNER JOIN cash_flow
        ON income_statement.fiscal_date_ending = cash_flow.fiscal_date_ending  AND cash_flow.symbol = '{symbol}'
        INNER JOIN stock_overview
        ON income_statement.symbol = stock_overview.symbol  AND stock_overview.symbol = '{symbol}'
        WHERE income_statement.symbol = '{symbol}'
        ORDER BY DATE(income_statement.fiscal_date_ending)
    '''
    stock_df = pd.read_sql(query, conn)
    
    # Drop columns with duplicated names
    stock_df = stock_df.loc[:, ~stock_df.columns.duplicated()]

    # List of columns to convert to float
    columns_to_convert = stock_df.columns.difference(
        ['symbol', 'fiscal_date_ending', 'reported_currency', 'sector']
    )

    # Convert selected columns to float
    stock_df[columns_to_convert] = stock_df[columns_to_convert].astype(float)
    # Fill NaN values with zero for the selected columns
    stock_df[columns_to_convert] = stock_df[columns_to_convert].fillna(0)
    return stock_df


def get_interest_rate_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Interest_Rate'
    '''

    interest_rate_df = pd.read_sql(query, conn)
    return interest_rate_df


def get_treasury_yield_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Treasury_Yield'
    '''

    treasury_yield_df = pd.read_sql(query, conn)
    return treasury_yield_df


def get_commodities_index_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Global_Commodities_Index'
    '''

    commodities_index_df = pd.read_sql(query, conn)
    return commodities_index_df


def get_unemployment_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Unemployment'
    '''

    unemployment_df = pd.read_sql(query, conn)
    return unemployment_df  


def get_inflation_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Inflation'
    ORDER BY registered_date_ts DESC
    '''

    inflation_df = pd.read_sql(query, conn)
    return inflation_df


def get_natural_gas_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Natural_Gas'
    ORDER BY registered_date_ts DESC
    '''

    inflation_df = pd.read_sql(query, conn)
    return inflation_df


def get_oil_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Crude_Oil'
    ORDER BY registered_date_ts DESC
    '''

    inflation_df = pd.read_sql(query, conn)
    return inflation_df


def get_stock_time_series_df(symbol: str) -> pd.DataFrame:
    query = f'''
    SELECT  *
    FROM stock_time_series
    WHERE symbol = '{symbol}'
    ORDER BY registered_date_ts DESC
    '''
    
    stock_time_series_df = pd.read_sql(query, conn)
    return stock_time_series_df


def calculate_time_series_avg_value(
    start_date: str,
    time_series_df: pd.DataFrame,
    target_column: str,
    days: int = PREDICTION_TIMEWINDOW_DAYS
) -> Optional[int]:
    """
    Given a start calculate what was the avg value
    between <start_date> and <start_date> + <days> time
    """
    lower_bound = pd.Timestamp(start_date)
    
    upper_bound = lower_bound + pd.DateOffset(days=days)
    
    # Filter the DataFrame
    filtered_df = time_series_df[(time_series_df['registered_date_ts'] >= lower_bound.timestamp()) & (time_series_df['registered_date_ts'] <= upper_bound.timestamp())]
    
    if len(filtered_df) == 0:
        return None

    average_value = filtered_df[target_column].mean()
    return average_value


def get_inflation_value_by_date(date_string: str, inflation_df: pd.DataFrame) -> Optional[float]:
    try:
        date_obj = pd.to_datetime(date_string, format='%Y-%m-%d')
        target_year = date_obj.year
        inflation_df['register_date_pandas_dt'] = pd.to_datetime(inflation_df['registered_date'], format='%d-%m-%Y')
        selected_row = inflation_df[inflation_df['register_date_pandas_dt'].dt.year == target_year]
        if not selected_row.empty:
            return selected_row['value'].iloc[0]
        else:
            return None
    except (ValueError, KeyError):
        return None


interest_rate_df = get_interest_rate_df()
treasury_yield_df = get_treasury_yield_df()
commodities_index_df = get_commodities_index_df()
unemployment_df = get_unemployment_df()
inflation_df = get_inflation_df()
natural_gas_df = get_natural_gas_df()
oil_df = get_oil_df()


def get_final_stock_data_df(symbol: str) -> pd.DataFrame:
    stock_fundamental_df = get_stock_fundamental_df(symbol)
    stock_time_series_df = get_stock_time_series_df(symbol)

    stock_fundamental_df['avg_interest_rate'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=interest_rate_df,
    )

    stock_fundamental_df['avg_treasury_yield'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=treasury_yield_df,
    )

    stock_fundamental_df['avg_natural_gas_price'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=natural_gas_df,
    )

    stock_fundamental_df['avg_oil_price'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=oil_df,
    )

    stock_fundamental_df['avg_unemployment_rate'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=unemployment_df,
    )

    stock_fundamental_df['avg_global_commodities_index_value'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=commodities_index_df,
    )

    stock_fundamental_df['inflation'] = stock_fundamental_df['fiscal_date_ending'].apply(
        get_inflation_value_by_date,
        inflation_df=inflation_df,
    )

    stock_fundamental_df['price'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='close_price',
        time_series_df=stock_time_series_df,
    )

    return stock_fundamental_df


def create_dataset(symbols: Optional[List[str]] = None):
    if not symbols:
        query = 'SELECT DISTINCT symbol FROM income_statement'
        rows = conn.execute(query).fetchall()
        symbols = [row[0] for row in rows]

    stock_dfs = []
    for symbol in symbols:
        stock_df = get_final_stock_data_df(symbol)
        stock_dfs.append(stock_df)

    dataset_df = pd.concat(stock_dfs)
    dataset_df.to_sql('price_prediction_dataset', conn, index=False, if_exists='replace')


create_dataset()
conn.close()