import requests
import pandas as pd
from typing import List, Dict, Tuple

# Function to fetch PubMed paper IDs based on a search query
def fetch_papers(query: str) -> List[Dict]:
    """
    Fetches a list of PubMed paper IDs for the given query.
    
    Parameters:
        query (str): The search query to fetch papers for.

    Returns:
        List[Dict]: A list of dictionaries, each containing a paper ID.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",          # Database to search in
        "term": query,           # Search query
        "retmode": "json",       # Response format
        "retmax": 100            # Max number of results to return
    }

    # Make a GET request to the PubMed API
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from PubMed API. Status code: {response.status_code}")

    try:
        # Parse the JSON response
        data = response.json()
        # Extract the list of paper IDs
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return [{"id": id} for id in id_list]
    except ValueError as e:
        raise Exception(f"Failed to parse JSON: {e}")

# Function to fetch detailed metadata for a list of PubMed paper IDs
def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    """
    Fetches detailed information for a list of PubMed paper IDs.
    
    Parameters:
        paper_ids (List[str]): A list of PubMed paper IDs.

    Returns:
        List[Dict]: A list of dictionaries, each containing metadata for a paper.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",              # Database to fetch details from
        "id": ",".join(paper_ids),   # Comma-separated list of paper IDs
        "retmode": "json"            # Response format
    }

    # Make a GET request to fetch paper details
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch paper details. Status code: {response.status_code}")

    try:
        # Parse the JSON response
        data = response.json()
        return [
            {
                "id": paper_id,
                "title": summary.get("title", ""),        # Extract paper title
                "authors": summary.get("authors", []),   # Extract list of authors
                "pub_date": summary.get("pubdate", "")   # Extract publication date
            }
            for paper_id, summary in data.get("result", {}).items()
            if paper_id != "uids"  # Skip the 'uids' key, which is metadata
        ]
    except ValueError as e:
        raise Exception(f"Failed to parse JSON: {e}")

# Function to filter non-academic authors from the paper metadata
def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """
    Filters out non-academic authors based on their affiliations.
    
    Parameters:
        papers (List[Dict]): A list of dictionaries, each containing paper metadata.

    Returns:
        List[Dict]: A list of dictionaries with filtered metadata for papers 
                    with non-academic authors.
    """
    filtered_papers = []
    for paper in papers:
        authors = paper.get('authors', [])  # Get the list of authors
        non_academic_authors = []           # List to store non-academic authors
        company_affiliations = []           # List to store company affiliations

        for author in authors:
            # Use .get() to handle missing keys gracefully
            affiliation = author.get('affiliation', '').lower()
            if "university" not in affiliation and "lab" not in affiliation:
                # Add non-academic authors and their affiliations
                non_academic_authors.append(author.get('name', 'Unknown Author'))
                company_affiliations.append(author.get('affiliation', 'Unknown Affiliation'))

        if non_academic_authors:
            # Add the filtered paper details to the result list
            filtered_papers.append({
                "PubmedID": paper['id'],                        # Paper ID
                "Title": paper['title'],                        # Paper title
                "Publication Date": paper['pub_date'],          # Publication date
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": paper.get('corresponding_author_email', 'Unknown Email')
            })

    return filtered_papers
