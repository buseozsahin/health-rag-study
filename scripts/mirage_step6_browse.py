import json

# enter the question id manually
question_id = "0447"
search_term = "firing"


search_term = search_term.lower()

all_chunks = []
file = open("data/processed/mirage_step5_candidate_pools.jsonl")
for line in file:
  chunk = json.loads(line)
  all_chunks.append(chunk)
file.close()

pool = []
for chunk in all_chunks:
  if chunk["question_id"] == question_id:
    pool.append(chunk)

print("Question: ", question_id, ": ", len(pool), "chunk")
print("****")

for chunk in pool:
  text = chunk["chunk_text"]
  text_lower = text.lower()

  if search_term not in text_lower:
    continue
  
  print("CHUNK: ", chunk["chunk_id"])
  print(text, "\n")