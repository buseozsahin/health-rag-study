import csv
import json
import os
import torch
from transformers import AutoTokenizer, AutoModel

os.makedirs("results", exist_ok=True)

query_tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Query-Encoder")
query_model = AutoModel.from_pretrained("ncbi/MedCPT-Query-Encoder")
query_model.eval()

article_tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Article-Encoder")
article_model = AutoModel.from_pretrained("ncbi/MedCPT-Article-Encoder")
article_model.eval()

benchmark_file = open("data/mirage/benchmark.json")
benchmark_data = json.load(benchmark_file)
benchmark_file.close()
medqa_questions = benchmark_data["medqa"]

question_ids = ["0563", "0501", "0457", "0285", "1116", "0178", "1209", "0065", "0447"]

all_chunks = []
file = open("data/processed/mirage_step5_candidate_pools.jsonl")
for line in file:
    chunk = json.loads(line)
    all_chunks.append(chunk)
file.close()

fieldnames = ["question_id", "rank", "chunk_id", "MedCPT_score", "chunk_text"]

output_file = open("results/medcpt_results.csv", "w", newline="")
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

for question_id in question_ids:

    pool = []
    for chunk in all_chunks:
        if chunk["question_id"] == question_id:
            pool.append(chunk)

    question_text = medqa_questions[question_id]["question"]
    with torch.no_grad():
        query_encoded = query_tokenizer(
            [question_text],
            truncation=True,
            padding=True,
            return_tensors="pt",
            max_length=64,
        )
        query_embed = query_model(**query_encoded).last_hidden_state[:, 0, :]

    article_pairs = []
    for chunk in pool:
        article_pairs.append([chunk["source_title"], chunk["chunk_text"]])

    with torch.no_grad():
        article_encoded = article_tokenizer(
            article_pairs,
            truncation=True,
            padding=True,
            return_tensors="pt",
            max_length=512,
        )
        article_embeds = article_model(**article_encoded).last_hidden_state[:, 0, :]

    scores = torch.matmul(query_embed, article_embeds.T).squeeze(0)
    scores_list = scores.tolist()

    scored_pool = []
    for i in range(len(pool)):
        scored_pool.append((scores_list[i], pool[i]))

    scored_pool.sort(key=lambda x: x[0], reverse=True)

    top5 = scored_pool[:5]

    print("Question", question_id, "- top 5 MedCPT chunks:")
    rank = 1
    for score, chunk in top5:
        print(" ", rank, "-", chunk["chunk_id"], "- score:", round(score, 3))
        writer.writerow({
            "question_id": question_id,
            "rank": rank,
            "chunk_id": chunk["chunk_id"],
            "MedCPT_score": score,
            "chunk_text": chunk["chunk_text"],
        })
        rank += 1
    print("")

output_file.close()
print("Saved top-5 MedCPT results to results/medcpt_results.csv")