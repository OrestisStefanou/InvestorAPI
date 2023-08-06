from typing import Tuple, Any, Optional, List

from app.repos.sql_repo import SqlRepo
from app.domain.date import Date
from app.domain.income_statement import IncomeStatement

class IncomeStatementRepo(SqlRepo):
    """
    Repo for income_statement table
    """
    @classmethod
    def _create_row_tuple_from_model(
        cls,
        income_statement: IncomeStatement,
    ) -> Tuple[Any]:
        return (
            income_statement.symbol,
            income_statement.fiscal_date_ending,
            income_statement.reported_currency,
            income_statement.gross_profit,
            income_statement.total_revenue,
            income_statement.cost_of_revenue,
            income_statement.cost_of_goods_and_services_sold,
            income_statement.operating_income,
            income_statement.selling_general_and_administrative,
            income_statement.research_and_development,
            income_statement.operating_expenses,
            income_statement.investment_income_net,
            income_statement.net_interest_income,
            income_statement.interest_income,
            income_statement.interest_expense,
            income_statement.non_interest_income,
            income_statement.other_non_operating_income,
            income_statement.depreciation,
            income_statement.depreciation_and_amortization,
            income_statement.income_before_tax,
            income_statement.income_tax_expense,
            income_statement.interest_and_debt_expense,
            income_statement.net_income_from_continuing_operations,
            income_statement.comprehensive_income_net_of_tax,
            income_statement.ebit,
            income_statement.ebitda,
            income_statement.net_income,
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> IncomeStatement:
        return IncomeStatement(
            symbol=row[0],
            fiscal_date_ending=row[1],
            reported_currency=row[2],
            gross_profit=row[3],
            total_revenue=row[4],
            cost_of_revenue=row[5],
            cost_of_goods_and_services_sold=row[6],
            operating_income=row[7],
            selling_general_and_administrative=row[8],
            research_and_development=row[9],
            operating_expenses=row[10],
            investment_income_net=row[11],
            net_interest_income=row[12],
            interest_income=row[13],
            interest_expense=row[14],
            non_interest_income=row[15],
            other_non_operating_income=row[16],
            depreciation=row[17],
            depreciation_and_amortization=row[18],
            income_before_tax=row[19],
            income_tax_expense=row[20],
            interest_and_debt_expense=row[21],
            net_income_from_continuing_operations=row[22],
            comprehensive_income_net_of_tax=row[23],
            ebit=row[24],
            ebitda=row[25],
            net_income=row[26],
        )
    
    def add_income_statement(
        self,
        income_statment: IncomeStatement
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO income_statement VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', self._create_row_tuple_from_model(income_statment)
            )

    def get_income_statements_for_symbol(
        self,
        symbol: str,
    ) -> Optional[List[IncomeStatement]]:
        cur  = self._db_conn.cursor()
        query = '''
            SELECT
                symbol,
                fiscal_date_ending,
                reported_currency,
                gross_profit,
                total_revenue,
                cost_of_revenue,
                cost_of_goods_and_services_sold,
                operating_income,
                selling_general_and_administrative,
                research_and_development,
                operating_expenses,
                investment_income_net,
                net_interest_income,
                interest_income,
                interest_expense,
                non_interest_income,
                other_non_operating_income,
                depreciation,
                depreciation_and_amortization,
                income_before_tax,
                income_tax_expense,
                interest_and_debt_expense,
                net_income_from_continuing_operations,
                comprehensive_income_net_of_tax,
                ebit,
                ebitda,
                net_income
            FROM income_statement
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

    def delete_income_statements_of_symbol(self, symbol: str) -> None:
        with self._db_conn as con:
            con.execute(
                '''
                DELETE FROM income_statement WHERE symbol = ?
                ''', (symbol, )
            )
