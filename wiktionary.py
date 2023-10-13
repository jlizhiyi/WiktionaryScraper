import requests
from bs4 import BeautifulSoup
import re
import csv

# URL of the initial category page
category_url = 'https://en.wiktionary.org/wiki/Category:Chinese_Han_characters'

# Create a CSV file to store the results
csv_filename = 'chinese_characters_with_pinyin.csv'

# Create a session to maintain cookies and session data
session = requests.Session()

# Set the maximum number of characters to scrape (approx. 1000)
max_characters_to_scrape = 10000

# Initialize a counter for the scraped characters
character_count = 0

while character_count < max_characters_to_scrape:
    # Send an HTTP GET request to the category page
    category_response = session.get(category_url)

    # Check if the request was successful (status code 200)
    if category_response.status_code == 200:
        # Parse the HTML content of the category page
        category_soup = BeautifulSoup(category_response.text, 'html.parser')

        # Find all links in the category page
        links = category_soup.find_all('a')

        # Create a list to store successful results
        results = []

        for link in links:
            link_href = link.get('href')
            # Check if the link points to a Chinese character page
            if link_href and link_href.startswith('/wiki/') and not link_href.startswith('/wiki/Category:'):
                character_page_url = 'https://en.wiktionary.org' + link_href

                # Send an HTTP GET request to the character's page
                character_response = session.get(character_page_url)

                # Check if the request was successful (status code 200)
                if character_response.status_code == 200:
                    character_soup = BeautifulSoup(character_response.text, 'html.parser')

                    # Find the element containing the Hanyu Pinyin
                    pinyin_element = character_soup.find('span', class_='form-of pinyin-ts-form-of')

                    # Extract the Hanyu Pinyin text
                    if pinyin_element:
                        hanyu_pinyin = pinyin_element.text.strip()
                        # Use regular expression to extract just the 'hao3' part
                        match = re.search(r'\(([^)]+)\)', hanyu_pinyin)
                        if match:
                            hanyu_pinyin_without_diacritics = match.group(1)
                            # Split the Pinyin by ',' or '.'
                            pronunciations = re.split(r'[,.]', hanyu_pinyin_without_diacritics)
                            # Take the first pronunciation
                            first_pronunciation = pronunciations[0].strip()
                            # Append the result to the list
                            print(f"Chinese character: {link.text}, Hanyu Pinyin: {first_pronunciation}")
                            results.append((link.text, first_pronunciation))
                            character_count += 1

        # Write the results to a CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write the results
            csv_writer.writerows(results)

        # Check if there is a link to the next page
        next_page_link = category_soup.find('a', text='next page')
        if next_page_link:
            # Update the category URL to the URL of the next page
            category_url = 'https://en.wiktionary.org' + next_page_link.get('href')
        else:
            # No more pages, break out of the loop
            break
    else:
        print(f"Failed to retrieve the category page. Status code: {category_response.status_code}")

print(f"Scraped {character_count} characters. Results have been saved to {csv_filename}")
