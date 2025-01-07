import requests
import pandas as pd
from typing import List, Dict, Tuple

def fetch_papers(query: str) -> List[Dict]:
    base_url = "https://pubmed.ncbi.nlm.nih.gov/api/query"
    response = requests.get(f"{base_url}?term={query}&format=abstract")

    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:500]}")  # Print the first 500 characters
    
    if response.status_code != 200:
        raise Exception("Failed to fetch data from PubMed API")
    
    try:
        papers = response.json().get('results', [])
    except ValueError as e:
        raise Exception(f"Failed to parse JSON: {e}")
    # if response.status_code != 200:
    #     raise Exception("Failed to fetch data from PubMed API")
    
    # papers = response.json().get('results', [])
    return papers

def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    filtered_papers = []
    for paper in papers:
        authors = paper.get('authors', [])
        non_academic_authors = []
        company_affiliations = []
        
        for author in authors:
            if "university" not in author['affiliation'].lower() and \
               "lab" not in author['affiliation'].lower():
                non_academic_authors.append(author['name'])
                company_affiliations.append(author['affiliation'])
        
        if non_academic_authors:
            filtered_papers.append({
                "PubmedID": paper['id'],
                "Title": paper['title'],
                "Publication Date": paper['pub_date'],
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": paper.get('corresponding_author_email', '')
            })
    
    return filtered_papers