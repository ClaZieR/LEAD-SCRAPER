# Google Maps Business Scraper

This Python script automates the process of scraping business names and website availability from Google Maps for a specified location. It uses Selenium WebDriver to navigate Google Maps, search for businesses, and extract details.

## Features

- Searches for businesses in a specified location (default: Kaduwela)
- Scrapes the first 10 business listings from the search results
- Checks for the presence of a website and prints "Yes" or "No" based on availability
- Outputs the business name and website status to the console

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.8 or later
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Required Python libraries: selenium

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/google-maps-business-scraper.git
cd google-maps-business-scraper
```

2. Install the required Python libraries:
```bash
pip install selenium
```

3. Download and install ChromeDriver and add it to your system's PATH.

## Usage

1. Update the `Service` path in the script to point to your ChromeDriver location:
```python
service = Service(r"C:\Path\To\chromedriver.exe")
```

2. Run the script:
```bash
python scraper.py
```

3. The script will:
   - Open Google Maps in a Chrome browser
   - Search for "Businesses in Kaduwela"
   - Scrape the first 10 business listings for names and website availability
   - Print the results to the console

## Example Output
```
1. Business Name: ABC Cafe
   Website: Yes

2. Business Name: XYZ Mart
   Website: No
```

## Notes
- Ensure a stable internet connection as the script requires real-time interaction with Google Maps
- Modify the location or search term in the `search_businesses` function as needed

## Troubleshooting

- If the browser closes unexpectedly:
  - Check if your ChromeDriver version matches your Chrome browser version
  - Ensure all required dependencies are installed
- If no results are found:
  - Verify the Google Maps layout and element class names
  - Google Maps UI updates may require changes to the script

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This script is for educational and research purposes only. Scraping Google Maps may violate their terms of service. Use responsibly.