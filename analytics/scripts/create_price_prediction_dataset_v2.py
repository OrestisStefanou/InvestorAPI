import datetime as dt
import sqlite3
from typing import Optional, List

import pandas as pd
import numpy as np

PREDICTION_TIMEWINDOW_DAYS = 90

conn = sqlite3.connect('app/database/ibd.db')

def get_stock_fundamental_df(symbol: str) -> pd.DataFrame:
    query = f'''
        SELECT 
            income_statement.total_revenue,
            income_statement.gross_profit,
            income_statement.operating_income,
            income_statement.net_income,
            income_statement.ebitda,
            income_statement.net_interest_income,

            balance_sheet.total_assets,
            balance_sheet.total_liabilities,
            balance_sheet.total_shareholder_equity,
            balance_sheet.total_current_assets,
            balance_sheet.total_current_liabilities,
            balance_sheet.cash_and_cash_equivalents_at_carrying_value,
            balance_sheet.long_term_debt,
            balance_sheet.current_net_receivables,
            balance_sheet.inventory,
            balance_sheet.property_plant_equipment,
            
            cash_flow.operating_cashflow,
            cash_flow.capital_expenditures,
            cash_flow.cashflow_from_investment,
            cash_flow.cashflow_from_financing,
            cash_flow.dividend_payout,
            cash_flow.proceeds_from_issuance_of_long_term_debt_and_capital_securities_net,
            cash_flow.payments_for_repurchase_of_equity,
            
            stock_overview.sector,
            stock_overview.symbol,
            income_statement.fiscal_date_ending
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
        ['symbol', 'fiscal_date_ending', 'sector']
    )

    # Convert selected columns to float
    stock_df[columns_to_convert] = stock_df[columns_to_convert].astype(float)

    # We fill NaN values with a small value because later we perform feature
    # engineering to calculate pct change and ratios and we can't divide witrh zero
    stock_df[columns_to_convert] = stock_df[columns_to_convert].fillna(0.01)
    stock_df[columns_to_convert] = stock_df[columns_to_convert].replace(0, 0.01)

    # Feature engineering
    for column in columns_to_convert:
        # arctan percentage change
        log_pct_change_column_name = f'{column}_arctan_pct_change'
        stock_df[log_pct_change_column_name] = np.arctan(stock_df[column].pct_change())

        # Plain percentage change
        pct_change_column_name = f'{column}_pct_change'
        stock_df[pct_change_column_name] = stock_df[column].pct_change()

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


def get_stock_time_series_df(symbol: str) -> pd.DataFrame:
    query = f'''
    SELECT  *
    FROM stock_time_series
    WHERE symbol = '{symbol}'
    ORDER BY registered_date_ts DESC
    '''
    
    stock_time_series_df = pd.read_sql(query, conn)
    return stock_time_series_df


def get_sector_time_series_df(sector: str) -> pd.DataFrame:
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
    days: int = PREDICTION_TIMEWINDOW_DAYS
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
    days: int = PREDICTION_TIMEWINDOW_DAYS
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



interest_rate_df = get_interest_rate_df()
treasury_yield_df = get_treasury_yield_df()

sectors_time_series = {
    'LIFE SCIENCES': get_sector_time_series_df('LIFE SCIENCES'),
    'TECHNOLOGY': get_sector_time_series_df('TECHNOLOGY'),
    'TRADE & SERVICES': get_sector_time_series_df('TRADE & SERVICES'),
    'FINANCE': get_sector_time_series_df('FINANCE'),
    'REAL ESTATE & CONSTRUCTION': get_sector_time_series_df('REAL ESTATE & CONSTRUCTION'),
    'MANUFACTURING': get_sector_time_series_df('MANUFACTURING'),
    'ENERGY & TRANSPORTATION': get_sector_time_series_df('ENERGY & TRANSPORTATION')
}

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

    final_stock_time_series_df['interest_rate'] = final_stock_time_series_df['Date'].apply(
        find_time_series_most_recent_value,
        target_column='value',
        time_series_df=interest_rate_df,
        days=-90
    )

    final_stock_time_series_df['treasury_yield'] = final_stock_time_series_df['Date'].apply(
        find_time_series_most_recent_value,
        target_column='value',
        time_series_df=treasury_yield_df,
        days=-90
    )

    final_stock_time_series_df['price_pct_change_last_six_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-180
    )

    final_stock_time_series_df['price_pct_change_last_three_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-90
    )

    final_stock_time_series_df['price_pct_change_last_month'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-33
    )

    final_stock_time_series_df['price_volatility_last_six_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_volatility,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-180
    )

    final_stock_time_series_df['price_volatility_last_three_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_volatility,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-90
    )

    final_stock_time_series_df['price_volatility_last_month'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_volatility,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-33
    )

    final_stock_time_series_df['price_pct_change_next_six_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=180
    )

    final_stock_time_series_df['price_pct_change_next_three_months'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=90
    )

    final_stock_time_series_df['price_pct_change_next_month'] = final_stock_time_series_df['Date'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=33
    )

    final_stock_time_series_df['sector_pct_change_last_six_months'] = final_stock_time_series_df['Date'].apply(
        calculate_sector_pct_change,
        time_series_df=sector_time_series_df,
        days=-180
    )

    final_stock_time_series_df['sector_pct_change_last_three_months'] = final_stock_time_series_df['Date'].apply(
        calculate_sector_pct_change,
        time_series_df=sector_time_series_df,
        days=-90
    )

    final_stock_time_series_df['sector_pct_change_last_month'] = final_stock_time_series_df['Date'].apply(
        calculate_sector_pct_change,
        time_series_df=sector_time_series_df,
        days=-33
    )

    financial_statements_columns = [col_name for col_name in stock_fundamental_df.columns if str(col_name).endswith('_arctan_pct_change')]
    final_stock_time_series_df[financial_statements_columns] = final_stock_time_series_df['Date'].apply(
        find_latest_financials_data,
        financials_time_series_df=stock_fundamental_df,
    )

    return final_stock_time_series_df


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
    dataset_df.to_sql('price_prediction_dataset_v2', conn, index=False, if_exists='replace')
    dataset_df.to_csv('price_prediction_dataset_v2.csv')


create_dataset()
conn.close()