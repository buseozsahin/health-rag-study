import csv

question_ids = ["0563", "0501", "0457", "0285", "1116", "0178", "1209", "0065", "0447"]

evidence_by_question = {}
file = open("annotations/evidence_requirements.csv")
reader = csv.DictReader(file)
for row in reader:
    evidence_by_question[row["question_id"]] = row
file.close()

bm25_rows = []
file = open("results/bm25_results.csv")
reader = csv.DictReader(file)
for row in reader:
    bm25_rows.append(row)
file.close()

medcpt_rows = []
file = open("results/medcpt_results.csv")
reader = csv.DictReader(file)
for row in reader:
    medcpt_rows.append(row)
file.close()

fieldnames = [
    "question_id", "retriever", "rank", "chunk_id", "score",
    "matches_required_evidence",
    "chunk_text",
    "required_fact_1", "source_chunk_1",
    "required_fact_2", "source_chunk_2",
    "label", "justification",
]

output_file = open("results/step9_review.csv", "w", newline="")
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

for question_id in question_ids:
    evidence = evidence_by_question[question_id]

    for row in bm25_rows:
        if row["question_id"] == question_id:

            match = ""
            if row["chunk_id"] == evidence["source_chunk_1"]:
                match = "fact_1"
            if row["chunk_id"] == evidence["source_chunk_2"]:
                match = "fact_2"

            writer.writerow({
                "question_id": question_id,
                "retriever": "BM25",
                "rank": row["rank"],
                "chunk_id": row["chunk_id"],
                "score": row["BM25_score"],
                "matches_required_evidence": match,
                "chunk_text": row["chunk_text"],
                "required_fact_1": evidence["required_fact_1"],
                "source_chunk_1": evidence["source_chunk_1"],
                "required_fact_2": evidence["required_fact_2"],
                "source_chunk_2": evidence["source_chunk_2"],
                "label": "",
                "justification": "",
            })

    for row in medcpt_rows:
        if row["question_id"] == question_id:

            match = ""
            if row["chunk_id"] == evidence["source_chunk_1"]:
                match = "fact_1"
            if row["chunk_id"] == evidence["source_chunk_2"]:
                match = "fact_2"

            writer.writerow({
                "question_id": question_id,
                "retriever": "MedCPT",
                "rank": row["rank"],
                "chunk_id": row["chunk_id"],
                "score": row["MedCPT_score"],
                "matches_required_evidence": match,
                "chunk_text": row["chunk_text"],
                "required_fact_1": evidence["required_fact_1"],
                "source_chunk_1": evidence["source_chunk_1"],
                "required_fact_2": evidence["required_fact_2"],
                "source_chunk_2": evidence["source_chunk_2"],
                "label": "",
                "justification": "",
            })

output_file.close()
print("Saved combined review spreadsheet to results/step9_review.csv")