import json
import re
import requests
from bs4 import BeautifulSoup
import argparse
from colorama import init, Fore, Style
import logging

# Initialize colorama
init(autoreset=True)

def fetch_page(url, debug):
    if debug:
        logging.debug(f"Fetching page: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        if debug:
            logging.debug(f"Successfully fetched page: {url}")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def search_for_text(html, text, debug):
    if debug:
        logging.debug(f"Searching for text: {text} in HTML content")
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(string=lambda s: text in s)
    if debug:
        logging.debug(f"Found {len(results)} occurrences of text: {text}")
    return results

def extract_username(html, debug):
    if debug:
        logging.debug("Extracting username from HTML content")
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='actual_persona_name')
    username = span.text if span else None
    if debug:
        logging.debug(f"Extracted username: {username}")
    return username

def extract_days(text, debug):
    if debug:
        logging.debug(f"Extracting days since last ban from text: {text}")
    match = re.search(r'(\d+) day\(s\) since last ban', text)
    days = int(match.group(1)) if match else None
    if debug:
        logging.debug(f"Extracted days: {days}")
    return days

def get_urls_from_json(file_path, debug):
    if debug:
        logging.debug(f"Loading URLs from JSON file: {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    if debug:
        logging.debug(f"Loaded {len(data['urls'])} URLs from JSON file")
    return data['urls']

def load_previous_data(file_path, debug):
    if debug:
        logging.debug(f"Loading previous data from JSON file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if debug:
            logging.debug("Successfully loaded previous data")
        return data
    except FileNotFoundError:
        if debug:
            logging.warning("Previous data file not found, starting with empty data.")
        return {}

def save_current_data(file_path, data, debug):
    if debug:
        logging.debug(f"Saving current data to JSON file: {file_path}")
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    if debug:
        logging.debug("Successfully saved current data")

def update_previous_data(previous_data, url, username, days, debug):
    if debug:
        logging.debug(f"Updating previous data for URL: {url}")
    previous_data[url] = {'username': username, 'days_since_last_ban': days if days is not None else -1}
    if debug:
        logging.debug(f"Updated data: {previous_data[url]}")

def check_new_bans(url_file, search_text, data_file, debug):
    urls = get_urls_from_json(url_file, debug)
    previous_data = load_previous_data(data_file, debug)

    print("Scanning has begun...")
    if debug:
        logging.debug("Started scanning URLs")

    new_bans_detected = False

    for url in urls:
        print(f"Searching in {url}...")
        if debug:
            logging.debug(f"Processing URL: {url}")
        html = fetch_page(url, debug)
        if html:
            username = extract_username(html, debug)
            results = search_for_text(html, search_text, debug)
            days = None
            if results:
                for result in results:
                    days = extract_days(result, debug)
                    if days is not None:
                        break  # Only interested in the first occurrence

            if url in previous_data:
                stored_username = previous_data[url]['username']
                prev_days = previous_data[url].get('days_since_last_ban', -1)
                if days is not None and (prev_days == -1 or days < prev_days):
                    new_bans_detected = True
                    print(f"{Fore.RED}[{stored_username}]: New ban detected: {days} day(s) since last ban (previously {prev_days} day(s)){Style.RESET_ALL}")
                update_previous_data(previous_data, url, username, days, debug)
            else:
                if days is not None:
                    print(f"New data for {username} ({url}): {days} day(s) since last ban")
                else:
                    print(f"New data for {username} ({url}): No ban info")
                update_previous_data(previous_data, url, username, days, debug)
        else:
            print(f"Failed to fetch {url}")
        print("")

    # Save the updated data to the file
    save_current_data(data_file, previous_data, debug)

    print("Scanning has finished.")
    if debug:
        logging.debug("Finished scanning URLs")

    if not new_bans_detected:
        print("No new bans detected.")
        if debug:
            logging.debug("No new bans detected")
    else:
        print("New bans detected!")
        if debug:
            logging.debug("New bans detected")

def main(url_file, search_text, data_file, debug_flag):
    if debug_flag:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    check_new_bans(url_file, search_text, data_file, debug_flag)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for bans on players from a list of URLs.")
    parser.add_argument('--debug', '-d', action='store_true', help="Run in debug mode with detailed output")
    args = parser.parse_args()

    url_file = r"Cheater Checker\urls.json"  # Path to your JSON file with URLs
    search_text = "day(s) since last ban"
    data_file = r"Cheater Checker\data.json"  # Path to your JSON file for storing previous data

    main(url_file, search_text, data_file, args.debug)
