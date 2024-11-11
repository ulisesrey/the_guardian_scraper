"""
Main script to run the web scraper
"""

import argparse
from datetime import datetime, timedelta
import pandas as pd
from scrape_guardian import scrape_guardian_headlines
from utils import save_to_csv
import os

def main(start_date, end_date):
    all_headlines = []
    
    # Parse the start and end dates from arguments
    current_date = start_date
    while current_date <= end_date:
        print(f"Scraping date: {current_date.strftime('%Y-%m-%d')}")
        headlines = scrape_guardian_headlines(current_date)
        
        # Append each headline with the date to our list
        for headline in headlines:
            all_headlines.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "headline": headline
            })
        
        current_date += timedelta(days=1)

    # Convert the list of headlines to a DataFrame
    df = pd.DataFrame(all_headlines, columns=["date", "headline"])
    
    # Save to CSV
    print(os.getcwd())
    save_to_csv(df, "datasets/guardian_headlines.csv")
    print("Data collection completed and saved to dataset/guardian_headlines.csv")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scrape headlines from The Guardian within a date range.")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert input strings to datetime objects
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    # Run the main function with parsed dates
    main(start_date, end_date)
