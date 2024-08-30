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
            }
        )

    def generate_prompt(self, stock_analysis):
        df = stock_analysis.df
        weekly_risk = stock_analysis.weekly_risk
        monthly_risk = stock_analysis.monthly_risk
        weekly_reward_amount = stock_analysis.weekly_reward_amount
        monthly_reward_amount = stock_analysis.monthly_reward_amount

        prompt = f"""
        Asume As: You are a stock expert and skilled trader. You have been analyzing the stock market for the past 10 years.
        Based on the historical stock data and technical analysis, here are the key metrics for the given stock over the past two weeks:
        Data for the past 14 days:
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

        
        Question:
        Analyze the current state of my stock investment by evaluating its risk and reward factors. Provide a detailed analysis of the expected performance, volatility, and potential gains or losses over the next 7 days (weekly) and 30 days (monthly)
        Reply with 3 sections: Current Situation, Potential Scenarios, Overall Rating, Expected Returns
        It would be good to have probability of each sinario.
        Also Rate the stock as 1-10 where 1 is the least and 10 is the highest to buy the stock.
        Please provide the insights in the following format: 
        {{
            "markdown": "your analysis of stock in markdown",
            "Uptrend": probability of upternd,
            "DownTrend": probability of DownTrend,
            "NeutralTrend": probability of Neutral trend,
        }}
        Add the trend Probability in markdown too insted of risk and reward.
        """
        return prompt
    # Risk and Reward Analysis:
    #     - **Weekly Risk**: {weekly_risk * 100:.2f}%
    #     - **Monthly Risk**: {monthly_risk * 100:.2f}%
    #     - **Weekly Reward**: ₹{weekly_reward_amount:.2f}
    #     - **Monthly Reward**: ₹{monthly_reward_amount:.2f}

    def get_insights(self, prompt):
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        return response.text
