"""
Module to scrape the Guardian newspaper website for headlines on a given date.
"""

import requests
from bs4 import BeautifulSoup
import random
import time
import logging
from datetime import datetime

import pandas as pd

# Set up logging to output to a file and to the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        #logging.StreamHandler() # To show message on terminal
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


def get_random_user_agent():
    """
    Return haders from a random User-Agent string, and user agent string.
    """
    user_agent = random.choice(USER_AGENTS)
    headers = {'User-Agent': user_agent}
    return headers, user_agent

def scrape_guardian_headlines(date):
    """
    Scrape the Guardian newspaper website for headlines on a given date.
    """
    # Construct the URL based on date
    date_str = date.strftime('%Y/%b/%d').lower()
    url = f"https://www.theguardian.com/world/{date_str}"
  
    # Choose a random User-Agent and log it
    headers, user_agent = get_random_user_agent()
    logging.info(f"Using User-Agent: {user_agent}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching data for {date_str}: {e}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # declare emtpy lists to store the authors, headlines and topics
    authors, headlines, all_topics = [], [], []
    
    # Locate all articles and extract information
    for headline3 in soup.find_all('h3'):
        a_tag = headline3.find('a')
        
        # Ensure there is a link in the a_tag
        if a_tag and a_tag.get("href"):
            article_url = a_tag.get("href")
            author, headline, topics = scrape_article(article_url, content=False)
            
            authors.append(author)
            headlines.append(headline)
            all_topics.append(topics)

    # Add a random delay to mimic human behavior
    time.sleep(random.uniform(0, 1))  # Random delay between 0 and 1 seconds
    
    return authors, headlines, all_topics


def scrape_article(url, content=False):
    """
    Scrape the content of a single article from the Guardian website.
    By default does not return the content of the article to be faster.
    """

    # Choose a random User-Agent and log it
    headers, user_agent = get_random_user_agent()
    logging.info(f"Using User-Agent: {user_agent}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching data for {url}: {e}")
        return []

    # access the article content
    soup = BeautifulSoup(response.content, 'html.parser')


    #get the author
    try:
        author = soup.find("a", rel="author").get_text(strip=True)
    except AttributeError:
        author = "No author found"
    # TODO: Do something if author is not found like this, for instance Associated Press, or no author.


    # find the headline in h1 tag
    try:
        headline = soup.find("h1").get_text(strip=True)
    except AttributeError:
        headline = "No headline found"

    #g et the topics
    try:
        topics = soup.find("meta", property="article:tag").get("content", "").strip(",")
    except AttributeError:
        topics = "No topics found"
    # article content
    if content is True:
        main_content = soup.find("div", {"id": "maincontent"})

        # Extract all paragraphs within the main content
        if main_content:
            paragraphs = main_content.find_all("p")  # Find all <p> tags
            article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)  # Combine and clean text

        return author, headline, topics, article_content
    else:
        return author, headline, topics

# if __name__ == "__main__":
#     # Scrape headlines for a specific date
#     date = datetime(2021, 6, 1)
#     headlines = scrape_guardian_headlines(date)
#     #print(headlines)

