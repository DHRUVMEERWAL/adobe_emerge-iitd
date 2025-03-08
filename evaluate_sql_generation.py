import json
from difflib import SequenceMatcher

# Load generated SQL results
with open("generated_sql_results.json", "r") as f:
    generated_data = json.load(f)

# Function to calculate similarity
def compute_similarity(expected, generated):
    return SequenceMatcher(None, expected.strip(), generated.strip()).ratio()

# Compute accuracy
total_queries = len(generated_data)
correct_matches = 0
similarities = []

for entry in generated_data:
    expected_sql = entry.get("Query", "").strip()  # Expected SQL
    generated_sql = entry.get("GeneratedQuery", "").strip()  # Model output

    similarity = compute_similarity(expected_sql, generated_sql)
    similarities.append(similarity)

    if similarity > 0.9:  # Consider 90%+ similarity as correct
        correct_matches += 1

accuracy = (correct_matches / total_queries) * 100

# Print results
print(f"Total Queries: {total_queries}")
print(f"Correct Matches (>90% similarity): {correct_matches}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"Average Similarity Score: {sum(similarities) / total_queries:.2f}")
