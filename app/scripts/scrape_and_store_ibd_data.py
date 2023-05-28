import logging
import time

from app.services.dividend_leaders import DividendLeadersService
from app.services.leaders_index import SmallMidCapLeadersIndexService, LargeMidCapLeadersIndexService
from app.services.reit_leaders import ReitLeadersService
from app.services.stocks_with_sector import StocksWithSectorService
from app.services.tech_leaders_stocks import TechLeadersStocksService
from app.services.top_comp_stocks import TopCompositeStocksService
from app.services.utility_leaders import UtilityLeadersService

async def scrape_and_store_data(day: int, month: int, year: int):
    try:
        await DividendLeadersService.scrape_and_store_dividend_leaders_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store dividend leaders:", err)

    time.sleep(2)

    try:
        await SmallMidCapLeadersIndexService.scrape_and_store_leaders_index_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store small mid cap leaders index:", err)

    time.sleep(2)

    try:
        await LargeMidCapLeadersIndexService.scrape_and_store_leaders_index_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store large mid cap leaders index:", err)

    time.sleep(2)

    try:
        await ReitLeadersService.scrape_and_store_reit_leaders_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store reit leaders:", err)

    time.sleep(2)

    try:
        await StocksWithSectorService.scrape_and_store_stocks_with_sector_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store stocks with sector:", err)

    time.sleep(2)

    try:
        await TechLeadersStocksService.scrape_and_store_tech_leaders_stocks_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store tech leaders:", err)

    time.sleep(2)

    try:
        await TopCompositeStocksService.scrape_and_store_top_200_comp_stocks_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store top composite stocks:", err)

    time.sleep(2)

    try:
        await UtilityLeadersService.scrape_and_store_utility_leaders_for_date(day, month, year)
    except Exception as err:
        logging.error("Failed to scrape and store utility leaders:", err)
