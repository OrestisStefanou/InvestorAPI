CREATE TABLE dividend_leaders(
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    closing_price REAL,
    yield_pct REAL,
    dividend_growth_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE utility_leaders(
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    closing_price REAL,
    yield_pct REAL,
    dividend_growth_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE reit_leaders(
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    closing_price REAL,
    yield_pct REAL,
    dividend_growth_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE top_composite_stocks(
    comp_rating INT,
	eps_rating INT,
	rs_rating INT,
	acc_dis_rating TEXT,
	fifty_two_wk_high REAL,
	name TEXT NOT NULL,
	symbol TEXT NOT NULL,
	closing_price REAL,
    price_change_pct REAL,
	vol_chg_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL   
);

CREATE TABLE bottom_composite_stocks(
    comp_rating INT,
	eps_rating INT,
	rs_rating INT,
	acc_dis_rating TEXT,
	fifty_two_wk_high REAL,
	name TEXT NOT NULL,
	symbol TEXT NOT NULL,
	closing_price REAL,
    price_change_pct REAL,
	vol_chg_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL   
);

CREATE TABLE stocks_with_sector(
    comp_rating INT,
	eps_rating INT,
	rs_rating INT,
	acc_dis_rating TEXT,
	fifty_two_wk_high REAL,
	name TEXT NOT NULL,
	symbol TEXT NOT NULL,
	closing_price REAL,
    price_change_pct REAL,
	vol_chg_pct REAL,
    smr_rating TEXT,
    sector_name TEXT,
    sector_daily_price_change_pct REAL,
    sector_start_of_year_price_change_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE tech_leaders (
    comp_rating INT,
	eps_rating INT,
	rs_rating INT,
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    price REAL,
    annual_eps_change_pct REAL,
    last_qtr_eps_change_pct REAL,
    next_qtr_eps_change_pct REAL,
    last_qtr_sales_change_pct REAL,
    return_on_equity TEXT,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE top_low_priced_stocks(
    comp_rating INT,
	eps_rating INT,
	rs_rating INT,
	acc_dis_rating TEXT,
	year_high REAL,
	name TEXT NOT NULL,
	symbol TEXT NOT NULL,
	closing_price REAL,
    price_change_pct REAL,
	vol_chg_pct REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL   
);

CREATE TABLE large_mid_cap_leaders_index (
    comp_rating INT,
    rs_rating INT,
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    price REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE small_mid_cap_leaders_index (
    comp_rating INT,
    rs_rating INT,
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    price REAL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE world_indices_time_series (
    index_name TEXT NOT NULL,
    open_price REAL NOT NULL,
    high_price REAL NOT NULL,
    low_price REAL NOT NULL,
    close_price REAL NOT NULL,
    volume REAL NOT NULL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);

CREATE TABLE economic_indicator_time_series (
    indicator_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    registered_date TEXT NOT NULL,
    registered_date_ts INT NOT NULL
);
