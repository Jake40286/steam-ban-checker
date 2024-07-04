# Steam Ban Checker

Steam Ban Checker is a Python script to monitor and detect bans on Steam players from a list of URLs. It fetches web pages, extracts relevant information using BeautifulSoup, and checks for ban statuses based on specified text.

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
git clone https://github.com/your_username/steam-ban-checker.git
cd steam-ban-checker
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Prepare URLs and configuration:
- Edit `urls.json` to include the URLs you want to monitor.
- Customize `data.json` for initial or previous ban data storage.

### Running the Script

To run the script, use the following command:

```sh
python steam_ban_checker.py
```

## Options

- **Debug Mode**: Use `-d` or `--debug` to run with detailed debug output:

  ```sh
  python steam_ban_checker.py --debug
  ```

## Example

Here's an example of how to use the script:

1. Prepare `urls.json` with URLs to monitor.
2. Run `steam_ban_checker.py` to scan and check for new bans.
3. View output in the console and monitor `data.json` for updated ban information.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Directory Structure

Ensure that your directory structure reflects the new names:

```
steam-ban-checker/
├── urls.json
├── data.json
├── steam_ban_checker.py
└── requirements.txt
```
