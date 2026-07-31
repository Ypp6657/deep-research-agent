import sys
import argparse
from graph import run_research
from core.logger import logger

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    parser = argparse.ArgumentParser(description="Deep Research Agent")
    parser.add_argument("query", nargs="?", type=str, help="Research query")
    args = parser.parse_args()

    query = args.query
    if not query:
        print("Welcome to Deep Research Agent!")
        try:
            query = input("Enter your research query: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            sys.exit(0)

    if not query.strip():
        print("Query cannot be empty. Exiting.")
        sys.exit(1)

    logger.info(f"Starting research for query: {query}")
    
    try:
        report = run_research(query)
        if report:
            print("\n" + "="*50)
            print("RESEARCH REPORT GENERATED")
            print("="*50)
            print(f"Title: {report.title}")
            print(f"\nExecutive Summary:\n{report.executive_summary}")
            print("="*50)
            print("Research complete. Check outputs folder for markdown and PDF files.")
        else:
            print("Research failed to generate a report.")
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
