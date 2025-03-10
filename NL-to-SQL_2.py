import json
import re
import groq

# Initialize Groq API
groq_api_key = "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"
client = groq.Groq(api_key=groq_api_key)

# Function to extract schema from SQL file
def extract_schema_from_sql(sql_file):
    with open(sql_file, "r") as f:
        schema_sql = f.read()
    
    tables = re.findall(r'CREATE TABLE (\w+) \((.*?)\);', schema_sql, re.DOTALL)
    database_schema = {}
    for table_name, columns in tables:
        column_list = [col.split()[0] for col in columns.strip().split("\n") if col]
        database_schema[table_name] = column_list
    
    return database_schema

# Function to generate SQL using Groq API
def generate_sql(natural_language_query, schema):
    schema_str = "\n".join([f"- {table}({', '.join(columns)})" for table, columns in schema.items()])
    
    prompt = f"""You are a SQL generator. Convert the following natural language query into a valid SQL statement, strictly following the provided database schema. Do NOT add any explanation, only output SQL.

Schema:
{schema_str}

Query: {natural_language_query}

SQL:"""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "system", "content": "You are a helpful SQL generator."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    return response.choices[0].message.content.strip()

# Load training data
with open("train_generate_task.json", "r") as f:
    nl_to_sql_data = json.load(f)

# Extract schema from the SQL file
database_schema = extract_schema_from_sql("hackathon_database_iitd.sql")

# Process all queries in the dataset
for i, entry in enumerate(nl_to_sql_data, start=1):
    print(f"Processing NL-to-SQL query {i}/{len(nl_to_sql_data)}...")
    entry["GeneratedQuery"] = generate_sql(entry["NL"], database_schema)
    print(f"Completed {i}/{len(nl_to_sql_data)}")

# Save results to JSON
with open("generated_sql_results_2.json", "w") as f:
    json.dump(nl_to_sql_data, f, indent=4)

print("SQL generation complete! Results saved.")
