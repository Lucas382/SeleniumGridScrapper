# Selenium grid scraper

## Instructions to run:

1. Install the dependencies with the `pip install -r requirements.txt` command.
2. Create the *selenium grid container* with the `docker compose up` command.
3. Run the book-scrapper.py file.

---

## How it works?

This script porpouse is to scrapp books data from `https://books.toscrape.com`, 
using selenium grid it create concurrent sessions to scrape all data from many pages and put ir on a csv file.

***Note: The website being scraped is open for scraping, and Selenium is not necessary. 
However, it's worth noting that this script was created as a training exercise, hence the use of Selenium despite it not being necessary.***
