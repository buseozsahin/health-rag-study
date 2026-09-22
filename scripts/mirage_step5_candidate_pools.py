import json
from datasets import load_dataset

texbook_chunks = load_dataset("MedRAG/textbooks")["train"]

chunks_title = {}
for chunk in texbook_chunks:
  title = chunk["title"]
  if title not in chunks_title:
    chunks_title[title] = []
  chunks_title[title].append(chunk)

# first filter just getting the relavant part of the data
question_to_books = {
    "0563": ["Gynecology_Novak"],
    "0501": ["Pathology_Robbins", "Pharmacology_Katzung"],
    "0457": ["InternalMed_Harrison"],
    "0285": ["InternalMed_Harrison"],
    "1116": ["InternalMed_Harrison"],
    "0178": ["Neurology_Adams"],
    "1209": ["Psichiatry_DSM-5"],
    "0065": ["Pathology_Robbins"],
    "0447": ["Physiology_Levy"],
}

# second filter just looking for specific keywords
question_keywords = {
    "0563": ["diethylstilbestrol", "clear cell adenocarcinoma"],
    "0501": ["methicillin", "penicillin-binding protein", "beta-lactam"],
    "0457": ["hepatic encephalopathy"],
    "0285": ["adrenal insufficiency", "addisonian crisis"],
    "1116": ["fibromyalgia", "amitriptyline"],
    "0178": ["Brown-Sequard", "hemicord", "spinothalamic"],
    "1209": ["brief psychotic", "schizophreniform", "prognosis"],
    "0065": ["metastasis", "osteolytic", "vertebral"],
    "0447": ["baroreceptor", "hemorrhagic shock", "hypovolemic"],
}

file = open("data/processed/mirage_step5_candidate_pools.jsonl", "w")

for question_id, book_titles in question_to_books.items():
  matching_chunks = []
  for title in book_titles:
    matching_chunks.extend(chunks_title.get(title, []))

  keywords = question_keywords[question_id]
  narrowed_chunks = []
  for chunk in matching_chunks:
    text_lower = chunk["content"].lower()
    if any(keyword.lower() in text_lower for keyword in keywords):
      narrowed_chunks.append(chunk)
      
  print(question_id, " - BOOK TITLE: ", book_titles, " --> ", "MATCHING CHUNKS: ", len(matching_chunks), " - NARROWED CHUNKS: ", len(narrowed_chunks))

  for chunk in narrowed_chunks:
    record = {
      "question_id": question_id,
      "chunk_id": chunk["id"],
      "source_title": chunk["title"],
      "chunk_text": chunk["content"],
    }
    file.write(json.dumps(record) + "\n")

file.close()
print("Saved")