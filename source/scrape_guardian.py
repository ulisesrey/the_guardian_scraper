"""
Module to scrape the Guardian newspaper website for headlines on a given date.
"""

import requests
from bs4 import BeautifulSoup
import random
import time
import logging
from datetime import datetime

# Set up logging to output to a file and to the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

# Define some User-Agent strings for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5412.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5361.172 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5388.177 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5397.215 Safari/537.36'
]   

def scrape_guardian_headlines(date):
    """
    Scrape the Guardian newspaper website for headlines on a given date.
    """
    # Construct the URL based on date
    date_str = date.strftime('%Y/%b/%d').lower()
    url = f"https://www.theguardian.com/world/{date_str}"
  
    # Choose a random User-Agent and log it
    user_agent = random.choice(USER_AGENTS)
    headers = {'User-Agent': user_agent}
    logging.info(f"Using User-Agent: {user_agent}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching data for {date_str}: {e}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    # Locate all articles and extract headlines
    for article in soup.find_all('h3'):
        headline_text = article.get_text().strip()
        if headline_text:
            headlines.append(headline_text)

    # Log the number of headlines found
    logging.info(f"Found {len(headlines)} headlines for {date_str}")

    # Add a random delay to mimic human behavior
    time.sleep(random.uniform(0, 1))  # Random delay between 0 and 1 seconds
    
    return headlines
