from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
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

def search_businesses(driver):
    driver.get("https://www.google.com/maps")
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_box.send_keys("Businesses in Kaduwela")
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)  # Wait for search results to load
    except TimeoutException:
        print("Timeout waiting for search box to load")
        return False
    return True

def check_for_website(driver):
    try:
        # Check for website button/link
        website_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-item-id='authority'], button[data-item-id='authority']"))
        )
        return "Yes" if website_elements else "No"
    except:
        return "No"

def get_unique_businesses(driver, max_businesses=10):
    visited_businesses = set()
    business_details = []
    
    try:
        # Wait for the business listings panel
        listings_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.DxyBCb"))
        )
        
        while len(business_details) < max_businesses:
            # Find all business entries in the current view
            business_entries = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Nv2PK"))
            )
            
            for entry in business_entries:
                try:
                    # Check if we've reached our target
                    if len(business_details) >= max_businesses:
                        break
                        
                    # Get the business name before clicking
                    name_element = entry.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall")
                    business_name = name_element.text.strip()
                    
                    if business_name in visited_businesses:
                        continue
                        
                    # Click on the business entry
                    entry.click()
                    time.sleep(3)
                    
                    # Check for website
                    website_status = check_for_website(driver)
                    
                    # Store the business details
                    business_details.append({
                        "name": business_name,
                        "website": website_status
                    })
                    visited_businesses.add(business_name)
                    
                    print(f"Processed: {business_name} - Website: {website_status}")
                    
                    # Click back to the listing
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
            
            # If we haven't found enough businesses, scroll and continue
            if len(business_details) < max_businesses:
                # Scroll within the panel
                driver.execute_script(
                    "arguments[0].scrollTop += 300;", listings_panel
                )
                time.sleep(2)
                
    except Exception as e:
        print(f"Error in main business processing loop: {str(e)}")
    
    return business_details

def main():
    driver = setup_driver()
    try:
        if search_businesses(driver):
            print("Starting to process businesses...")
            businesses = get_unique_businesses(driver)
            print("\nFinal Results:")
            for i, business in enumerate(businesses, 1):
                print(f"{i}. Business Name: {business['name']}")
                print(f"   Website: {business['website']}\n")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()