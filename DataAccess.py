import datetime
import os
import sqlite3

import pandas as pd


class DataAccess:
            def __init__(self):
                self.conn = None
                self.cursor = None

            def connect(self):
                if not os.path.exists('db'):
                    os.makedirs('db')
                self.conn = sqlite3.connect('db/StockData.db')
                self.cursor = self.conn.cursor()

            def create_table(self):
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS StockData
                                      (Date TEXT, Open REAL, High REAL, Low REAL, Close REAL, Volume REAL, Symbol TEXT)''')

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

            def load_data(self, symbol, start_date):
                self.cursor.execute("SELECT * FROM StockData WHERE Symbol=? AND Date>=?", (symbol, start_date))
                rows = self.cursor.fetchall()
                return pd.DataFrame(rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol'])

            def commit_changes(self):
                self.conn.commit()

            def close_connection(self):
                self.conn.close()
                
            def create_prompt_table(self):
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS PromptLog
                                          (Symbol TEXT, Prompt TEXT, Insights TEXT, Date TEXT)''')

            def insert_prompt_data(self, stock_code, prompt, insights, date):
                self.cursor.execute("INSERT INTO PromptLog VALUES (?, ?, ?, ?)",
                                        (stock_code, prompt, insights, date))
                self.conn.commit()
                
            def get_Insights_stockcode(self, date, stock_code):
                #date = date.date()  # Extract only the date part
                self.cursor.execute("SELECT * FROM PromptLog WHERE Date=? AND Symbol=?", (date, stock_code))
                rows = self.cursor.fetchall()
                return pd.DataFrame(rows, columns=['Symbol', 'Prompt', 'Insights', 'Date'])