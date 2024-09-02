import datetime
import json
import os

import pandas as pd
import pyodbc


class DataAccessMSSQL:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pyodbc.connect(
            'DRIVER=ODBC Driver 17 for SQL Server;'
            'SERVER=your_server_name;'
            'DATABASE=StockData;'
            'Trusted_Connection=yes;'
            
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='StockData' AND xtype='U')
            CREATE TABLE StockData (
                Date DATE,
                Open FLOAT,
                High FLOAT,
                Low FLOAT,
                Close FLOAT,
                Volume FLOAT,
                Symbol NVARCHAR(50)
            )
        ''')
        self.conn.commit()

    def check_data_exists(self, symbol):
        self.cursor.execute("SELECT COUNT(*) FROM StockData WHERE Symbol=?", (symbol,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def get_latest_date(self, symbol):
        self.cursor.execute("SELECT MAX(Date) FROM StockData WHERE Symbol=?", (symbol,))
        latest_date = self.cursor.fetchone()[0]
        return datetime.datetime.strptime(latest_date, "%Y-%m-%d").date()

    def insert_data(self, index, row, symbol):
        self.cursor.execute("INSERT INTO StockData VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (index.strftime("%Y-%m-%d"), row['Open'], row['High'], row['Low'], row['Close'],
                             row['Volume'], symbol))
        self.conn.commit()

    def load_data(self, symbol, start_date):
        self.cursor.execute("SELECT * FROM StockData WHERE Symbol=? AND Date>=?", (symbol, start_date))
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol'])

    def commit_changes(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def create_prompt_table(self):
        self.cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='PromptLog' AND xtype='U')
            CREATE TABLE PromptLog (
                Symbol NVARCHAR(50),
                Prompt NVARCHAR(MAX),
                Insights NVARCHAR(MAX),
                Date DATE,
                Markdown NVARCHAR(MAX),
                Uptrend FLOAT,
                Downtrend FLOAT,
                NeutralTrend FLOAT
            )
        ''')
        self.conn.commit()

    def insert_prompt_data(self, stock_code, prompt, insights_llm, date):
        insights = json.loads(insights_llm)

        # Extract values with default fallback
        markdown = insights.get("markdown", "")
        uptrend = float(insights.get("Uptrend", None))
        if uptrend is not None and uptrend < 1:
            uptrend *= 100

        downtrend = float(insights.get("DownTrend", None))
        if downtrend is not None and downtrend < 1:
            downtrend *= 100

        neutraltrend = float(insights.get("NeutralTrend", None))
        if neutraltrend is not None and neutraltrend < 1:
            neutraltrend *= 100

        # Combine insights into a single string
        self.cursor.execute("INSERT INTO PromptLog VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (stock_code, prompt, insights_llm, date, markdown, uptrend, downtrend, neutraltrend))
        self.conn.commit()

    def get_Insights_stockcode(self, date, stock_code):
        self.cursor.execute("SELECT * FROM PromptLog WHERE Date=? AND Symbol=?", (date, stock_code))
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns=['Symbol', 'Prompt', 'Insights', 'Date', 'Markdown', 'Uptrend', 'Downtrend', 'NeutralTrend'])