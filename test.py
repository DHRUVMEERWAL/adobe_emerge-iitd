import json

# Load AI-generated queries
try:
    with open("generated_sql_results.json", "r") as f:
        generated_queries = json.load(f)
except FileNotFoundError:
    print("❌ Error: generated_sql_results.json not found!")
    exit(1)

# Store test results
test_results = []

# Dummy function to check SQL format (doesn't execute)
def validate_sql_syntax(query):
    keywords = ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "JOIN"]
    return any(keyword in query.upper() for keyword in keywords)

# Process each generated query
for i, entry in enumerate(generated_queries, start=1):
    query = entry.get("GeneratedQuery", "")
    if not query:
        entry["ExecutionStatus"] = "Error"
        entry["ErrorMessage"] = "Empty query string"
        test_results.append(entry)
        continue

    print(f"Validating query {i}/{len(generated_queries)}:\n{query}")

    # Validate SQL syntax without running it
    if validate_sql_syntax(query):
        entry["ExecutionStatus"] = "Success"
        entry["Results"] = "Syntax check passed"
    else:
        entry["ExecutionStatus"] = "Error"
        entry["ErrorMessage"] = "Invalid SQL syntax"

    test_results.append(entry)

# Save test results
with open("test_results.json", "w") as f:
    json.dump(test_results, f, indent=4)

print("✅ Local testing complete! Results saved to test_results.json")
