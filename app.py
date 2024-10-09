from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import mysql.connector
from predict import make_prediction
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

# Database connection configuration
db_config = {
    'user': os.getenv('DB_USER'),       
    'password': os.getenv('DB_PASSWORD'), 
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'raise_on_warnings': True
}

def fetch_data_from_table(table_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        # Fetch column names
        column_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        combined_data = [column_names] + list(data)
        return combined_data
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/get-data', methods=['GET'])
def get_data():
    data = fetch_data_from_table('data')
    metadata = fetch_data_from_table('metadata')
    return jsonify({'data': data, 'metadata': metadata})

@app.route('/process-columns', methods=['POST'])
def process_columns():
    data = request.json  # Retrieve JSON data from the request
    rowX = data.get('rowX')
    colY = data.get('colY')
    
    r2_score = make_prediction(rowX, colY)
    
    # Return the R² score
    return jsonify({'status': 'success', 'r2': r2_score})

@app.route('/get-code', methods=['GET'])
def get_code():
    return send_file('predict.py', mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
