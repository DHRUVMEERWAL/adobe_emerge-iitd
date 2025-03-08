import json

# Load the trained model results
with open("corrected_sql_results.json", "r") as f:
    corrected_sql_data = json.load(f)

# Function to test SQL correction
def test_sql_correction(incorrect_sql):
    for entry in corrected_sql_data:
        if entry["IncorrectQuery"] == incorrect_sql:
            return entry["CorrectedQuery"]
    return "Query not found in trained model."

# Example test cases
test_queries = [
    "SELECT SUM(preferences_total_orders) FROM customerinfo WHERE person_income > 50000 AND person_occupation = sales;",
    "SELECT * FROM customerinfo JOIN wishlist ON customerinfo.person_customer_id = wishlist.priority_level",
    "SELECT campaign_id FROM campaigns WHERE campaign_status = 1"
]

# Run tests
for query in test_queries:
    corrected_query = test_sql_correction(query)
    print(f"\nIncorrect Query:\n{query}\nCorrected Query:\n{corrected_query}")
