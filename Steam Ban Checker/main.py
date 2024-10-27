import json
import re
import requests
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Style, init

init()

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def search_for_text(html, text):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(string=lambda s: text in s)

def extract_username(html):
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='actual_persona_name')
    return span.text if span else None

def extract_days(text):
    match = re.search(r'(\d+) day\(s\) since last ban', text)
    return int(match.group(1)) if match else None

def get_urls_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['urls']

def add_url_to_json(file_path, new_url):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['urls'].append(new_url)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def load_previous_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

def save_current_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def check_new_bans(urls, search_text, data_file, debug):
    previous_data = load_previous_data(data_file)
    new_bans_detected = False

    for url in urls:
        if debug:
            print(f"Searching in {url}...")
        html = fetch_page(url)
        if html:
            username = extract_username(html)
            results = search_for_text(html, search_text)
            days = None
            if results:
                for result in results:
                    days = extract_days(result)
                    if days is not None:
                        break  # Only interested in the first occurrence

            if url in previous_data:
                stored_username = previous_data[url]['username']
                prev_days = previous_data[url].get('days_since_last_ban', -1)
                if days is not None and days < prev_days:
                    new_bans_detected = True
                    print(f"{Fore.RED}[{stored_username}]: New ban detected: {days} day(s) since last ban (previously {prev_days} day(s)){Style.RESET_ALL}")
            else:
                print(f"New data for {username} ({url}): {days if days is not None else 'No ban info'} day(s) since last ban")

            previous_data[url] = {
                'username': username,
                'days_since_last_ban': days if days is not None else -1
            }
        else:
            print(f"Failed to fetch {url}")

    save_current_data(data_file, previous_data)

    if debug:
        print("Scanning has finished.")
    
    if not new_bans_detected:
        print("No new bans detected.")

def main(url_file, search_text, data_file, debug_flag, new_url):
    if new_url:
        add_url_to_json(url_file, new_url)
        check_new_bans([new_url], search_text, data_file, debug_flag)
    else:
        urls = get_urls_from_json(url_file)
        check_new_bans(urls, search_text, data_file, debug_flag)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for bans on Steam players from a list of URLs.")
    parser.add_argument('--debug', '-d', action='store_true', help="Run with detailed debug output")
    parser.add_argument('--add-url', '-a', type=str, help="Add a new URL to urls.json and scan it immediately")
    args = parser.parse_args()

    url_file = r"Steam Ban Checker\urls.json"  # Path to your JSON file with URLs
    search_text = "day(s) since last ban"
    data_file = r"Steam Ban Checker\data.json"  # Path to your JSON file for storing previous data

    main(url_file, search_text, data_file, args.debug, args.add_url)
