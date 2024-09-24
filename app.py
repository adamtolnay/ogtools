from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection configuration
db_config = {
    'user': 'root',        # Replace with your MySQL username
    'password': 'Halloween123!', # Replace with your MySQL password
    'host': '127.0.0.1',
    'database': 'ogtools',
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
        return {'columns': column_names, 'rows': data}
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {'columns': [], 'rows': []}
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

if __name__ == '__main__':
    app.run(debug=True)
