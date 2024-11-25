# Web Scraper

This project uses Python to scrape data from major Canadian news sources and analyze the frequency of mentions for Canadian provinces/territories and countries.

## Overview

The script retrieves data from the following sources:
- CBC News
- CBC World
- Windspeaker (Indigenous News)

It analyzes which Canadian province/territory is most frequently mentioned in CBC News and Windspeaker, and which country is most frequently mentioned in CBC World.

## Features

- **Data Retrieval**: Accesses and cleans HTML content from specified URLs.
- **Data Analysis**: Counts occurrences of provinces/territories and countries.
- **Results Display**: Prints the analysis results, highlighting the most mentioned regions.

## Usage

1. Ensure you have the required dependencies installed:
   ```sh
   pip install certifi pycountry
   ```
