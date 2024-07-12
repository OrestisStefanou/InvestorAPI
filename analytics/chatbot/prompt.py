from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from app import settings

db = SQLDatabase.from_uri(f"sqlite:///{settings.db_path}")

examples = [
    {
        "input": "Find all the balance sheets of symbol 'AAPL' and 'META' in year 2023.",
        "query": """SELECT * FROM balance_sheet WHERE symbol IN ('AAPL', 'META') AND strftime('%Y', fiscal_date_ending) = '2023';""",
    },
    {
        "input": "Find all the balance sheets of symbol 'AAPL' in year 2023.",
        "query": """SELECT * FROM balance_sheet WHERE symbol = 'AAPL' AND strftime('%Y', fiscal_date_ending) = '2023';""",
    },
    {
        "input": "Find all the income statements of symbol 'AAPL' in year 2023.",
        "query": """SELECT * FROM income_statement WHERE symbol = 'AAPL' AND strftime('%Y', fiscal_date_ending) = '2023';""",
    },
    {
        "input": "What are the available sectors?",
        "query": "SELECT DISTINCT sector FROM stock_overview WHERE sector is not null;",
    },
    {
        "input": "Can you compare the revenue of 'AAPL' and 'GOOGL' in year 2023?",
        "query": """SELECT symbol, total_revenue, fiscal_date_ending FROM income_statement WHERE symbol IN ('AAPL', 'GOOGL') AND strftime('%Y', fiscal_date_ending) = '2023';""",
    },
    {
        "input": "Which company from the 'Technology' sector had the most current assets in 2023?",
        "query": """SELECT b.symbol, b.total_current_assets
                    FROM balance_sheet b
                    INNER JOIN stock_overview s
                    ON s.symbol = b.symbol
                    WHERE s.sector = 'TECHNOLOGY' AND strftime('%Y', b.fiscal_date_ending) = '2023'
                    ORDER BY b.total_current_assets DESC LIMIT 1;
                """,
    },
    {
        "input": "Which company from the Technology sector had the highest total revenue to cost of revenue ratio in 2023?",
        "query": """
                SELECT i.symbol, i.total_revenue, i.cost_of_revenue, i.total_revenue/i.cost_of_revenue AS revenue_to_cost_ratio
                FROM income_statement i
                INNER JOIN stock_overview s
                ON i.symbol = s.symbol
                WHERE strftime('%Y', fiscal_date_ending) = '2023' AND s.sector = 'TECHNOLOGY'
                ORDER BY revenue_to_cost_ratio DESC
                LIMIT 1;
            """
    },
    {
        "input": "Which symbol had the highest average total revenue in 2023 in the TECHNOLOGY sector?",
        "query": """
                SELECT i.symbol, AVG(i.total_revenue) AS avg_total_revenue
                FROM income_statement i
                INNER JOIN stock_overview o
                ON i.symbol = o.symbol
                WHERE strftime('%Y', i.fiscal_date_ending) = '2023' AND o.sector = 'TECHNOLOGY'
                GROUP BY i.symbol
                ORDER BY avg_total_revenue DESC
                LIMIT 1
            """
    },
    {
        "input": "Which symbol had the highest average total revenue in 2023 from each sector?",
        "query": """
            WITH avg_revenue_per_company AS (
                SELECT
                    i.symbol,
                    AVG(i.total_revenue) AS avg_revenue,
                    s.sector
                FROM
                    income_statement i
                INNER JOIN
                    stock_overview s ON i.symbol = s.symbol
                WHERE strftime('%Y', i.fiscal_date_ending) = '2023'
                GROUP BY
                    i.symbol, s.sector
            ),
            max_avg_revenue_per_sector AS (
                SELECT
                    sector,
                    MAX(avg_revenue) AS max_avg_revenue
                FROM
                    avg_revenue_per_company
                GROUP BY
                    sector
            )
            SELECT
                arc.symbol,
                arc.sector,
                arc.avg_revenue
            FROM
                avg_revenue_per_company arc
            JOIN
                max_avg_revenue_per_sector marp
            ON
                arc.sector = marp.sector AND arc.avg_revenue = marp.max_avg_revenue;
        """
    },
    {
        "input": "Which sector had the highest total revenue in 2023?",
        "query": """
            WITH total_revenue_per_company AS (
                SELECT
                    i.symbol,
                    SUM(i.total_revenue) AS total_revenue,
                    s.sector
                FROM
                    income_statement i
                INNER JOIN
                    stock_overview s ON i.symbol = s.symbol
                WHERE strftime('%Y', i.fiscal_date_ending) = '2023'
                GROUP BY
                    i.symbol, s.sector
            ),
            total_revenue_per_sector AS (
                SELECT
                    sector,
                    SUM(total_revenue) AS total_revenue
                FROM
                    total_revenue_per_company
                GROUP BY
                    sector
            )
            SELECT
                sector,
                total_revenue
            FROM
                total_revenue_per_sector
            ORDER BY
                total_revenue DESC
            LIMIT 1;
        """
    },
    {
        "input": "Which symbol has the most cash?",
        "query": """
            WITH latest_fiscal_date AS (
                SELECT
                    symbol,
                    MAX(fiscal_date_ending) AS latest_fiscal_date
                FROM
                    balance_sheet
                GROUP BY
                    symbol
            ),
            latest_cash_equivalents AS (
                SELECT
                    bs.symbol,
                    bs.cash_and_cash_equivalents_at_carrying_value,
                    lfd.latest_fiscal_date
                FROM
                    balance_sheet bs
                JOIN
                    latest_fiscal_date lfd
                ON
                    bs.symbol = lfd.symbol AND bs.fiscal_date_ending = lfd.latest_fiscal_date
            )
            SELECT
                symbol,
                cash_and_cash_equivalents_at_carrying_value
            FROM
                latest_cash_equivalents
            ORDER BY
                cash_and_cash_equivalents_at_carrying_value DESC
            LIMIT 1;
        """
    },
    {
        "input": "Which symbol has the most short term debt?",
        "query": """
            WITH latest_fiscal_date AS (
                SELECT
                    symbol,
                    MAX(fiscal_date_ending) AS latest_fiscal_date
                FROM
                    balance_sheet
                GROUP BY
                    symbol
            ),
            latest_short_term_debt AS (
                SELECT
                    bs.symbol,
                    bs.short_term_debt,
                    lfd.latest_fiscal_date
                FROM
                    balance_sheet bs
                JOIN
                    latest_fiscal_date lfd
                ON
                    bs.symbol = lfd.symbol AND bs.fiscal_date_ending = lfd.latest_fiscal_date
            )
            SELECT
                symbol,
                short_term_debt
            FROM
                latest_short_term_debt
            ORDER BY
                short_term_debt DESC
            LIMIT 1;
        """
    },
    {
        "input": "Which symbol had the most cash in 2023?",
        "query": """SELECT symbol, cash_and_cash_equivalents_at_carrying_value FROM balance_sheet WHERE strftime('%Y', fiscal_date_ending) = '2023' ORDER BY cash_and_cash_equivalents_at_carrying_value DESC LIMIT 1;""",
    },
    {
        "input": "Compare the price movement of AAPL and MSFT the last year",
        "query": """"
                    SELECT s1.symbol, s1.close_price AS aapl_close_price, s2.close_price AS msft_close_price, s1.registered_date
                    FROM stock_time_series s1
                    JOIN stock_time_series s2 ON s1.registered_date = s2.registered_date
                    WHERE s1.symbol = 'AAPL' AND s2.symbol = 'MSFT'
                    ORDER BY s1.registered_date_ts DESC
                    LIMIT 100;
                """,
    },
    {
        "input": "Which sector had the highest average quarterly earnings growth year over year?",
        "query": """"
                SELECT sector
                FROM stock_overview
                WHERE sector!=''
                GROUP BY sector
                ORDER BY AVG(quarterly_earnings_growth_yoy)
                LIMIT 1
            """,
    },
    {
        "input": "For which superinvestors do you have portfolio data?",
        "query": """"
                SELECT DISTINCT super_investor FROM super_investor_portfolio_holding;
            """,
    },
    {
        "input": "Can you give me the portfolio holdings of super investor Warren Buffet?",
        "query": """"
                SELECT * FROM super_investor_portfolio_holding WHERE super_investor='Warren Buffet';
            """,
    },
    {
        "input": "Can you give me the portfolio sector analysis of super investor Warren Buffet?",
        "query": """"
                SELECT * FROM super_investor_portfolio_sector_analysis WHERE super_investor='Warren Buffet';
            """,
    },
    {
        "input": "Which are the top 10 most hold stocks from super investors?",
        "query": """"
                SELECT * FROM super_investor_grand_portfolio ORDER BY ownership_count DESC LIMIT 10;
            """,
    }
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(openai_api_key=settings.openai_key),
    FAISS,
    k=5,
    input_keys=["input"],
)

context = db.get_context()["table_info"]

system_prefix = """You are a financial advisor agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
If you get an error while executing a query, rewrite the query and try again.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
If the question does not seem related to the database or investing related, just return "I don't know" as the answer.
The database context is as follows:
{context}

Here are some examples of user inputs and their corresponding SQL queries:"""

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k", "context"],
    prefix=system_prefix,
    suffix="",
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
