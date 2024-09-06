import datetime
import json
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
            
            def check_data_exists_for_date(self, symbol, date):
                self.cursor.execute("SELECT COUNT(*) FROM StockData WHERE Symbol=? AND Date=?", (symbol, date))
                result = self.cursor.fetchone()
                return result[0] > 0

            def insert_data(self, index, row, symbol):
                if self.check_data_exists_for_date(symbol,index.strftime("%Y-%m-%d")) == False:
                    self.cursor.execute("INSERT INTO StockData VALUES (?, ?, ?, ?, ?, ?, ?)",
                                        (index.strftime("%Y-%m-%d"), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], symbol))
               
                    

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
                                          (Symbol TEXT, Prompt TEXT, Insights TEXT, Date TEXT,Markdown TEXT, Uptrend REAL, Downtrend REAL, NeutralTrend REAL)''')

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
                                        (stock_code, prompt, insights_llm, date,markdown, uptrend, downtrend, neutraltrend))
                self.conn.commit()
                
            def get_Insights_stockcode(self, date, stock_code):
                #date = date.date()  # Extract only the date part
                self.cursor.execute("SELECT * FROM PromptLog WHERE Date=? AND Symbol=?", (date, stock_code))
                rows = self.cursor.fetchall()
                return pd.DataFrame(rows, columns=['Symbol', 'Prompt', 'Insights', 'Date', 'Markdown', 'Uptrend', 'Downtrend', 'NeutralTrend'])
            
            def get_all_Insights(self):
                #date = date.date()  # Extract only the date part
                self.cursor.execute("SELECT * FROM PromptLog")
                rows = self.cursor.fetchall()
                return pd.DataFrame(rows, columns=['Symbol', 'Prompt', 'Insights', 'Date', 'Markdown', 'Uptrend', 'Downtrend', 'NeutralTrend'])
            
            def get_records_by_stock_code(self, stock_code):
                self.cursor.execute("SELECT * FROM StockData WHERE Symbol=? ", (stock_code + ".NS",))
                stock_data_rows = self.cursor.fetchall()
                stock_data_df = pd.DataFrame(stock_data_rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol'])
                stock_data_df['Date'] = pd.to_datetime(stock_data_df['Date'], format='%Y-%m-%d')

                # Sort the DataFrame by Date in descending order
                stock_data_df = stock_data_df.sort_values(by='Date', ascending=False)

                # Take only the first 60 records
                stock_data_df = stock_data_df.head(60)
                self.cursor.execute("SELECT * FROM PromptLog WHERE Symbol=? ORDER BY Date DESC", (stock_code,))
                prompt_log_rows = self.cursor.fetchall()
                prompt_log_df = pd.DataFrame(prompt_log_rows, columns=['Symbol', 'Prompt', 'Insights', 'Date', 'Markdown', 'Uptrend', 'Downtrend', 'NeutralTrend'])

                return stock_data_df, prompt_log_df