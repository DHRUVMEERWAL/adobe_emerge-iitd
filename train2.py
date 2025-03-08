import pandas as pd
import groq
import json

# Initialize Groq API
groq_api_key = "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"
client = groq.Groq(api_key=groq_api_key)

# Load training data
with open("train_generate_task.json", "r") as f:
    nl_to_sql_data = json.load(f)

with open("train_query_correction_task.json", "r") as f:
    sql_correction_data = json.load(f)

# Function to generate SQL using Groq API
def generate_sql(natural_language_query):
    prompt = f"""You are a SQL generator. Convert the following natural language query into a valid SQL statement, strictly following the schema provided. Do NOT add any explanation, only output SQL.

Schema: 
- users(id, name, age, email)
- orders(id, user_id, amount, date)
- products(id, name, price, stock)

Query: {natural_language_query}

SQL:"""
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "system", "content": "You are a helpful SQL generator."},
                  {"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Function to correct SQL using Groq API
def correct_sql(incorrect_query):
    prompt = f"""You are an expert SQL error corrector. Fix the following incorrect SQL query based on the given schema. Return ONLY the corrected SQL query, no explanations.

Schema: 
- users(id, name, age, email)
- orders(id, user_id, amount, date)
- products(id, name, price, stock)

Incorrect SQL:
{incorrect_query}

Correct SQL:"""
    response = client.chat.completions.create(
        model="distil-whisper-large-v3-en",
        messages=[{"role": "system", "content": "You are a helpful SQL error corrector."},
                  {"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# Process all queries in the dataset
for i, entry in enumerate(nl_to_sql_data, start=1):
    print(f"Processing NL-to-SQL query {i}/{len(nl_to_sql_data)}...")
    entry["GeneratedQuery"] = generate_sql(entry["NL"]) 
    print(f"Completed {i}/{len(nl_to_sql_data)}")

for i, entry in enumerate(sql_correction_data, start=1):
    print(f"Processing SQL Correction {i}/{len(sql_correction_data)}...")
    entry["CorrectedQuery"] = correct_sql(entry["IncorrectQuery"]) 
    print(f"Completed {i}/{len(sql_correction_data)}")

# Save results to JSON
with open("generated_sql_results.json", "w") as f:
    json.dump(nl_to_sql_data, f, indent=4)

with open("corrected_sql_results.json", "w") as f:
    json.dump(sql_correction_data, f, indent=4)

print("SQL generation and correction complete! Results saved.")
