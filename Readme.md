# Elasticsearch Recurring Sentence Analyzer

This Docker container runs a Python script that analyzes recurring sentences at the beginning and end of documents in an Elasticsearch index.

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
  elasticsearch-analyzer <index_name> <field_name>
```

Replace the following:
- `/path/to/your/ca_cert.crt`: The path to your Elasticsearch CA certificate on your host machine.
- `/path/to/your/.env`: The path to your .env file on your host machine.
- `<index_name>`: The name of the Elasticsearch index you want to analyze.
- `<field_name>`: The name of the field in the documents that contains the text to analyze.

For example:

```bash
docker run -it --network host \
  -v /Users/kent/github/servicenow-utils/http_ca.crt:/app/ca_cert.crt \
  -v /Users/kent/github/servicenow-utils/.env:/app/.env \
  elasticsearch-analyzer www-ornl body_content
```

This command does the following:
- `-it`: Runs the container interactively.
- `--network host`: Uses the host's network, allowing the container to connect to your local Elasticsearch instance.
- `-v /path/to/your/ca_cert.crt:/app/ca_cert.crt`: Mounts your CA certificate into the container.
- `-v /path/to/your/.env:/app/.env`: Mounts your .env file into the container.

Example output

```
Analyzed 10000 randomly sampled documents from index 'www-ornl', field 'body_content'

Recurring sentences at the beginning of documents:
- Credit: Carlos Jones/ORNL, U.S. Dept. (Occurrences: 57)
- Credit: ORNL, U.S. Dept. (Occurrences: 36)
- Oak Ridge National Laboratory 1 Bethel Valley Road Oak Ridge, TN 37830 (+1) 865.576.7658 Connect With Us Partnerships Visit Contact News Newsroom Newsletter Signup Media Contacts Research Science Areas User Facilities Centers & Institutes Resources Internal Users Directory Oak Ridge National Laboratory is managed by UT-Battelle LLC for the US Department of Energy Privacy Accessibility/508 Nondiscrimination/1557 Vulnerability Disclosure Program (Occurrences: 30)
- He received his B.S. (Occurrences: 26)
- Media may use the resources listed below or send questions to news@ornl.gov . (Occurrences: 18)
- Credit: Genevieve Martin/ORNL, U.S. Dept. (Occurrences: 15)
- Dept. (Occurrences: 12)
- Skip to main content twitter facebook linkedin youtube flickr Partnerships Visit Contact Menu Science Areas Biology & Environment Clean Energy Fusion & Fission Isotopes Physical Sciences National Security Neutron Science Supercomputing Work With Us User Facilities Educational Programs Procurement Small Business Programs About Us Overview Leadership Team Initiatives Visiting ORNL Our Values Community Diversity History Fact Sheets Virtual Tour Careers News Hit enter to search or ESC to close Sheng Dai SH-RPR Separations and Polymer Chemistry Contact dais@ornl.gov | 865.576.7307 Bio Dr. Sheng Dai is currently a corporate fellow and section head overseeing four research groups in the areas of separations and polymer chemistry at Chemical Sciences Division, Oak Ridge National Laboratory (ORNL) and a Professor of Chemistry at the University of Tennessee, Knoxville (UTK). (Occurrences: 11)
- His current research interests include ionic liquids, porous materials, and their applications for separation sciences and energy storage as well as catalysis by nanomaterials. (Occurrences: 11)
- He was named US DOE Distinguished Scientist Fellow for pioneering advances in development of functional materials in 2022. (Occurrences: 11)

Recurring sentences at the end of documents:
- For more information, please visit energy.gov/science . (Occurrences: 136)
- The Office of Science is working to address some of the most pressing challenges of our time. (Occurrences: 120)
- DOE’s Office of Science is working to address some of the most pressing challenges of our time. (Occurrences: 105)
- Oak Ridge National Laboratory 1 Bethel Valley Road Oak Ridge, TN 37830 (+1) 865.576.7658 Connect With Us Partnerships Visit Contact News Newsroom Newsletter Signup Media Contacts Research Science Areas User Facilities Centers & Institutes Resources Internal Users Directory Oak Ridge National Laboratory is managed by UT-Battelle LLC for the US Department of Energy Privacy Accessibility/508 Nondiscrimination/1557 Vulnerability Disclosure Program (Occurrences: 75)
- UT-Battelle manages ORNL for the Department of Energy’s Office of Science, the single largest supporter of basic research in the physical sciences in the United States. (Occurrences: 58)
- The Office of Science is the single largest supporter of basic research in the physical sciences in the United States, and is working to address some of the most pressing challenges of our time. (Occurrences: 49)
- Media Contact Communications Staff news@ornl.gov 865.576.1946 Oak Ridge National Laboratory 1 Bethel Valley Road Oak Ridge, TN 37830 (+1) 865.576.7658 Connect With Us Partnerships Visit Contact News Newsroom Newsletter Signup Media Contacts Research Science Areas User Facilities Centers & Institutes Resources Internal Users Directory Oak Ridge National Laboratory is managed by UT-Battelle LLC for the US Department of Energy Privacy Accessibility/508 Nondiscrimination/1557 Vulnerability Disclosure Program (Occurrences: 46)
- For more information, please visit http://energy.gov/science/ . (Occurrences: 45)
- For more information, visit https://energy.gov/science . (Occurrences: 37)
- UT-Battelle manages ORNL for DOE’s Office of Science, the single largest supporter of basic research in the physical sciences in the United States. (Occurrences: 36)
```

## Notes

- Ensure your Elasticsearch instance is running and accessible.
- The script uses the connection details specified in the .env file.
- The script analyzes a random sample of 10,000 documents from the specified index.

## Security Note

The .env file contains sensitive information. Make sure to keep it secure and never commit it to version control systems.
