import json
from datasets import load_dataset

file = open("data/mirage/benchmark.json")
mirage = json.load(file)

print(list(mirage.keys()))

# Manual inspection check
medqa = mirage["medqa"]
print(len(medqa), "questions in medqa")

first_five_id = list(medqa.keys()) [:5]

for question_id in first_five_id:
  entry = medqa[question_id]

  print("id", question_id)
  print("question: ", entry["question"])
  print("options: ", entry["options"])
  print("answer: ", entry["answer"])

  assert len(entry["options"]) == 4, f"Question {question_id} does not have 4 options"
  assert entry["answer"] in entry["options"], "This answer key is not valid"

print("benchmark.json is correct")

# Manual corpus check
textbook_chunks = load_dataset("MedRAG/textbooks")["train"]

for i in range(5):
  chunk = textbook_chunks[i]
  print(f"-- {i} --")
  print(chunk)