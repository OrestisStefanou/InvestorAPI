from typing import Tuple, Any, Optional, List

from app.repos.sql_repo import SqlRepo
from app.domain.cash_flow import CashFlow

class CashFlowRepo(SqlRepo):
    """
    Repo for cash_flow table
    """
    @classmethod
    def _create_row_tuple_from_model(
        cls,
        cash_flow: CashFlow,
    ) -> Tuple[Any]:
        return (
            cash_flow.symbol,
            cash_flow.fiscal_date_ending,
            cash_flow.reported_currency,
            cash_flow.payments_for_operating_activities,
            cash_flow.operating_cashflow,
            cash_flow.proceeds_from_operating_activities,
            cash_flow.change_in_operating_liabilities,
            cash_flow.change_in_operating_assets,
            cash_flow.depreciation_depletion_and_amortization,
            cash_flow.capital_expenditures,
            cash_flow.change_in_receivables,
            cash_flow.change_in_inventory,
            cash_flow.profit_loss,
            cash_flow.cashflow_from_investment,
            cash_flow.cashflow_from_financing,
            cash_flow.proceeds_from_repayments_of_short_term_debt,
            cash_flow.payments_for_repurchase_of_common_stock,
            cash_flow.payments_for_repurchase_of_equity,
            cash_flow.payments_for_repurchase_of_preferred_stock,
            cash_flow.dividend_payout,
            cash_flow.dividend_payout_common_stock,
            cash_flow.dividend_payout_preferred_stock,
            cash_flow.proceeds_from_issuance_of_common_stock,
            cash_flow.proceeds_from_issuance_of_long_term_debt_and_capital_securities_net,
            cash_flow.proceeds_from_issuance_of_preferred_stock,
            cash_flow.proceeds_from_repurchase_of_equity,
            cash_flow.proceeds_from_sale_of_treasury_stock,
            cash_flow.change_in_cash_and_cash_equivalents,
            cash_flow.change_in_exchange_rate,
            cash_flow.net_income,
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> CashFlow:
        return CashFlow(
            symbol=row[0],
            fiscal_date_ending=row[1],
            reported_currency=row[2],
            payments_for_operating_activities=row[3],
            operating_cashflow=row[4],
            proceeds_from_operating_activities=row[5],
            change_in_operating_liabilities=row[6],
            change_in_operating_assets=row[7],
            depreciation_depletion_and_amortization=row[8],
            capital_expenditures=row[9],
            change_in_receivables=row[10],
            change_in_inventory=row[11],
            profit_loss=row[12],
            cashflow_from_investment=row[13],
            cashflow_from_financing=row[14],
            proceeds_from_repayments_of_short_term_debt=row[15],
            payments_for_repurchase_of_common_stock=row[16],
            payments_for_repurchase_of_equity=row[17],
            payments_for_repurchase_of_preferred_stock=row[18],
            dividend_payout=row[19],
            dividend_payout_common_stock=row[20],
            dividend_payout_preferred_stock=row[21],
            proceeds_from_issuance_of_common_stock=row[22],
            proceeds_from_issuance_of_long_term_debt_and_capital_securities_net=row[23],
            proceeds_from_issuance_of_preferred_stock=row[24],
            proceeds_from_repurchase_of_equity=row[25],
            proceeds_from_sale_of_treasury_stock=row[26],
            change_in_cash_and_cash_equivalents=row[27],
            change_in_exchange_rate=row[28],
            net_income=row[29],
        )
    
    def add_cash_flow(
        self,
        cash_flow: CashFlow
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO cash_flow VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', self._create_row_tuple_from_model(cash_flow)
            )

    def get_cash_flows_for_symbol(
        self,
        symbol: str,
    ) -> Optional[List[CashFlow]]:
        cur  = self._db_conn.cursor()
        query = '''
            SELECT
                symbol,
                fiscal_date_ending,
                reported_currency,
                payments_for_operating_activities,
                operating_cashflow,
                proceeds_from_operating_activities,
                change_in_operating_liabilities,
                change_in_operating_assets,
                depreciation_depletion_and_amortization,
                capital_expenditures,
                change_in_receivables,
                change_in_inventory,
                profit_loss,
                cashflow_from_investment,
                cashflow_from_financing,
                proceeds_from_repayments_of_short_term_debt,
                payments_for_repurchase_of_common_stock,
                payments_for_repurchase_of_equity,
                payments_for_repurchase_of_preferred_stock,
                dividend_payout,
                dividend_payout_common_stock,
                dividend_payout_preferred_stock,
                proceeds_from_issuance_of_common_stock,
                proceeds_from_issuance_of_long_term_debt_and_capital_securities_net,
                proceeds_from_issuance_of_preferred_stock,
                proceeds_from_repurchase_of_equity,
                proceeds_from_sale_of_treasury_stock,
                change_in_cash_and_cash_equivalents,
                change_in_exchange_rate,
                net_income
            FROM cash_flow
            WHERE symbol = ?
        '''

        query_params = (symbol, )
        rows = cur.execute(query, query_params).fetchall()
        
        if len(rows) == 0:
            return None
         
        return [
            self._create_model_from_row(row)
            for row in rows
        ]

    def delete_cash_flows_of_symbol(self, symbol: str) -> None:
        with self._db_conn as con:
            con.execute(
                '''
                DELETE FROM cash_flow WHERE symbol = ?
                ''', (symbol, )
            )
