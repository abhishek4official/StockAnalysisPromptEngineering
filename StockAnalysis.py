import requests
import pandas as pd
import ta  # Technical Analysis library
import yfinance as yf
import datetime
import os
import csv
import sqlite3
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from arch import arch_model

import DataAccess


class StockAnalysis:
    def __init__(self, symbol, investment_amount=10000):
        self.symbol = symbol
        self.investment_amount = investment_amount
        self.data = None
        self.df = None
        self.weekly_risk = None
        self.monthly_risk = None
        self.weekly_reward = None
        self.monthly_reward = None
        self.weekly_reward_amount = None
        self.monthly_reward_amount = None

    def download_data(self):
        start_date = datetime.date.today() - datetime.timedelta(days=365)
        
        # Create an instance of DataAccess
        data_access = DataAccess.DataAccess()
        data_access.connect()
        data_access.create_table()
        
        # Check if data exists for the symbol in the database
        if data_access.check_data_exists(self.symbol):
            # Get the latest date from the database
            latest_date = data_access.get_latest_date(self.symbol)
            
            # Check if the latest date is today
            if latest_date < datetime.date.today() - datetime.timedelta(days=1):
                # Download data for the entire period
                start_date = datetime.date.today() - datetime.timedelta(days=365)
                end_date = datetime.date.today()
                self.data = yf.download(self.symbol, start=start_date, end=end_date)
                self.df = pd.DataFrame(self.data)

                # Insert data into the database
                for index, row in self.df.iterrows():
                    data_access.insert_data(index, row, self.symbol)

                # Commit the changes to the database
                data_access.commit_changes()
 
        else:
            # Download data for the entire period
            end_date = datetime.date.today()
            self.data = yf.download(self.symbol, start=start_date, end=end_date)
            self.df = pd.DataFrame(self.data)
            
            for index, row in self.df.iterrows():
                data_access.insert_data(index, row, self.symbol)
            
            # Commit the changes to the database
            data_access.commit_changes()

        # Load data from the database for the last 1 year
        self.df = data_access.load_data(self.symbol, start_date)

        # Close the database connection
        data_access.close_connection()

    def calculate_indicators(self):
        window = 20  # Set the window value according to your requirements
        self.df['sma'] = ta.trend.SMAIndicator(self.df['Close'], window=window).sma_indicator()
        bb=ta.volatility.BollingerBands(self.df['Close'])
        self.df['bbands_middle']=bb.bollinger_mavg()
        self.df['bbands_upper']= bb.bollinger_hband()
        self.df['bbands_lower'] =bb.bollinger_lband()
        self.df['atr'] = ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close']).average_true_range()
        self.df['obv'] = ta.volume.OnBalanceVolumeIndicator(self.df['Close'], self.df['Volume']).on_balance_volume()
        self.df['roc'] = ta.momentum.ROCIndicator(self.df['Close']).roc()
        self.df['rsi'] = ta.momentum.RSIIndicator(self.df['Close']).rsi()
        macd = ta.trend.MACD(self.df['Close'])
        self.df['macd'] = macd.macd()
        self.df['macd_signal'] = macd.macd_signal()
        self.df['macd_diff'] = macd.macd_diff()
        self.df['ema'] = ta.trend.EMAIndicator(self.df['Close']).ema_indicator()
        adx = ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'])
        self.df['adx'] = adx.adx()
        self.df['weekly_return'] = self.df['Close'].pct_change(7)
        self.df['monthly_return'] = self.df['Close'].pct_change(30)

    def calculate_risk_reward(self):
        self.weekly_risk = self.df['weekly_return'].std()
        self.monthly_risk = self.df['monthly_return'].std()
        self.weekly_reward = self.df['weekly_return'].mean()
        self.monthly_reward = self.df['monthly_return'].mean()
        self.weekly_reward_amount = self.investment_amount * self.weekly_reward
        self.monthly_reward_amount = self.investment_amount * self.monthly_reward

    def get_results(self):
        results= {
            'Weekly Risk (%)': str(self.weekly_risk * 100),
            'Monthly Risk (%)': str(self.monthly_risk * 100),
            'Weekly Reward (₹)': str(self.weekly_reward_amount),
            'Monthly Reward (₹)': str(self.monthly_reward_amount)
        }
        result_string = ""
        for key, value in results.items():
            result_string += f"{key}: {value}\n"
        return result_string

    def get_ARIMA_AND_GARCH_Forcast(self):
        # Step 2: Prepare the data for ARIMA modeling
        close_prices = self.df['Close']
        close_prices = pd.to_numeric(close_prices, errors='coerce')
        close_prices = close_prices.dropna()

        # Step 3: Check for stationarity
        result = adfuller(close_prices)
        print('ADF Statistic:', result[0])
        print('p-value:', result[1])

        if result[1] > 0.05:
            print("Series is not stationary. Differencing the series.")
            close_prices_diff = close_prices.diff().dropna()
        else:
            close_prices_diff = close_prices

        # Step 4: Fit the ARIMA model
        try:
            model = ARIMA(close_prices_diff, order=(5, 1, 0))  # Adjust (p, d, q) as needed
            model_fit = model.fit()
        except Exception as e:
            print(f"Error fitting ARIMA model: {e}")
        print("2")
        # Step 5: Fit the GARCH model to the residuals of the ARIMA model
        residuals = model_fit.resid
        garch_model = arch_model(residuals, vol='Garch', p=1, q=1)
        garch_fit = garch_model.fit(disp='off')

        # Step 6: Forecast future values using ARIMA
        forecast_steps = 30  # Number of days to forecast
        forecast_diff = model_fit.forecast(steps=forecast_steps)
        last_value = close_prices.iloc[-1]
        forecast = last_value + forecast_diff.cumsum()
        print("2")
        # Step 7: Forecast volatility using GARCH
        garch_forecast = garch_fit.forecast(horizon=forecast_steps)
        volatility = garch_forecast.variance.values[-1, :]
        
        self.forcastedPrice=forecast.tail(forecast_steps)
        
        self.forcastedVolatility = volatility[-forecast_steps:]
        print("1")
        
        
        
