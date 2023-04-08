from pydantic import BaseSettings

# TODO Create a .env file and read these values from there
class Settings(BaseSettings):
    # Ibd
    ibd_base_url: str = "https://www.investors.com/data-tables"
    # SQLite
    db_path = "app/database/ibd.db"
    # Redis
    redis_host: str = "redis-10023.c135.eu-central-1-1.ec2.cloud.redislabs.com"
    redis_port: int = 10023
    redis_password: str = '7A3YqMImyKXKVoWh5Hcda9ooGHtVyi14'
    # Yahoo finance
    y_finance_base_url: str = 'https://finance.yahoo.com'
