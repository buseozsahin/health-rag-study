import csv
import json
import os

os.makedirs("annotations", exist_ok=True)

benchmark_file = open("data/mirage/benchmark.json")
benchmark_data = json.load(benchmark_file)
benchmark_file.close()

medqa_questions = benchmark_data["medqa"]

# add queston_id and chunks
manual_rows = [
  {
    "question_id": "0563",
    "required_fact_1": "DES exposure in utero is causally linked to vaginal clear cell adenocarcinoma",
    "source_chunk_1": "Gynecology_Novak_7087",
    "required_fact_2": "Clear cell adenocarcinoma in DES-exposed women typically presents in the anterior/upper third of the vagina",
    "source_chunk_2": "Gynecology_Novak_7088",
    "requires_multiple_notes": "DES history alone does not distinguish clear cell adenocarcinoma from other DES-related findings (e.g. plain adenosis); the anatomic location of the mass (anterior wall) is what narrows the diagnosis to CCA specifically.",
    "notes": "",
  },

  {
    "question_id": "0501",
    "required_fact_1": "Altered penicillin-binding proteins (PBPs) with low affinity for beta-lactams are the basis of methicillin resistance in staphylococci",
    "source_chunk_1": "Pharmacology_Katzung_4952",
    "required_fact_2": "Isoxazolyl penicillins like dicloxacillin are already designed to resist staphylococcal beta-lactamase, so treatment failure cannot be explained by beta-lactamase production",
    "source_chunk_2": "Pharmacology_Katzung_4964",
    "requires_multiple_notes": "Fact 1 alone identifies PBP alteration as A resistance mechanism, but Fact 2 is needed to rule out the competing distractor (beta-lactamase cleavage, option B) given this patient is already on a beta-lactamase-resistant drug.",
    "notes": "",
  },

  {
    "question_id": "0457",
    "required_fact_1": "The diagnosis of hepatic encephalopathy is clinical, requiring an experienced clinician to recognize and synthesize multiple features, rather than being confirmed by a single test",
    "source_chunk_1": "InternalMed_Harrison_24061",
    "required_fact_2": "Ammonia levels are often elevated in hepatic encephalopathy but correlate poorly with disease severity, so most hepatologists do not rely on ammonia levels to make the diagnosis",
    "source_chunk_2": "InternalMed_Harrison_24056",
    "requires_multiple_notes": "Fact 1 supports the correct answer (diagnosis of exclusion) directly, but Fact 2 is needed to specifically rule out the most tempting distractor (option A, ammonia as the best initial confirmatory test).",
    "notes": "",
  },

  {
    "question_id": "0285",
    "required_fact_1": "Hyperpigmentation without sun exposure is a distinguishing feature of primary adrenal insufficiency, caused by excess ACTH stimulation of melanocytes; secondary adrenal insufficiency instead presents with pale skin",
    "source_chunk_1": "InternalMed_Harrison_27034",
    "required_fact_2": "Primary adrenal insufficiency involves loss of both glucocorticoid and mineralocorticoid secretion, whereas secondary adrenal insufficiency involves glucocorticoid deficiency only",
    "source_chunk_2": "InternalMed_Harrison_27032",
    "requires_multiple_notes": "Fact 1 establishes this is primary (not secondary) adrenal insufficiency via the hyperpigmentation clue; Fact 2 is needed to justify why BOTH hydrocortisone and fludrocortisone are required (option C) rather than glucocorticoid alone.",
    "notes": "",
  },

  {
    "question_id": "1116",
    "required_fact_1": "Fibromyalgia is characterized by widespread muscle pain/tenderness with normal ESR, CK, and muscle biopsy, distinguishing it from inflammatory conditions like polymyalgia rheumatica (which has elevated ESR)",
    "source_chunk_1": "InternalMed_Harrison_31361",
    "required_fact_2": "When fibromyalgia symptoms are dominated by pain and sleep disturbance, a sedating antidepressant such as amitriptyline is preferred because it treats both symptom domains at once; opioids should be avoided",
    "source_chunk_2": "InternalMed_Harrison_26179",
    "requires_multiple_notes": "Fact 1 establishes the diagnosis is fibromyalgia (normal labs rule out inflammatory rheumatologic disease); Fact 2 is needed to justify amitriptyline specifically as the treatment, given this patient's combined pain + sleep disturbance presentation.",
    "notes": "",
  },

  {
    "question_id": "0178",
    "required_fact_1": "In Brown-Sequard syndrome (spinal cord hemisection), pain and thermal sensation loss occurs contralateral to the lesion, while motor paralysis and proprioceptive loss occur ipsilateral to the lesion",
    "source_chunk_1": "Neurology_Adams_1236",
    "required_fact_2": "Spinothalamic tract axons decussate within 1-3 segments rostral to their point of entry, which is the anatomical basis for why pain/temperature loss is specifically contralateral (unlike the corticospinal tract, which is already crossed)",
    "source_chunk_2": "Neurology_Adams_994",
    "requires_multiple_notes": "Fact 1 names the correct clinical pattern (contralateral analgesia), but Fact 2 is needed to understand WHY it's contralateral specifically, which is what distinguishes the correct answer from the trap answer (option C, contralateral corticospinal involvement, which is anatomically backwards).",
    "notes": "",
  },

  {
    "question_id": "1209",
    "required_fact_1": "Presence of affective/mood symptoms predicts better prognosis: schizoaffective disorder's prognosis is better than schizophrenia's but worse than a pure mood disorder's",
    "source_chunk_1": "Psichiatry_DSM-5_568",
    "required_fact_2": "Negative symptoms are the most persistent and predict a WORSE prognosis, not a favorable one, ruling out 'negative symptoms' as the good-prognosis answer",
    "source_chunk_2": "Psichiatry_DSM-5_541",
    "requires_multiple_notes": "yes",
    "notes": "",
  },

  {
    "question_id": "0065",
    "required_fact_1": "Skeletal metastases typically involve the axial skeleton, especially the vertebral column, and appear radiographically as purely lytic, purely blastic, or mixed lesions",
    "source_chunk_1": "Pathology_Robbins_4828",
    "required_fact_2": "Carcinomas frequently metastasize to the vertebral column via the paravertebral venous plexus, a well-documented route explaining why a carcinoma patient's new spinal pain should raise concern for vertebral metastasis rather than being attributed to a mechanical injury",
    "source_chunk_2": "Pathology_Robbins_1165",
    "requires_multiple_notes": "yes",
    "notes": "",
  },

  {
    "question_id": "0447",
    "required_fact_1": "Carotid sinus baroreceptor firing frequency is diminished by a reduction in arterial blood pressure — directly supporting decreased baroreceptor firing in this hypotensive patient",
    "source_chunk_1": "Physiology_Levy_2234",
    "required_fact_2": "Hemorrhage triggers sympathetic vasoconstriction that increases (not decreases) total peripheral/systemic vascular resistance, ruling out option A",
    "source_chunk_2": "Physiology_Levy_3260",
    "requires_multiple_notes": "yes",
    "notes": "",
  },
]

fieldnames = [
    "question_id", "question", "correct_answer",
    "required_fact_1", "source_chunk_1",
    "required_fact_2", "source_chunk_2",
    "requires_multiple_notes", "notes",
]

file = open("annotations/evidence_requirements.csv", "w", newline="")
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

for manual_row in manual_rows:
    qid = manual_row["question_id"]
    entry = medqa_questions[qid]

    full_row = {
        "question_id": qid,
        "question": entry["question"],
        "correct_answer": entry["answer"] + " - " + entry["options"][entry["answer"]],
        "required_fact_1": manual_row["required_fact_1"],
        "source_chunk_1": manual_row["source_chunk_1"],
        "required_fact_2": manual_row["required_fact_2"],
        "source_chunk_2": manual_row["source_chunk_2"],
        "requires_multiple_notes": manual_row["requires_multiple_notes"],
        "notes": manual_row["notes"],
    }
    writer.writerow(full_row)

file.close()
print("Saved", len(manual_rows), "rows to annotations/evidence_requirements.csv")