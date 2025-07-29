import argparse
import pandas as pd
from langdetect import detect
from textblob import TextBlob
import spacy
from tqdm import tqdm

#topic modelling
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# prepreocessing text
import nltk
from nltk.stem import WordNetLemmatizer
import re

nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()


def download_nltk_resource(resource_name):
    """
    Download an NLTK resource if it isn't already available.
    """
    from nltk.data import find
    try:
        find(f'corpora/{resource_name}')
    except LookupError:
        print(f"Downloading NLTK resource: {resource_name}")
        nltk.download(resource_name)

#-----language detection-----
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        return 'unknown'

#----preprocessing text----
lemmatizer = WordNetLemmatizer()
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = [lemmatizer.lemmatize(word) for word in text.split()]
    tokens = [word for word in tokens if len(word) > 2]  
    
    return ' '.join(tokens)


#---sentiment analysis---
def get_sentiment(text):
    if not isinstance(text, str):
        return None, None, None
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.05:
        category = 'positive'
    elif polarity < -0.05:
        category = 'negative'
    else:
        category = 'neutral'
    return polarity, subjectivity, category

#-----entity recognition-----
def extract_entities(text):
    if not isinstance(text, str):
        return [], [], []
    doc = nlp(text)
    persons = list(set(ent.text for ent in doc.ents if ent.label_ == "PERSON"))
    organizations = list(set(ent.text for ent in doc.ents if ent.label_ == "ORG"))
    locations = list(set(ent.text for ent in doc.ents if ent.label_ == "GPE"))
    return persons, organizations, locations


#-----topic modelling-----
def get_topic_words(model, feature_names, n_top_words=10):
    topic_words = {}
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        topic_words[topic_idx] = top_features
    return topic_words

def run_topic_modeling(text_series, n_topics=5, n_top_words=10, max_features=1000):
    vectorizer = CountVectorizer(max_features=max_features, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(text_series)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(doc_term_matrix)

    feature_names = vectorizer.get_feature_names_out()
    topic_words = get_topic_words(lda, feature_names, n_top_words)
    doc_topics = lda.transform(doc_term_matrix).argmax(axis=1)


    return lda, feature_names, topic_words, doc_topics


#----enrichment pipeline--------
def enrich_news_articles(df: pd.DataFrame, chunk_size):

    enriched_chunks = []
    for start in tqdm(range(0, len(df), chunk_size), desc="Enriching articles"):
        end = start + chunk_size
        chunk = df.iloc[start:end].copy()

        # Language detection
        chunk['language'] = chunk['content'].apply(detect_language)

        # Preprocessing text
        chunk['clean_text'] = chunk['content'].apply(preprocess_text)

        # Sentiment analysis
        chunk[['polarity', 'subjectivity', 'sentiment_category']] = chunk['clean_text'].apply(get_sentiment).apply(pd.Series)

        # Entity recognition
        chunk[['persons', 'organizations', 'locations']] = chunk['clean_text'].apply(extract_entities).apply(pd.Series)


        enriched_chunks.append(chunk)

    return pd.concat(enriched_chunks, ignore_index=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Enrich news articles with NLP techniques.")
    parser.add_argument("input_file", type=str,required=True, help="Path to the input Parquet file containing news articles.")
    parser.add_argument("output_file", type=str, required=True, help="Path to save the enriched Parquet file.")
    args = parser.parse_args()

    download_nltk_resource('wordnet')
    download_nltk_resource('omw-1.4')

    data = pd.read_parquet(args.input_file)

    enriched_data = enrich_news_articles(data, chunk_size=500)

    lda_model,features,top_words,doc_topics = run_topic_modeling(enriched_data['clean_text'], n_topics=6, n_top_words=5, max_features=1000)

    topic_keywords = {topic_id: ', '.join(top_words[topic_id]) for topic_id in top_words.keys()}

    enriched_data['topic_id'] = doc_topics

    enriched_data['topic_keywords'] = enriched_data['topic_id'].map(topic_keywords)

    topic_label_mapping = {
        0: "Education & Development",
        1: "Higher Education",
        2: "Politics",
        3: "Economy",
        4: "Agriculture",
        5: "Local Government"
    }

    enriched_data['topic_label'] = enriched_data['topic_id'].map(topic_label_mapping)

    enriched_data.to_parquet(args.output_file, index=False)
    print(f"Enrichment complete. Data saved to {args.output_file}")
