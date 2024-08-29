import requests
import pandas as pd
import ta  # Technical Analysis library
import yfinance as yf
import datetime


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
        end_date = datetime.date.today()
        self.data = yf.download(self.symbol, start=start_date, end=end_date)
        self.df = pd.DataFrame(self.data)

    def calculate_indicators(self):
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
        return {
            'Weekly Risk (%)': self.weekly_risk * 100,
            'Monthly Risk (%)': self.monthly_risk * 100,
            'Weekly Reward (₹)': self.weekly_reward_amount,
            'Monthly Reward (₹)': self.monthly_reward_amount
        }


