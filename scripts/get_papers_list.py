import argparse
import pandas as pd
from get_papers.fetch_papers import fetch_papers, filter_non_academic_authors

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output filename for CSV")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    if args.debug:
        print(f"Fetching papers for query: {args.query}")
    
    papers = fetch_papers(args.query)
    filtered_papers = filter_non_academic_authors(papers)
    
    df = pd.DataFrame(filtered_papers)
    
    if args.file:
        df.to_csv(args.file, index=False)
        print(f"Results saved to {args.file}")
    else:
        print(df)

if __name__ == "__main__":
    main()
