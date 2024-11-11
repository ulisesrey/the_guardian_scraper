"""
Module to scrape the Guardian newspaper website for headlines on a given date.
"""
"""
Module to scrape the Guardian newspaper website for headlines on a given date.
"""

import requests
from bs4 import BeautifulSoup

def scrape_guardian_headlines(date):
    """
    Scrape the Guardian newspaper website for headlines on a given date.
    """
    # Construct the URL based on date
    date_str = date.strftime('%Y/%b/%d').lower()
    url = f"https://www.theguardian.com/world/{date_str}"
  
    # Define a user agent to avoid 403 error
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {date_str}: {e}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    # Locate all articles and extract headlines
    for article in soup.find_all('h3'):
        headline_text = article.get_text().strip()
        if headline_text:
            headlines.append(headline_text)
    
    return headlines
