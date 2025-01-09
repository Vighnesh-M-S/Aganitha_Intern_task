import argparse
import pandas as pd
from get_papers.fetch_papers import fetch_papers, filter_non_academic_authors, fetch_paper_details

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output filename for CSV")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    if args.debug:
        print(f"Fetching papers for query: {args.query}")
    
    paper_ids = fetch_papers(args.query)
    if args.debug:
        print(f"Fetched {len(paper_ids)} paper IDs")
    
    # Fetch detailed paper information
    paper_details = fetch_paper_details([paper["id"] for paper in paper_ids])
    if args.debug:
        print(f"Fetched details for {len(paper_details)} papers")
    
    filtered_papers = filter_non_academic_authors(paper_details)
    
    # Convert to DataFrame
    df = pd.DataFrame(filtered_papers)
    
    if args.file:
        df.to_csv(args.file, index=False)
        print(f"Results saved to {args.file}")
    else:
        print(df)

if __name__ == "__main__":
    main()
