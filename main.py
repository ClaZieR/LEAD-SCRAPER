import random
import time
import requests
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Expanded list of towns with more variety
towns = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", 
    "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX", "San Diego, CA",
    "Dallas, TX", "San Jose, CA", "Miami, FL", "Seattle, WA", 
    "Denver, CO", "Atlanta, GA", "Boston, MA", "Las Vegas, NV",
    "Portland, OR", "Charlotte, NC", "Detroit, MI", "Memphis, TN"
]

def setup_driver():
    chrome_options = Options()
    # Extensive options to improve detection and performance
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Experimental options
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(r"C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Additional anti-detection techniques
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    return driver

def validate_website(url):
    """Enhanced website validation with multiple checks"""
    if not url or len(url) < 5:
        return False
    
    try:
        # Multiple validation strategies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Try HEAD request first
        response = requests.head(url, timeout=5, allow_redirects=True, headers=headers)
        if 200 <= response.status_code < 400:
            return True
        
        # Fallback to GET request for more thorough check
        response = requests.get(url, timeout=5, allow_redirects=True, headers=headers)
        return 200 <= response.status_code < 400
    except requests.RequestException:
        # Try with additional prefix variations
        try:
            prefixes = ['http://', 'https://', 'www.']
            for prefix in prefixes:
                full_url = prefix + url.replace('http://', '').replace('https://', '').replace('www.', '')
                response = requests.head(full_url, timeout=5, allow_redirects=True, headers=headers)
                if 200 <= response.status_code < 400:
                    return True
        except:
            pass
    
    return False

def extract_business_details(driver):
    """Enhanced business details extraction with new website detection method"""
    business_details = {
        'name': 'Unknown',
        'website': 'No website',
        'website_status': 'N/A',
        'phone': 'Not available',
        'email': 'Not available',
        'address': 'Not available'
    }
    
    # New website detection method using the specific class
    try:
        website_container = driver.find_elements(By.CLASS_NAME, "rogA2c.ITvuef")
        if website_container:
            website_element = website_container[0].find_element(By.CLASS_NAME, "Io6YTe.fontBodyMedium.kR99db.fdkmkc")
            website = website_element.text.strip()
            
            # Ensure website is not empty and add protocol if missing
            if website:
                # Validate and standardize website
                if not website.startswith(('http://', 'https://', 'www.')):
                    website = f"https://{website}"
                
                # Validate website
                if validate_website(website):
                    business_details['website'] = website
                    business_details['website_status'] = 'Working'
    except:
        # Fallback to previous website detection methods
        # ... [rest of the previous website detection code remains the same]
        pass
    
    # Phone and email extraction (same as before)
    try:
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        
        # Phone number regex with multiple formats
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+1\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, page_text)
            if phones:
                business_details['phone'] = phones[0]
                break
        
        # Email extraction
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_text)
        if emails:
            business_details['email'] = emails[0]
    except:
        pass
    
    return business_details

def search_town_businesses(driver, town):
    """Enhanced business search with multiple query strategies"""
    driver.get("https://www.google.com/maps")
    
    search_queries = [
        f"Businesses in {town}",
        f"Local businesses near {town}",
        f"Small businesses in {town}",
        f"Business directory {town}"
    ]
    
    for query in search_queries:
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            
            # Check if results are found
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
                )
                break  # Exit if results found
            except TimeoutException:
                continue  # Try next query
        except Exception as e:
            print(f"Search error: {e}")
    
    time.sleep(3)

def scrape_businesses(driver):
    """Advanced business scraping with multiple detection methods"""
    businesses = []
    seen = set()
    
    try:
        # Multiple business listing selectors
        business_selectors = [
            (By.CLASS_NAME, "hfpxzc"),
            (By.XPATH, "//div[contains(@class, 'business') or contains(@role, 'article')]"),
            (By.CSS_SELECTOR, "a[href*='maps/place']")
        ]
        
        # Try each selector
        for selector_type, selector in business_selectors:
            try:
                results = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((selector_type, selector))
                )
                
                # Limit to first 30 results
                for result in results[:30]:
                    try:
                        # Click with retry mechanism
                        attempts = 0
                        while attempts < 3:
                            try:
                                result.click()
                                break
                            except StaleElementReferenceException:
                                attempts += 1
                                time.sleep(1)
                        
                        time.sleep(2)
                        
                        # Extract business details
                        business = extract_business_details(driver)
                        
                        # Get coordinates
                        try:
                            current_url = driver.current_url
                            if "@" in current_url:
                                coordinates = current_url.split("@")[1].split(",")[:2]
                                business['latitude'], business['longitude'] = coordinates
                            else:
                                business['latitude'], business['longitude'] = "Unknown", "Unknown"
                        except:
                            business['latitude'], business['longitude'] = "Unknown", "Unknown"
                        
                        # Avoid duplicates
                        identifier = (business['name'], business['latitude'], business['longitude'])
                        if identifier in seen:
                            continue
                        seen.add(identifier)
                        
                        # Filter for businesses without websites or with non-working websites
                        if business['website'] == 'No website' or business['website_status'] == 'Not working':
                            businesses.append(business)
                        
                    except Exception as e:
                        print(f"Error processing individual business: {e}")
                    
                    # Navigate back to results
                    try:
                        driver.back()
                        time.sleep(1)
                    except:
                        pass
                
                # Break if businesses found
                if businesses:
                    break
            
            except:
                continue
    
    except Exception as e:
        print(f"Overall business scraping error: {e}")
    
    return businesses

def save_to_csv(businesses, town):
    """Save businesses to CSV with comprehensive logging"""
    if not businesses:
        print("No businesses found to save.")
        return
    
    df = pd.DataFrame(businesses)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"businesses_{town.replace(', ', '_')}_{timestamp}.csv"
    
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data saved to {filename}")
    print(f"Total businesses found: {len(businesses)}")
    
    # Print details to console
    for business in businesses:
        print(f"Business: {business['name']}")
        print(f"Website: {business['website']}")
        print(f"Website Status: {business['website_status']}")
        print(f"Phone: {business['phone']}")
        print(f"Email: {business['email']}")
        print("---")

def main():
    driver = setup_driver()
    try:
        town = random.choice(towns)
        print(f"Searching businesses in: {town}")
        
        search_town_businesses(driver, town)
        businesses = scrape_businesses(driver)
        
        if businesses:
            save_to_csv(businesses, town)
        else:
            print("No businesses without websites found.")
    
    except Exception as e:
        print(f"Main process error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()