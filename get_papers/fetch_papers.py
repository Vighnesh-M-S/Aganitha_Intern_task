import requests
import pandas as pd
from typing import List, Dict, Tuple


def fetch_papers(query: str) -> List[Dict]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",          # Database to search in
        "term": query,           # Search query
        "retmode": "json",       # Response format
        "retmax": 100            # Max number of results to return
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from PubMed API. Status code: {response.status_code}")
    
    try:
        data = response.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return [{"id": id} for id in id_list]
    except ValueError as e:
        raise Exception(f"Failed to parse JSON: {e}")

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch paper details. Status code: {response.status_code}")
    
    try:
        data = response.json()
        return [
            {
                "id": paper_id,
                "title": summary.get("title", ""),
                "authors": summary.get("authors", []),
                "pub_date": summary.get("pubdate", "")
            }
            for paper_id, summary in data.get("result", {}).items()
            if paper_id != "uids"
        ]
    except ValueError as e:
        raise Exception(f"Failed to parse JSON: {e}")

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