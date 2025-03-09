# SQL Generation and Correction with Groq API

This project leverages the Groq API to transform natural language queries into SQL statements and to correct erroneous SQL queries. It utilizes the `groq` Python library to interface with Groq's large language models.

## Features

- **Natural Language to SQL Conversion:** Converts user-friendly language into SQL queries.
- **SQL Query Correction:** Identifies and corrects errors in SQL statements.

## Prerequisites

- **Python 3.8+**: Ensure you have Python installed. You can download it from the [official website](https://www.python.org/downloads/).
- **Groq API Key**: Obtain a free API key by creating an account on the [Groq Console](https://console.groq.com/).

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/dhruvmeerwal/adobe_emerge-iitd
   cd sql-groq-api
   ```

2. **Install Dependencies:**

   It's recommended to use a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

   Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the project root directory and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. **Prepare Training Data:**

   - Place your natural language to SQL training data in `train_generate_task.json`.
   - Place your SQL correction training data in `train_query_correction_task.json`.

2. **Run the Training Script:**

   ```bash
   python train_model.py
   ```

   This script will process the training data, generate SQL queries, correct SQL queries, and save the results to `generated_sql_results.json` and `corrected_sql_results.json`.

3. **Evaluate the Model:**

   Use the provided evaluation scripts to assess the model's performance:

   ```bash
   python evaluate_sql_generation.py
   python evaluate_sql_correction.py
   ```

   These scripts will output metrics such as accuracy and average similarity scores.

## Project Structure

- `train_model.py`: Main script for training and generating/correcting SQL queries.
- `evaluate_sql_generation.py`: Evaluates the performance of SQL generation.
- `evaluate_sql_correction.py`: Evaluates the performance of SQL correction.
- `train_generate_task.json`: Training data for natural language to SQL conversion.
- `train_query_correction_task.json`: Training data for SQL correction.
- `generated_sql_results.json`: Output file containing generated SQL queries.
- `corrected_sql_results.json`: Output file containing corrected SQL queries.
- `requirements.txt`: List of Python dependencies.
- `.env`: File to store environment variables like the Groq API key.

## Notes

- Ensure that your training data is in the correct JSON format as expected by the scripts.
- The Groq API key should be kept confidential. Avoid sharing it publicly.

## References

- [Groq API Cookbook](https://github.com/groq/groq-api-cookbook)
- [Groq Python Library](https://github.com/groq/groq-python)
- [Groq Console Examples](https://console.groq.com/docs/examples)

For further assistance, refer to the [Groq API Documentation](https://console.groq.com/docs) or join the [Groq Developer Community on Discord](https://discord.gg/groq).

