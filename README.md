# Cheater Checker

Cheater Checker is a Python script to monitor and detect bans on players from a list of URLs. It fetches web pages, extracts relevant information using BeautifulSoup, and checks for ban statuses based on specified text.

## Features

- **Web Scraping**: Fetches HTML content from specified URLs using `requests`.
- **HTML Parsing**: Uses `beautifulsoup4` to parse HTML and extract relevant information.
- **Ban Detection**: Searches for specified ban-related text to detect bans on players.
- **Data Persistence**: Stores previous ban data in a JSON file (`data.json`) for comparison and tracking.

## Requirements

- Python 3.6+
- Install dependencies using:

```sh
  pip install -r requirements.txt
```

## Usage

### Setup

    Clone the repository:

```sh
    git clone https://github.com/your_username/cheater-checker.git
    cd cheater-checker
```

### Install dependencies:

```sh
    pip install -r requirements.txt
```

    Prepare URLs and configuration:
        Edit urls.json to include the URLs you want to monitor. (Not these examples provided are for example only, not confirmed cheaters and are included only because of hackusations.)
        Customize data.json for initial or previous ban data storage.

### Running the Script

To run the script, use the following command:

```sh
python cheater_checker.py
```

## Options

Debug Mode: Use -d or --debug to run with detailed debug output:

```sh
python cheater_checker.py --debug
```

## Example

Here's an example of how to use the script:

    Prepare urls.json with URLs to monitor.
    Run cheater_checker.py to scan and check for new bans.
    View output in the console and monitor data.json for updated ban information.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.
License

This project is licensed under the MIT License - see the LICENSE file for details.
