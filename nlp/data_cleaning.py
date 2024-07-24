import os
import re
from convokit import Corpus
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = text.lower() 
    return text

def preprocess_text(text):
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

script_dir = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(script_dir, 'reddit-corpus-small')
if os.path.exists(corpus_path):
    corpus = Corpus(filename=corpus_path)
    for utterance in corpus.iter_utterances():
        clean_utterance = clean_text(utterance.text)
        preprocessed_utterance = preprocess_text(clean_utterance)
        utterance.text = preprocessed_utterance
    corpus.dump(name='cleaned_reddit_corpus', base_path='./')
else:
    print(f"File not found: {corpus_path}")