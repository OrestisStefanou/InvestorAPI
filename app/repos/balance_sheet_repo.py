from typing import Tuple, Any, Optional, List

from app.repos.sql_repo import SqlRepo
from app.domain.balance_sheet import BalanceSheet

class BalanceSheetRepo(SqlRepo):
    """
    Repo for income_statement table
    """
    @classmethod
    def _create_row_tuple_from_model(
        cls,
        balance_sheet: BalanceSheet,
    ) -> Tuple[Any]:
        return (
            balance_sheet.symbol,
            balance_sheet.fiscal_date_ending,
            balance_sheet.reported_currency,
            balance_sheet.total_assets,
            balance_sheet.total_current_assets,
            balance_sheet.cash_and_cash_equivalents_at_carrying_value,
            balance_sheet.cash_and_short_term_investments,
            balance_sheet.inventory,
            balance_sheet.current_net_receivables,
            balance_sheet.total_non_current_assets,
            balance_sheet.property_plant_equipment,
            balance_sheet.accumulated_depreciation_amortization_ppe,
            balance_sheet.intangible_assets,
            balance_sheet.intangible_assets_excluding_goodwill,
            balance_sheet.goodwill,
            balance_sheet.investments,
            balance_sheet.long_term_investments,
            balance_sheet.short_term_investments,
            balance_sheet.other_current_assets,
            balance_sheet.other_non_current_assets,
            balance_sheet.total_liabilities,
            balance_sheet.total_current_liabilities,
            balance_sheet.current_accounts_payable,
            balance_sheet.deferred_revenue,
            balance_sheet.current_debt,
            balance_sheet.short_term_debt,
            balance_sheet.total_non_current_liabilities,
            balance_sheet.capital_lease_obligations,
            balance_sheet.long_term_debt,
            balance_sheet.current_long_term_debt,
            balance_sheet.long_term_debt_noncurrent,
            balance_sheet.short_long_term_debt_total,
            balance_sheet.other_current_liabilities,
            balance_sheet.other_non_current_liabilities,
            balance_sheet.total_shareholder_equity,
            balance_sheet.treasury_stock,
            balance_sheet.retained_earnings,
            balance_sheet.common_stock,
            balance_sheet.common_stock_shares_outstanding,
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> BalanceSheet:
        return BalanceSheet(
            symbol=row[0],
            fiscal_date_ending=row[1],
            reported_currency=row[2],
            total_assets=row[3],
            total_current_assets=row[4],
            cash_and_cash_equivalents_at_carrying_value=row[5],
            cash_and_short_term_investments=row[6],
            inventory=row[7],
            current_net_receivables=row[8],
            total_non_current_assets=row[9],
            property_plant_equipment=row[10],
            accumulated_depreciation_amortization_ppe=row[11],
            intangible_assets=row[12],
            intangible_assets_excluding_goodwill=row[13],
            goodwill=row[14],
            investments=row[15],
            long_term_investments=row[16],
            short_term_investments=row[17],
            other_current_assets=row[18],
            other_non_current_assets=row[19],
            total_liabilities=row[20],
            total_current_liabilities=row[21],
            current_accounts_payable=row[22],
            deferred_revenue=row[23],
            current_debt=row[24],
            short_term_debt=row[25],
            total_non_current_liabilities=row[26],
            capital_lease_obligations=row[27],
            long_term_debt=row[28],
            current_long_term_debt=row[29],
            long_term_debt_noncurrent=row[30],
            short_long_term_debt_total=row[31],
            other_current_liabilities=row[32],
            other_non_current_liabilities=row[33],
            total_shareholder_equity=row[34],
            treasury_stock=row[35],
            retained_earnings=row[36],
            common_stock=row[37],
            common_stock_shares_outstanding=row[38],
        )
    
    def add_balance_sheet(
        self,
        balance_sheet: BalanceSheet
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO balance_sheet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', self._create_row_tuple_from_model(balance_sheet)
            )

    def get_balance_sheets_for_symbol(
        self,
        symbol: str,
    ) -> Optional[List[BalanceSheet]]:
        cur  = self._db_conn.cursor()
        query = '''
            SELECT
                symbol,
                fiscal_date_ending,
                reported_currency,
                total_assets,
                total_current_assets,
                cash_and_cash_equivalents_at_carrying_value,
                cash_and_short_term_investments,
                inventory,
                current_net_receivables,
                total_non_current_assets,
                property_plant_equipment,
                accumulated_depreciation_amortization_ppe,
                intangible_assets,
                intangible_assets_excluding_goodwill,
                goodwill,
                investments,
                long_term_investments,
                short_term_investments,
                other_current_assets,
                other_non_current_assets,
                total_liabilities,
                total_current_liabilities,
                current_accounts_payable,
                deferred_revenue,
                current_debt,
                short_term_debt,
                total_non_current_liabilities,
                capital_lease_obligations,
                long_term_debt,
                current_long_term_debt,
                long_term_debt_noncurrent,
                short_long_term_debt_total,
                other_current_liabilities,
                other_non_current_liabilities,
                total_shareholder_equity,
                treasury_stock,
                retained_earnings,
                common_stock,
                common_stock_shares_outstanding
            FROM balance_sheet
            WHERE symbol = ?
            ORDER BY DATE(fiscal_date_ending) DESC
        '''

        query_params = (symbol, )
        rows = cur.execute(query, query_params).fetchall()
        
        if len(rows) == 0:
            return None
         
        return [
            self._create_model_from_row(row)
            for row in rows
        ]

    def delete_balance_sheets_of_symbol(self, symbol: str) -> None:
        with self._db_conn as con:
            con.execute(
                '''
                DELETE FROM balance_sheet WHERE symbol = ?
                ''', (symbol, )
            )
