from flask import Flask, request, jsonify
from flasgger import Swagger
from StockProcess import StockProcessor

app = Flask(__name__)
swagger = Swagger(app)
stock_processor = StockProcessor()

@app.route('/process_stock_code', methods=['POST'])
def process_stock_code():
    """
    Process a stock code
    ---
    parameters:
      - name: stock_code
        in: body
        type: string
        required: true
        description: The stock code to process
        schema:
          type: object
          required:
            - stock_code
          properties:
            stock_code:
              type: string
              example: AAPL
    responses:
      200:
        description: Stock code processed successfully
      400:
        description: stock_code is required
      500:
        description: Internal server error
    """
    data = request.get_json()
    stock_code = data.get('stock_code')
    if not stock_code:
        return jsonify({'error': 'stock_code is required'}), 400
    
    try:
        stock_processor.process_stock_code(stock_code)
        return jsonify({'message': 'Stock code processed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_data', methods=['GET'])
def load_data():
    """
    Load data
    ---
    responses:
      200:
        description: Data loaded successfully
      500:
        description: Internal server error
    """
    try:
        df = stock_processor.load_data()
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)