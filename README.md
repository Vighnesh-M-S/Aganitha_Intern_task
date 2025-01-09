# Get Papers List(Aganiths_Intern_task)

This project fetches research papers from PubMed based on a query, filters out non-academic authors, and generates a CSV file with relevant details. 

## Project Organization
```
project/
├── get_papers/
│   ├── fetch_papers.py         # Module to fetch and filter papers
├── scripts/
│   ├── get_papers_list.py      # Command-line program to use the module
├── tests/                      # Directory for test cases
├── README.md                   # Project documentation
├── pyproject.toml              # Poetry configuration
├── dist/                       # Generated distribution files for publishing
```


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/get_papers.git
   cd get_papers

2. Install dependencies:
   ```bash
   poetry install

## Usage

1. Run the command-line program to fetch papers and generate a CSV file:
   ```bash
   poetry run python3 scripts/get_papers_list.py "<search_query>" -f <output_file> -d

## Command-Line Arguments
| Argument      | Description                                | Example                          |
|---------------|--------------------------------------------|----------------------------------|
| --query       | Search query for PubMed                    | "cancer research"                |
| --output      | Name of the output CSV file                | "pubmed_data.csv"                |

2. Example:
   ```bash
   poetry run python3 scripts/get_papers_list.py "cancer treatment" -f results.csv -d

## Output Format
The generated CSV file will have the following columns:

| Column Name              | Description                                                     |
|--------------------------|-----------------------------------------------------------------|
| PubmedID                 | Unique identifier for the paper                                 |
| Title                    | Title of the paper                                              |
| Publication Date         | Date the paper was published                                    |
| Non-academic Author(s)   | Names of authors affiliated with non-academic institutions      |
| Company Affiliation(s)   | Names of pharmaceutical/biotech companies                      |
| Corresponding Author Email | Email address of the corresponding author                      |

## Tools and Libraries Used
The following tools and libraries are used in this project:

- **Python**: The programming language used to develop the script.
- **Poetry**: For dependency management and packaging. [Link](https://python-poetry.org/)
- **Requests**: To fetch data from the PubMed API. [Link](https://docs.python-requests.org/en/latest/)
- **Pandas**: For data manipulation and CSV generation. [Link](https://pandas.pydata.org/)
- **Argparse**: For command-line argument parsing. [Link](https://docs.python.org/3/library/argparse.html)

## Publishing the Module
The module can be published to Test PyPI using the following steps:

### Build the package:
```bash
poetry build
```

### Upload to Test PyPI:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
For more information, refer to the [Test PyPI Guide](https://packaging.python.org/guides/using-testpypi/).

## Troubleshooting
- Ensure you have an active internet connection to access the PubMed API.
- If you encounter authentication issues while uploading to Test PyPI, verify your token and credentials.
