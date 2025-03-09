import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset

# Load training data
with open("train_generate_task.json", "r") as f:
    nl_to_sql_data = json.load(f)

# Prepare data for training
def preprocess_data(data):
    inputs = []
    outputs = []
    for entry in data:
        inputs.append(entry["NL"])  # Natural Language query
        outputs.append(entry["Query"])  # Expected SQL query
    return Dataset.from_dict({"input": inputs, "output": outputs})

# Convert dataset to Hugging Face format
dataset = preprocess_data(nl_to_sql_data)

# Load model and tokenizer
MODEL_NAME = "mistralai/Mistral-7B-Instruct"  # Use Llama-2-7B or other models if preferred
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def tokenize_function(examples):
    model_inputs = tokenizer(examples["input"], padding="max_length", truncation=True, max_length=512)
    labels = tokenizer(examples["output"], padding="max_length", truncation=True, max_length=512)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(tokenize_function, batched=True)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./sql_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train the model
trainer.train()

# Save the trained model
model.save_pretrained("./fine_tuned_sql_model")
tokenizer.save_pretrained("./fine_tuned_sql_model")

print("Training complete! Model saved.")
