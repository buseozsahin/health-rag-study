import json
import random

file = open("data/mirage/benchmark.json")
mirage = json.load(file)
medqa = mirage["medqa"]

random.seed(42)

questions_ids = list(medqa.keys())
sample_questions = random.sample(questions_ids, 20)

for question_id in sample_questions:
  question_data = medqa[question_id]
  
  print("***")
  print("ID: ", question_id)
  print("Question: ", question_data["question"])
  print("Options: ", question_data["options"])
  print("Answer: ", question_data["answer"])
