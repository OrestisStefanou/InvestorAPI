import sqlite3

import pandas as pd

conn = sqlite3.connect('app/database/ibd.db')

query = '''
SELECT income_statement.*, balance_sheet.*, cash_flow.*
FROM income_statement
INNER JOIN balance_sheet
ON income_statement.fiscal_date_ending = balance_sheet.fiscal_date_ending AND balance_sheet.symbol = 'META'
INNER JOIN cash_flow
ON income_statement.fiscal_date_ending = cash_flow.fiscal_date_ending AND cash_flow.symbol = 'META'
WHERE income_statement.symbol = 'META'
'''
df = pd.read_sql(query, conn)

# Drop columns with duplicated names
df = df.loc[:, ~df.columns.duplicated()]
print(df)

conn.close()
