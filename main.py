from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import requests
import pandas as pd
import re
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(r"C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def search_businesses(driver, location="Businesses in Superior Colorado"):
    driver.get("https://www.google.com/maps")
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
    except TimeoutException:
        print("Timeout waiting for search box to load")
        return False
    return True

def check_website_status(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return "Working" if response.status_code == 200 else "Not Working"
    except:
        try:
            response = requests.head('http://' + url.replace('https://', ''), timeout=10, allow_redirects=True)
            return "Working" if response.status_code == 200 else "Not Working"
        except:
            return "Not Working"

def extract_contact_info(driver):
    contact_info = {
        'phone': None,
        'email': None,
        'website': None,
        'maps_url': driver.current_url
    }
    
    try:
        # Look for phone numbers
        phone_elements = driver.find_elements(By.CSS_SELECTOR, "button[data-tooltip='Copy phone number']")
        if phone_elements:
            contact_info['phone'] = phone_elements[0].get_attribute('aria-label').replace('Phone:', '').strip()

        # Look for website
        website_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-item-id='authority']")
        if website_elements:
            website_url = website_elements[0].get_attribute('href')
            contact_info['website'] = website_url
            
            # Try to find email on website
            try:
                website_response = requests.get(website_url, timeout=10)
                email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
                emails = re.findall(email_pattern, website_response.text)
                if emails:
                    contact_info['email'] = emails[0]
            except:
                pass

    except Exception as e:
        print(f"Error extracting contact info: {str(e)}")
    
    return contact_info

def get_filtered_businesses(driver, max_businesses=10):  # Changed to 10
    visited_businesses = set()
    business_details = []
    processed_count = 0  # Track total processed businesses
    
    try:
        listings_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.DxyBCb"))
        )
        
        while len(business_details) < max_businesses and processed_count < 30:  # Added limit to prevent infinite loop
            business_entries = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Nv2PK"))
            )
            
            for entry in business_entries:
                try:
                    if len(business_details) >= max_businesses:
                        break
                        
                    name_element = entry.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall")
                    business_name = name_element.text.strip()
                    
                    if business_name in visited_businesses:
                        continue
                    
                    processed_count += 1
                    print(f"Processing business {processed_count}: {business_name}")
                        
                    entry.click()
                    time.sleep(3)
                    
                    contact_info = extract_contact_info(driver)
                    
                    # Check website status if website exists
                    website_status = "No Website"
                    if contact_info['website']:
                        website_status = check_website_status(contact_info['website'])
                    
                    # Only add businesses with no website or non-working websites
                    if website_status in ["No Website", "Not Working"]:
                        business_details.append({
                            "name": business_name,
                            "phone": contact_info['phone'],
                            "email": contact_info['email'],
                            "website_status": website_status,
                            "website_url": contact_info['website'],
                            "maps_url": contact_info['maps_url']
                        })
                        print(f"Added to list: {business_name} - Website Status: {website_status}")
                        print(f"Progress: {len(business_details)}/{max_businesses} businesses found")
                    
                    visited_businesses.add(business_name)
                    
                    back_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsaction='pane.back']"))
                    )
                    back_button.click()
                    time.sleep(2)
                    
                except StaleElementReferenceException:
                    print("Stale element, refreshing view...")
                    time.sleep(2)
                    continue
                except Exception as e:
                    print(f"Error processing business: {str(e)}")
                    continue
            
            if len(business_details) < max_businesses:
                driver.execute_script(
                    "arguments[0].scrollTop += 300;", listings_panel
                )
                time.sleep(2)
                
    except Exception as e:
        print(f"Error in main business processing loop: {str(e)}")
    
    return business_details

def export_to_excel(businesses, filename="business_report.xlsx"):
    try:
        df = pd.DataFrame(businesses)
        df = df[['name', 'phone', 'email', 'website_status', 'website_url', 'maps_url']]
        df.columns = ['Business Name', 'Phone Number', 'Email', 'Website Status', 'Website URL', 'Google Maps URL']
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Data exported to {filename}")
    except ImportError:
        # Fallback to CSV if openpyxl is not installed
        csv_filename = filename.replace('.xlsx', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"openpyxl not found. Data exported to {csv_filename} instead")

def main():
    driver = setup_driver()
    try:
        if search_businesses(driver):
            print("Starting to process businesses...")
            businesses = get_filtered_businesses(driver)  # Now defaults to 10 businesses
            if businesses:
                export_to_excel(businesses)
                print(f"\nFound {len(businesses)} businesses with no website or non-working websites")
            else:
                print("No matching businesses found")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()