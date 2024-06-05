# Menu Scraper

## Problem Statement
Design an image server.
Scrape menu images for restaurants in Mumbai
OCR the menu, read items and prices
Store Items and prices on any database

## Implementation Details
Made using python and mongodb database
Deployed and served as api using FastAPI for easier access and testing.
The environment variables are hardcoded so as to enable easy access.
Menus are served using dineout website.
The query in the api works same as search term in Swiggy Dineout.
Some of the restaurants block the access or show not found(mostly the newer ones). So I have added some restaurants as test cases.
The results of database are cached so that scraping is not performed redundantly.

## Reasonings
1. Used a regex string to filter out the response from the scraped text. Every menu has its differences and image quality also varies.Some of the results will not be totally accurate.
    String used:
    ```
    pattern = r'[•\-\s>]+\s*([A-Za-z\s\(\)\']+)\s*[•\-\s>]+\s*(\d+)(?:\n|$)'
    ```


## Build Command

### Install Dependencies
```
pip install -r requirements.txt
```

```
uvicorn main:app --host 0.0.0.0 --port 8080 --reload 
```



## Test Restaurants
- Amoeba Sports Bar
- Dobaraa
- Sigree Global Grill
- Grandmama's Cafe
- Urban Tadka
