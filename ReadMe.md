# POC for Using Prompt Engineering to analyse Stock 
This project is a Python-based stock analysis tool that leverages the Google Gemini API to analyze stock symbols using prompt engineering. It processes stock data, calculates technical indicators, and generates insights using a language model.

## Features

- Download stock data using yfinance for Indian NSE stocks.
- Calculate various technical indicators such as SMA, Bollinger Bands, ATR, OBV, ROC, RSI, MACD, EMA, and ADX.
- Assess weekly and monthly risk and reward based on stock returns.
- Generate insights using the LLM (Language Model) library.
- Save the results in both JSON and Markdown formats.
- Data is saved in SQLLite DB too.

## Requirements

- Python 3.x
- Required Python libraries:
    - `json`
    - `markdown`
    - `LLM` (custom library)
    - `StockAnalysis` (custom library)

## Installation

1. Clone the repository:
        ```sh
        git clone https://github.com/abhishek4official/StockUsingPromptEngineering.git
        cd stock-analysis-tool
        ```

2. Install the required libraries:
        ```sh
        pip install -r requirements.txt
        ```

3. Add a file named `apiKey.key` and save your Gemini API key.

## Usage

1. Run the `main.py` script:
        ```sh
        python main.py
        ```

2. Enter the stock code when prompted.

3. The results will be saved in JSON and Markdown formats with the stock symbol as the filename. The JSON file will be saved in the `Data` folder, and the Markdown file will be saved in the `Markdown` folder.

`Note:` The code is specific for the Indian NSE stock exchange but if you want to configure it you just need to remove '.NS' is main.py
```sh
    # Remove .NS any you can pass any yahoo finance compatible symbol
    stock_analysis = StockAnalysis.StockAnalysis(symbol=f"{stock_code}.NS")
```

## Example

After running the script, you will find two files in the project directory:

- `Data/{stock_code}.json`: Contains the insights in JSON format.
- `Markdown/{stock_code}.md`: Contains the insights in Markdown format.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please contact [Abhishek Kumar](mailto:abhishek4official@gmail.com).
