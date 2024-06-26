import argparse
from elasticsearch import Elasticsearch
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Analyze recurring sentences in Elasticsearch documents")
parser.add_argument("index_name", help="Name of the Elasticsearch index to search")
parser.add_argument("field_name", help="Name of the field to analyze for recurring sentences")
args = parser.parse_args()

# Download the necessary NLTK data
nltk.download('punkt', quiet=True)

# Get Elasticsearch connection details from environment variables
es_host = os.getenv('ES_HOST', 'https://localhost:9200')
es_user = os.getenv('ES_USER', 'elastic')
es_password = os.getenv('ES_PASSWORD')

if not es_password:
    raise ValueError("ES_PASSWORD must be set in the .env file")

# Connect to Elasticsearch using environment variables
es = Elasticsearch(
    [es_host],
    basic_auth=(es_user, es_password),
    ca_certs="/app/ca_cert.crt"
)

# Define the search query with random sampling
search_query = {
    "size": 10000,
    "query": {
        "function_score": {
            "query": {"match_all": {}},
            "random_score": {}
        }
    }
}

# Perform the search
result = es.search(index=args.index_name, body=search_query)

def get_start_end_sentences(text, num_sentences=5):
    sentences = sent_tokenize(text)
    start_sentences = sentences[:num_sentences]
    end_sentences = sentences[-num_sentences:]
    return start_sentences, end_sentences

# Process results
start_sentences = []
end_sentences = []

for hit in result['hits']['hits']:
    body_content = hit['_source'].get(args.field_name, '')
    start, end = get_start_end_sentences(body_content)
    start_sentences.extend(start)
    end_sentences.extend(end)

# Count sentence occurrences
start_counts = Counter(start_sentences)
end_counts = Counter(end_sentences)

# Find recurring sentences (occurring in more than one document)
recurring_start = [sentence for sentence, count in start_counts.items() if count > 1]
recurring_end = [sentence for sentence, count in end_counts.items() if count > 1]

# Sort recurring sentences by frequency (most frequent first)
recurring_start.sort(key=lambda s: start_counts[s], reverse=True)
recurring_end.sort(key=lambda s: end_counts[s], reverse=True)

# Print results
print(f"Analyzed {len(result['hits']['hits'])} randomly sampled documents from index '{args.index_name}', field '{args.field_name}'")

print("\nRecurring sentences at the beginning of documents:")
for sentence in recurring_start[:10]:  # Print top 10 most common start sentences
    print(f"- {sentence} (Occurrences: {start_counts[sentence]})")

print("\nRecurring sentences at the end of documents:")
for sentence in recurring_end[:10]:  # Print top 10 most common end sentences
    print(f"- {sentence} (Occurrences: {end_counts[sentence]})")
