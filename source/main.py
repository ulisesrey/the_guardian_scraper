"""
Main script to run the web scraper
"""

import argparse
from datetime import datetime, timedelta
import csv
import os
from scrape_guardian import scrape_guardian_headlines

def main(start_date, end_date, output_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Open the CSV file once and set up the writer
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "authors", "headline", "topics"])  # Write header
        
        current_date = start_date
        while current_date <= end_date:
            print(f"Scraping date: {current_date.strftime('%Y-%m-%d')}")
            authors, headlines, topics = scrape_guardian_headlines(current_date)
            
        
            # Write each headline, author, and topic to the CSV file immediately
            for i in range(len(headlines)):
                writer.writerow([current_date.strftime('%Y-%m-%d'), authors[i], headlines[i], topics[i]])

                
            current_date += timedelta(days=1)
    print(f"Data collection completed and saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scrape headlines from The Guardian within a date range.")
    parser.add_argument("-start", "--start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("-end", "--end_date", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("-o", "--output", type=str, default="dataset/guardian_headlines.csv",
                        help="Output file path for the CSV file (default: dataset/guardian_headlines.csv)")

    # Parse arguments
    args = parser.parse_args()
    
    # Convert input strings to datetime objects
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Run the main function with parsed dates and output file path
    main(start_date, end_date, args.output)
