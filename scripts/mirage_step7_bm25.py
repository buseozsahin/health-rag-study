import csv
import json
import os
from rank_bm25 import BM25Okapi

os.makedirs("results", exist_ok=True)

file = open("data/mirage/benchmark.json")
data = json.load(file)
file.close()
medqa_questions = data["medqa"]

question_ids = ["0563", "0501", "0457", "0285", "1116", "0178", "1209", "0065", "0447"]

all_chunks = []
file = open("data/processed/mirage_step5_candidate_pools.jsonl")
for line in file:
    chunk = json.loads(line)
    all_chunks.append(chunk)
file.close()

fieldnames = ["question_id", "rank", "chunk_id", "BM25_score", "chunk_text"]

output_file = open("results/bm25_results.csv", "w", newline="")
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

for question_id in question_ids:
    pool = []
    for chunk in all_chunks:
        if chunk["question_id"] == question_id:
            pool.append(chunk)

    tokenized_pool = []
    for chunk in pool:
        tokens = chunk["chunk_text"].lower().split()
        tokenized_pool.append(tokens)

    bm25 = BM25Okapi(tokenized_pool)

    question_text = medqa_questions[question_id]["question"]
    query_tokens = question_text.lower().split()

    scores = bm25.get_scores(query_tokens)

    scored_pool = []
    for i in range(len(pool)):
        scored_pool.append((scores[i], pool[i]))

    scored_pool.sort(key=lambda x: x[0], reverse=True)

    top5 = scored_pool[:5]

    print("Question", question_id, "- top 5 BM25 chunks:")
    rank = 1
    for score, chunk in top5:
        print(" ", rank, "-", chunk["chunk_id"], "- score:", round(score, 3))
        writer.writerow({
            "question_id": question_id,
            "rank": rank,
            "chunk_id": chunk["chunk_id"],
            "BM25_score": score,
            "chunk_text": chunk["chunk_text"],
        })
        rank += 1
    print("")

output_file.close()
print("Saved")