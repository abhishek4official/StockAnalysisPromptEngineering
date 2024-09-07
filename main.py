import datetime
import json
import markdown
import DataAccess
import LLM
import StockAnalysis
import os
from rich.console import Console
from rich.markdown import Markdown
import MSSQL
from StockProcess import StockProcessor

def process_stock_code(stock_code):
    dbType = "MSSQL"
    if(dbType == "sqlite"):
        data_access = MSSQL.MSSQLDataAccess()
    else:
        data_access = DataAccess.DataAccess()
    
    data_access.connect()
    data_access.create_prompt_table()
    
    dbInsights=data_access.get_Insights_stockcode(datetime.date.today(), stock_code)
    data_access.close_connection()
    if len(dbInsights) <= 0:
        llm = LLM.LLM(api_key_path='apiKey.key')
        # Remove .NS any you can pass any yahoo finance compatible symbol
        stock_analysis = StockAnalysis.StockAnalysis(symbol=f"{stock_code}.NS")
        stock_analysis.download_data()
        stock_analysis.calculate_indicators()
        stock_analysis.calculate_risk_reward()
        results = stock_analysis.get_results()
        #stock_analysis.get_ARIMA_AND_GARCH_Forcast()

        prompt = llm.generate_prompt(stock_analysis)
        insights = llm.get_insights(prompt)
        
        data_access.connect()
        data_access.insert_prompt_data(stock_code, prompt, insights, datetime.date.today())
        data_access.close_connection()
        save_data(stock_code, insights)
        return
    else:
        data = dbInsights.iloc[0]
        save_data(stock_code, data['Insights'])
    

# def display_insights(insights):
#     print(f"Bot: {insights}")

# def save_data(stock_code, insights):
#     # Create folders if they don't exist
#     if not os.path.exists("Data"):
#         os.makedirs("Data")
#     if not os.path.exists("Markdown"):
#         os.makedirs("Markdown")
#     # Convert insights to JSON
#     insights_json = json.dumps(insights)

#     # Save data in JSON format
#     with open(f"Data/{stock_code}.json", "w") as json_file:
#         json.dump(insights_json, json_file)

#     # Create a Markdown file
#     markdown_text = f"# Stock Analysis for {stock_code}\n\n"
    
#     insights = json.loads(insights_json.strip())
#     if isinstance(insights, str):
#         insights = json.loads(insights)
    
#     markdown_text += insights["markdown"]
#     console = Console()
#     console.print(Markdown(markdown_text))
         

#     with open(f"Markdown/{stock_code}.md", "w", encoding="utf-8") as md_file:
#         md_file.write(markdown_text)

if __name__ == "__main__":
    stock_code=''
    while stock_code != 'exit' or stock_code != 'e':
        stock_code = input("Enter the stock code: ")  # Ask for stock code from user
        stock_code = stock_code.upper()
        
        sp=StockProcessor()
        print("Waiting...")
        sp.process_stock_code(stock_code)
        print("______________________________________________________________")
    