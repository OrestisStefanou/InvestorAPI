from pydantic import BaseSettings

# TODO Create a .env file and read these values from there
class Settings(BaseSettings):
    # Ibd
    ibd_base_url: str = "https://www.investors.com/data-tables"
    # SQLite
    db_path = "app/database/ibd.db"
    # Yahoo finance
    y_finance_base_url: str = 'https://query1.finance.yahoo.com/v7'
    # Alpha vantage
    alpha_vantage_base_url: str = 'https://www.alphavantage.co/query'
    alpha_vantage_token: str = 'LQ2GKKKWRJI6WAM9'
