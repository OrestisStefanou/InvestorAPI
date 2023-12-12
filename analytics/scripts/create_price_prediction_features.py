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
        # arctan ratio
        log_ration_column_name = f'{column}_arctan_ratio'
        stock_df[log_ration_column_name] = np.arctan(stock_df[column] / stock_df[column].shift(1))

        # arctan percentage change
        log_pct_change_column_name = f'{column}_arctan_pct_change'
        stock_df[log_pct_change_column_name] = np.arctan(stock_df[column].pct_change())

        # Plain percentag change
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


def get_unemployment_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Unemployment'
    '''

    unemployment_df = pd.read_sql(query, conn)
    return unemployment_df


def get_commodities_index_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Global_Commodities_Index'
    '''

    commodities_index_df = pd.read_sql(query, conn)
    return commodities_index_df

def get_natural_gas_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Natural_Gas'
    ORDER BY registered_date_ts DESC
    '''

    natural_gas_df = pd.read_sql(query, conn)
    return natural_gas_df


def get_oil_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Crude_Oil'
    ORDER BY registered_date_ts DESC
    '''

    oil_df = pd.read_sql(query, conn)
    return oil_df


def get_inflation_df() -> pd.DataFrame:
    query = '''
    SELECT  *
    FROM economic_indicator_time_series
    WHERE indicator_name = 'Inflation'
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

    average_value = filtered_df[target_column].mean()
    return average_value


def calculate_time_series_volatility(
    start_date: str,
    time_series_df: pd.DataFrame,
    target_column: str,
    days: int = PREDICTION_TIMEWINDOW_DAYS
) -> Optional[int]:
    """
    Given a start calculate what was the volatility
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

    volatility = filtered_df[target_column].pct_change().std()
    return volatility


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
unemployment_df = get_unemployment_df()
inflation_df = get_inflation_df()
natural_gas_df = get_natural_gas_df()
oil_df = get_oil_df()
commodities_index_df = get_commodities_index_df()


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

    stock_fundamental_df['avg_global_commodities_index_value'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=commodities_index_df,
    )

    stock_fundamental_df['avg_unemployment_rate'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='value',
        time_series_df=unemployment_df,
    )

    stock_fundamental_df['inflation'] = stock_fundamental_df['fiscal_date_ending'].apply(
        get_inflation_value_by_date,
        inflation_df=inflation_df,
    )

    stock_fundamental_df['price_pct_change_three_months'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-PREDICTION_TIMEWINDOW_DAYS
    )

    stock_fundamental_df['price_volatility_three_months'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_volatility,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-PREDICTION_TIMEWINDOW_DAYS
    )

    stock_fundamental_df['price_pct_change_next_three_months'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_pct_change,
        target_column='close_price',
        time_series_df=stock_time_series_df,
    )

    stock_fundamental_df['avg_three_months_price'] = stock_fundamental_df['fiscal_date_ending'].apply(
        calculate_time_series_avg_value,
        target_column='close_price',
        time_series_df=stock_time_series_df,
        days=-PREDICTION_TIMEWINDOW_DAYS
    )

    stock_fundamental_df['avg_next_three_months_price'] = stock_fundamental_df['fiscal_date_ending'].apply(
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
    dataset_df.to_sql('price_prediction_features', conn, index=False, if_exists='replace')
    dataset_df.to_csv('price_prediction_features.csv')


create_dataset()
conn.close()