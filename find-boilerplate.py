import argparse
from elasticsearch import Elasticsearch
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Analyze recurring sentences in Elasticsearch documents")
parser.add_argument("index_name", help="Name of the Elasticsearch index to search")
parser.add_argument("field_name", help="Name of the field to analyze for recurring sentences")
parser.add_argument("--output-pipeline", action="store_true", help="Output Elasticsearch ingest pipeline")
args = parser.parse_args()

# Download the necessary NLTK data
nltk.download('punkt', quiet=True)

# Get Elasticsearch connection details from .env file
es_host = os.getenv('ES_HOST', 'https://localhost:9200')
es_user = os.getenv('ES_USER', 'elastic')
es_password = os.getenv('ES_PASSWORD')

if not es_password:
    raise ValueError("ES_PASSWORD must be set in the .env file")

# Connect to Elasticsearch 
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

# Output Elasticsearch ingest pipeline if flag is set
if args.output_pipeline:
    pipeline = {
        "description": "Pipeline to remove common start and end sentences",
        "processors": []
    }

    for sentence in recurring_start[:10] + recurring_end[:10]:
        escaped_sentence = re.escape(sentence).replace('/', '\\/')
        processor = {
            "gsub": {
                "field": args.field_name,
                "pattern": f"^{escaped_sentence}\\s*|\\s*{escaped_sentence}$",
                "replacement": ""
            }
        }
        pipeline["processors"].append(processor)

    print("\n--- Elasticsearch Ingest Pipeline ---")
    print("PUT _ingest/pipeline/remove_common_sentences")
    print(json.dumps(pipeline, indent=2))
    print("---------------------------------------")

    print("\n--- Reindex Command ---")
    reindex_body = {
        "source": {
            "index": args.index_name
        },
        "dest": {
            "index": f"{args.index_name}_cleaned",
            "pipeline": "remove_common_sentences"
        }
    }
    print("POST _reindex")
    print(json.dumps(reindex_body, indent=2))
    print("------------------------")

    print("\nInstructions:")
    print("1. Copy and paste the Elasticsearch Ingest Pipeline into Kibana's Dev Console and execute it.")
    print("2. Then, copy and paste the Reindex Command into the Dev Console and execute it.")
    print("3. This will create a new index called '{}_cleaned' with the common sentences removed.".format(args.index_name))
    print("4. After reindexing, verify the new index and update your applications to use the new index if everything looks correct.")
