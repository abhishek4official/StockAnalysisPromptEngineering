import json
import markdown
import LLM
import StockAnalysis

def process_stock_code(stock_code):
    llm = LLM.LLM(api_key_path='apiKey.key')

    stock_analysis = StockAnalysis.StockAnalysis(symbol=f"{stock_code}.NS")
    stock_analysis.download_data()
    stock_analysis.calculate_indicators()
    stock_analysis.calculate_risk_reward()
    results = stock_analysis.get_results()

    prompt = llm.generate_prompt(stock_analysis)
    insights = llm.get_insights(prompt)

    #display_insights(insights)
    save_data(stock_code, insights)

def display_insights(insights):
    print(f"Bot: {insights}")

def save_data(stock_code, insights):
    # Convert insights to JSON
    insights_json = json.dumps(insights)

    # Save data in JSON format
    with open(f"{stock_code}.json", "w") as json_file:
        json.dump(insights_json, json_file)

    # Create a Markdown file
    markdown_text = f"# Stock Analysis for {stock_code}\n\n"
    
    insights = json.loads(insights_json.strip())
    if isinstance(insights, str):
        insights = json.loads(insights)
    
    markdown_text += insights["markdown"]
         

    with open(f"{stock_code}.md", "w", encoding="utf-8") as md_file:
        md_file.write(markdown_text)

if __name__ == "__main__":
    stock_code = input("Enter the stock code: ")  # Ask for stock code from user
    
    process_stock_code(stock_code)