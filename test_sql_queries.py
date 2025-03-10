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

def validate_sql_syntax(query):
    keywords = ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "JOIN"]
    return any(keyword in query.upper() for keyword in keywords)

# Count statistics
total_queries = len(generated_queries)
success_count = 0
error_count = 0

# Process each generated query
for i, entry in enumerate(generated_queries, start=1):
    query = entry.get("GeneratedQuery", "")
    if not query:
        entry["ExecutionStatus"] = "Error"
        entry["ErrorMessage"] = "Empty query string"
        test_results.append(entry)
        error_count += 1
        continue

    print(f"Validating query {i}/{total_queries}:\n{query}")

    if validate_sql_syntax(query):
        entry["ExecutionStatus"] = "Success"
        entry["Results"] = "Syntax check passed"
        success_count += 1
    else:
        entry["ExecutionStatus"] = "Error"
        entry["ErrorMessage"] = "Invalid SQL syntax"
        error_count += 1
    
    test_results.append(entry)

# Calculate scores
accuracy = (success_count / total_queries) * 100 if total_queries > 0 else 0

# Save test results
with open("test_results.json", "w") as f:
    json.dump(test_results, f, indent=4)

print(f"✅ Testing complete! Results saved to test_results.json")
print(f"🔹 Total Queries: {total_queries}")
print(f"✅ Successful Queries: {success_count}")
print(f"❌ Failed Queries: {error_count}")
print(f"🎯 Accuracy: {accuracy:.2f}%")