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
from transformers import T5Tokenizer, T5ForConditionalGeneration


class StockProcessor:
    def __init__(self):
        self.console = Console()
        self.dbType = "sqlite"
        
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')


    def process_stock_code(self, stock_code):
        
        data_access = None
        if(self.dbType  == "MSSQL"):
            data_access = MSSQL.MSSQLDataAccess()
        else:
            data_access = DataAccess.DataAccess()
        
        data_access.connect()
        data_access.create_prompt_table()
        
        dbInsights = data_access.get_Insights_stockcode(datetime.date.today(), stock_code)
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
            self.save_data(stock_code, insights)
            return
        else:
            data = dbInsights.iloc[0]
            self.save_data(stock_code, data['Insights'])
        
    def display_insights(self, insights):
        print(f"Bot: {insights}")

    def save_data(self, stock_code, insights):
        # Create folders if they don't exist
        if not os.path.exists("Data"):
            os.makedirs("Data")
        if not os.path.exists("Markdown"):
            os.makedirs("Markdown")
        # Convert insights to JSON
        insights_json = json.dumps(insights)

        # Save data in JSON format
        with open(f"Data/{stock_code}.json", "w") as json_file:
            json.dump(insights_json, json_file)

        # Create a Markdown file
        markdown_text = f"# Stock Analysis for {stock_code}\n\n"
        
        insights = json.loads(insights_json.strip())
        if isinstance(insights, str):
            insights = json.loads(insights)
        
        markdown_text += insights["markdown"]
        self.console.print(Markdown(markdown_text))
            
        with open(f"Markdown/{stock_code}.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_text)
    
    def load_data(self):
        
        data_access = None
        if(self.dbType  == "MSSQL"):
            data_access = MSSQL.MSSQLDataAccess()
        else:
            data_access = DataAccess.DataAccess()
        
        
        data_access.connect()
        df = data_access.get_all_Insights()
        data_access.close_connection()
        return df
    def get_stock_data(self,stock_code):
        
        data_access = None
        if(self.dbType  == "MSSQL"):
            data_access = MSSQL.MSSQLDataAccess()
        else:
            data_access = DataAccess.DataAccess()
        
        
        data_access.connect()
        df_stock_data_df, prompt_log_df = data_access.get_records_by_stock_code(stock_code)
        # Iterate Prompt log and Add New column Summery
        prompt_log_df['Summary'] = prompt_log_df['Markdown'].apply(self.summarize_text)

        data_access.close_connection()
        return df_stock_data_df, prompt_log_df 
        data_access.close_connection()
        return df_stock_data_df, prompt_log_df 
    
    def summarize_text(self, text):
        # Encode the text
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)

        # Generate the summary
        outputs = self.model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)

        # Decode the summary
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return summary
    