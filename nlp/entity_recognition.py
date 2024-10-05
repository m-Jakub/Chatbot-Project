import spacy
import json
import os

processed_file = "nlp/annotated_entities_final_batch.json"
nlp = spacy.load("en_core_web_sm")

def load_processed_entities():
    if os.path.exists(processed_file):
        with open(processed_file, "r") as f:
            print ("Loading entities from file")
            return json.load(f)
    else:
        print ("Processed file not found")
        return []

def extract_entities(text):
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    
# Load preprocessed data instead of reprocessing every time
annotated_entities = load_processed_entities()

if not annotated_entities:

    corpus_path = "nlp/filtered_utterences.jsonl"

    utterances = []
    with open(corpus_path, "r") as f:
        for line in f:
            utterances.append(json.loads(line))

    batch_size = 10000
    batch_results = []  

    for i, utterance in enumerate(utterances):
        text = utterance.get('text', '')
        entities = extract_entities(text)
        batch_results.append({
            'text': text,
            'entities': entities
        })

        if i > 0 and i % 1000 == 0:
            print(f"Processed {i} documents")
        
        # Save the results to a file every batch_size iterations
        if i > 0 and i % batch_size == 0:
            with open(f"nlp/annotated_entities_batch_{i // batch_size}.json", "w") as f:
                json.dump(batch_results, f, indent=4)
            batch_results = []

    # Save any remaining documents
    if batch_results:
        with open(f"nlp/annotated_entities_final_batch.json", "w") as f:
            json.dump(batch_results, f, indent=4)

    print("Entities extracted and saved to nlp/annotated_entities.json")

else:
    print("Entities loaded from file")