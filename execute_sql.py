import json
import psycopg2

# Connecting  to PostgreSQL running in Docker
conn = psycopg2.connect(
    dbname="mydb",
    user="user",
    password="password",
    host="my-postgres",  # Use Docker container name
    port="5321"  # Custom PostgreSQL port - Default 5432 if available
)
cursor = conn.cursor()

# Load AI-generated queries
with open("generated_sql_results.json", "r") as f:
    generated_queries = json.load(f)

# Execute Queries in PostgreSQL
for i, entry in enumerate(generated_queries, start=1):
    query = entry["GeneratedQuery"]
    print(f"Executing query {i}/{len(generated_queries)}:\n{query}")
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Fetch query results
        entry["ExecutionStatus"] = "Success"
        entry["Results"] = results
    except Exception as e:
        entry["ExecutionStatus"] = "Error"
        entry["ErrorMessage"] = str(e)
        conn.rollback()  # Rollback in case of error

# Save updated results
with open("executed_sql_results.json", "w") as f:
    json.dump(generated_queries, f, indent=4)

# Close the connection
cursor.close()
conn.close()

print("Executed all queries and saved results to executed_sql_results.json")
