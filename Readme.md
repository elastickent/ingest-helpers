# Elasticsearch Recurring Sentence Analyzer

This Docker container runs a Python script that analyzes recurring sentences at the beginning and end of documents in an Elasticsearch index. It can also generate an ingest pipeline to remove these common sentences and provide instructions for reindexing.

## Prerequisites

- Docker installed on your system
- Access to an Elasticsearch instance

## Setup

1. Clone this repository or copy all files to a local directory.
2. Create a `.env` file in the same directory with the following content:

```
ES_HOST=https://your_elasticsearch_host:9200
ES_USER=your_username
ES_PASSWORD=your_password
```

Replace the values with your actual Elasticsearch connection details.

## Building the Docker Container

1. Open a terminal and navigate to the directory containing the Dockerfile.
2. Build the Docker image with the following command:

```bash
docker build -t elasticsearch-analyzer .
```

This command builds a Docker image and tags it as `elasticsearch-analyzer`.

## Running the Script

To run the script, use the following command:

```bash
docker run -it --network host \
  -v /path/to/your/ca_cert.crt:/app/ca_cert.crt \
  -v /path/to/your/.env:/app/.env \
  elasticsearch-analyzer <index_name> <field_name> [--output-pipeline]
```

Replace the following:
- `/path/to/your/ca_cert.crt`: The path to your Elasticsearch CA certificate on your host machine.
- `/path/to/your/.env`: The path to your .env file on your host machine.
- `<index_name>`: The name of the Elasticsearch index you want to analyze.
- `<field_name>`: The name of the field in the documents that contains the text to analyze.
- `[--output-pipeline]`: Optional flag to generate and print an Elasticsearch ingest pipeline and reindex instructions.

For example:

```bash
docker run -it --network host \
  -v /Users/kent/github/servicenow-utils/http_ca.crt:/app/ca_cert.crt \
  -v /Users/kent/github/servicenow-utils/.env:/app/.env \
  elasticsearch-analyzer www-ornl body_content --output-pipeline
```

This command does the following:
- `-it`: Runs the container interactively.
- `--network host`: Uses the host's network, allowing the container to connect to your local Elasticsearch instance.
- `-v /path/to/your/ca_cert.crt:/app/ca_cert.crt`: Mounts your CA certificate into the container.
- `-v /path/to/your/.env:/app/.env`: Mounts your .env file into the container.

## Ingest Pipeline and Reindexing

If you use the `--output-pipeline` flag, the script will generate and print:
1. An Elasticsearch ingest pipeline definition
2. A reindex command
3. Instructions for using these in Kibana's Dev Console

To use the generated pipeline and reindex your data:

1. Run the script with the `--output-pipeline` flag.
2. Copy the output between the "Elasticsearch Ingest Pipeline" delimiters and execute it in Kibana's Dev Console.
3. Copy the output between the "Reindex Command" delimiters and execute it in Kibana's Dev Console.
4. Follow the printed instructions to verify and start using your new, cleaned index.

Example of saving the output to a file:

```bash
docker run -it --network host \
  -v /path/to/your/ca_cert.crt:/app/ca_cert.crt \
  -v /path/to/your/.env:/app/.env \
  elasticsearch-analyzer www-ornl body_content --output-pipeline > pipeline_and_reindex_commands.txt
```

This will save the entire output, including the pipeline, reindex command, and instructions to `pipeline_and_reindex_commands.txt`.

## Notes

- Ensure your Elasticsearch instance is running and accessible.
- The script uses the connection details specified in the .env file.
- The script analyzes a random sample of 10,000 documents from the specified index.
- The script extracts the first and last 5 sentences from each document for analysis. You can modify this by changing the `num_sentences` parameter in the `get_start_end_sentences()` function in the script.

## Security Note

The .env file contains sensitive information. Make sure to keep it secure and never commit it to version control systems.

## Troubleshooting

If you encounter connection issues:
1. Ensure your Elasticsearch instance is running and accessible from your host machine.
2. Check that the ES_HOST in your .env file is correct and accessible from within the Docker container.
3. Verify that the CA certificate path is correct and the certificate is valid.

## Customization

You can modify the script to change the number of documents sampled or the number of sentences analyzed from each document. These changes would require rebuilding the Docker image.

## Contributing

Feel free to fork this repository and submit pull requests with any enhancements.

