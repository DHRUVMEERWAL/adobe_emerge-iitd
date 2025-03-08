import os
import psycopg2
import groq
import pandas as pd
from flask import Flask, request, jsonify

# Database connection setup
def connect_db():
    return psycopg2.connect(
        dbname="mydb",
        user="user",
        password="password",
        host="my-postgres",  # Use Docker container name
        port="5432"  # Default PostgreSQL port
    )

# Initialize Groq API
groq_api_key = "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"
client = groq.Client(api_key=groq_api_key)

app = Flask(__name__)

# Default route for health check
@app.route('/')
def home():
    return jsonify({"message": "AI-powered SQL Query Generator and Corrector API is running!"})

# Natural Language to SQL Conversion
@app.route('/nl_to_sql', methods=['POST'])
def nl_to_sql():
    user_input = request.json.get("query")
    schema_info = "Table schema: users(id, name, age, email), orders(id, user_id, amount, date)"
    
    prompt = f"Convert the following natural language query into SQL using the given schema:\n\nSchema: {schema_info}\n\nQuery: {user_input}\n\nSQL:"
    response = client.completions.create(
        model="groq-7b",  # Ensure using the correct model from Groq
        prompt=prompt,
        max_tokens=100
    )
    sql_query = response.choices[0].text.strip()
    return jsonify({"sql_query": sql_query})

# SQL Query Error Correction
@app.route('/fix_sql', methods=['POST'])
def fix_sql():
    incorrect_sql = request.json.get("sql")
    
    prompt = f"Fix the following SQL query:\n\n{incorrect_sql}\n\nCorrect SQL:"
    response = client.completions.create(
        model="groq-7b",
        prompt=prompt,
        max_tokens=150
    )
    fixed_sql = response.choices[0].text.strip()
    return jsonify({"corrected_sql": fixed_sql})

# Execute SQL query and return result
@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    sql_query = request.json.get("sql")
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.commit()
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)  # Allow access in Docker
