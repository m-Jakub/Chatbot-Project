import json

utterances = []
corpus_path = "cleaned_reddit_corpus/utterances.jsonl"

with open(corpus_path, "r") as f:
    for line in f:
        utterances.append(json.loads(line))

# Remove entries where 'text' is empty
filtered_utterances = [utterance for utterance in utterances if utterance.get('text', '').strip()]

filtered_corpus_path = "nlp/filtered_utterances.jsonl"
with open(filtered_corpus_path, "w") as f:
    for utterance in filtered_utterances:
        f.write(json.dumps(utterance) + "\n")