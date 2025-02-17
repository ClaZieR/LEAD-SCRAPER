# Google Maps Business Contact Scraper

This Python script automates the process of scraping business contact information from Google Maps, focusing on businesses with no website or non-working websites. The script collects business names, phone numbers, emails, website status, and Google Maps URLs.

## Features

- Searches for businesses in a specified location (default: Superior, Colorado)
- Scrapes detailed contact information including:
  - Business name
  - Phone number
  - Email address (when available)
  - Website status (No Website/Working/Not Working)
  - Website URL (if exists)
  - Google Maps URL
- Automatically checks website status using HTTP requests
- Filters businesses to only include those with no website or non-working websites
- Exports data to Excel (.xlsx) or CSV format
- Includes progress tracking and error handling

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.8 or later
- Google Chrome
- ChromeDriver (compatible with your Chrome version)

Required Python libraries:
- selenium
- requests
- pandas
- openpyxl (for Excel export)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/google-maps-contact-scraper.git
cd google-maps-contact-scraper
```

2. Install the required Python libraries:
```bash
pip install selenium requests pandas openpyxl
```

3. Download and install ChromeDriver and add it to your system's PATH.

## Usage

1. Update the ChromeDriver path in the script:
```python
service = Service(r"C:\Path\To\chromedriver.exe")
```

2. (Optional) Modify the search location in the script:
```python
search_businesses(driver, location="Your Location Here")
```

3. Run the script:
```bash
python scraper.py
```

## Output

The script generates an Excel file (`business_report.xlsx`) with the following columns:
- Business Name
- Phone Number
- Email
- Website Status
- Website URL
- Google Maps URL

Example of console output during execution:
```
Processing business 1: Sample Business
Added to list: Sample Business - Website Status: No Website
Progress: 1/10 businesses found
...
```

## Configuration Options

You can modify the following parameters in the script:
- `max_businesses`: Number of businesses to collect (default: 10)
- `location`: Target area for business search
- Export filename and format

## Error Handling

The script includes comprehensive error handling for:
- Network connectivity issues
- Website availability checking
- Stale elements in Google Maps
- Missing or invalid data
- Excel export failures (with CSV fallback)

## Limitations

- Rate limiting may apply when checking website status
- Email extraction depends on website accessibility
- Google Maps UI changes may require script updates
- Website status checks may take additional time

## Troubleshooting

- If the browser closes unexpectedly:
  - Verify ChromeDriver version matches Chrome browser version
  - Check system resources and internet connection
- If data export fails:
  - Ensure you have write permissions in the script directory
  - Check if the output file is not open in another program

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This script is for educational and research purposes only. Usage should comply with Google Maps' terms of service and website owners' policies. Always respect robots.txt and rate limiting when checking websites.