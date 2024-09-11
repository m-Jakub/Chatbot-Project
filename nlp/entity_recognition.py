import spacy
import json

nlp = spacy.load("en_core_web_sm")

corpus_path = "nlp/filtered_utterances.jsonl"

utterances = []
with open(corpus_path, "r") as f:
    for line in f:
        utterances.append(json.loads(line))

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

results = []
for utterance in utterances:
    text = utterance.get('text', '')
    entities = extract_entities(text)
    results.append({
        "text": text,
        "entities": entities
    })

with open("nlp/annotated_entities.json", "w") as f:
    json.dump(results, f, indent=4)