import os
import google.generativeai as genai

class LLM:
    def __init__(self, api_key_path):
        with open(api_key_path, 'r') as file:
            api_key = file.read().strip()
        os.environ["GEMINI_API_KEY"] = api_key
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.45,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json"
            },
            system_instruction="ACT as stock market expert and skilled trader with over 10 years of experience in  analyzing Indian Market stock market",
        )

    def generate_prompt(self, stock_analysis):
        df = stock_analysis.df
        weekly_risk = stock_analysis.weekly_risk
        monthly_risk = stock_analysis.monthly_risk
        weekly_reward_amount = stock_analysis.weekly_reward_amount
        monthly_reward_amount = stock_analysis.monthly_reward_amount

        prompt = f"""
        Role: You are a financial analyst specializing in the Indian stock market.

        Context: You have access to the following Technical Indecator data for a stock listed on an Indian exchange (e.g., NSE or BSE):
        
        **RSI (Relative Strength Index)**:
        {df['rsi'].tail(14).to_list()}

        **MACD (Moving Average Convergence Divergence)**:
        {df['macd'].tail(14).to_list()}

        **MACD Signal**:
        {df['macd_signal'].tail(14).to_list()}

        **MACD Difference**:
        {df['macd_diff'].tail(14).to_list()}

        **Exponential Moving Average (EMA)**:
        {df['ema'].tail(14).to_list()}

        **ADX (Average Directional Index)**:
        {df['adx'].tail(14).to_list()}
        
        **ATR (Average True Range)**:
        {df['atr'].tail(14).to_list()}
        
        **Bollinger Bands**:
        Upper Band: {df['bbands_upper'].tail(14).to_list()}
        Middle Band: {df['bbands_middle'].tail(14).to_list()}
        Lower Band: {df['bbands_lower'].tail(14).to_list()}

        **On-Balance Volume (OBV)**:
        {df['obv'].tail(14).to_list()}

        **Rate of Change (ROC)**:
        {df['roc'].tail(14).to_list()}

        **Weekly Return**:
        {df['weekly_return'].tail(14).to_list()}

        **Monthly Return**:
        {df['monthly_return'].tail(14).to_list()}
        
       

        
        Tasks:

        Basic Analysis: Analyze the stock's historical performance by identifying key trends, patterns, and notable movements. Focus on elements specific to the Indian market context.
        Performance Rating: Provide a rating of the stock’s performance on a scale of 1-10, where 1 indicates very poor performance and 10 indicates excellent performance. Justify your rating.
        Outcome Assessment: Estimate the probability percentages for three possible outcomes over the next  7 days and 30 days
        Positive: Increase in stock price
        Negative: Decrease in stock price
        Neutral: Little or no change in stock price
        Return Calculation: Calculate the probable return (gain) and loss (decline) percentages for each outcome (positive, negative, neutral), considering market-specific factors in India.
        Reasoning Explanation: Explain the reasoning behind your analysis, rating, probability assessments, and return calculations. Consider the provided historical data, technical indicators, and relevant market conditions (e.g., recent economic events, government policies, sector-specific news)
        Please format your insights in the following JSON structure:
        {{
            "markdown": "your analysis of stock in markdown",
            "Uptrend": probability of upternd,
            "DownTrend": probability of DownTrend,
            "NeutralTrend": probability of Neutral trend,
        }}
        
        """
        return prompt
        # **ARIMA Forcast**:
        # {stock_analysis.forcastedPrice.to_list()}
        
        # **GARCH Volatility**:
        # {stock_analysis.forcastedVolatility.tolist()}

    def get_insights(self, prompt):
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        return response.text
