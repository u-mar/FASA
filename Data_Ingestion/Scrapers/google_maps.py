from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time
import json




def scrape_google_maps(company,last): 
    try:
        chrome_options = Options()
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--headless=new')  # Or just '--headless' for older versions
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--remote-debugging-port=9222')
        

        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        print("🌍 Loading Google Maps...")
        driver.get('https://www.google.com/maps?hl=en')
        

        print(f"🔍 Searching for {company}...")
        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'searchboxinput'))
        )
        search_box.clear()
        search_box.send_keys(company)
        search_box.send_keys(Keys.RETURN)
        
        print("⏳ Waiting for business page...")
        time.sleep(5)
        
        print("📝 Opening reviews section...")
        reviews_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Reviews")]'))
        )
        reviews_button.click()
        time.sleep(5)

        review_element = driver.find_elements(By.CSS_SELECTOR, '.fontBodySmall[jslog]')[1]
        review_text = review_element.text
        total_reviews = int(review_text.split()[0])
        print(f"Total Review {total_reviews}")
        if total_reviews > last:
            new_total = total_reviews - last
            max_scroll_attempts = new_total // 10 + 1
            print("🔄 Sorting by newest reviews...")

            try:
                sort_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Sort reviews"]'))
                )
                sort_button.click()
                time.sleep(2)
                
                newest_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'.fxNQSd[data-index="1"]')))
                newest_option.click()
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Could not sort by newest: {str(e)}")
        
            data = {
                'reviewer': [],
                'rating': [],
                'date': [],
                'text': [],
                'response': []
            }
            
            # Find the scrollable reviews panel
            scroll_panel = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'))
            )
            
            # Enhanced scrolling to ensure all reviews load
            SCROLL_PAUSE_TIME = 3
            last_review_count = 0
            same_count = 0
            
            for attempt in range(max_scroll_attempts):
                # Scroll down
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_panel)
                time.sleep(SCROLL_PAUSE_TIME)
                
                # Get current count of loaded reviews
                current_reviews = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
                current_count = len(current_reviews)
                
                print(f"⬇️ Scroll {attempt+1}/{max_scroll_attempts} - Reviews loaded: {current_count}")
                
                # Check if we've stopped loading new reviews
                if current_count == last_review_count:
                    same_count += 1
                    if same_count >= 3:  # Stop if no new reviews after 3 scrolls
                        print("📜 No new reviews loading - stopping scroll")
                        break
                else:
                    same_count = 0
                    last_review_count = current_count
                
            
            # Click all "More" buttons to expand review text
            more_buttons = driver.find_elements(By.XPATH, '//button[contains(., "More")]')
            print(f"🔍 Expanding {len(more_buttons)} reviews with 'More' buttons")
            for button in more_buttons:
                try:
                    button.click()
                    time.sleep(0.3)  # Shorter pause between clicks
                except:
                    continue
            
            # Final extraction after all scrolling and expanding
            review_cards = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
            print(f"✅ Final review count: {len(review_cards)}")
            
            for card in review_cards:
                try:
                    # Initialize default values for this card
                    card_data = {
                        'reviewer': "#N/A",
                        'rating': "#N/A",
                        'date': "#N/A",
                        'text': "#N/A",
                        'response': "#N/A"
                    }
                    
                    # Extract reviewer name
                    try:
                        card_data['reviewer'] = card.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                    except NoSuchElementException:
                        pass
                    
                    # Extract rating
                    try:
                        rating_element = card.find_element(By.CSS_SELECTOR, 'span.kvMYJc')
                        card_data['rating'] = rating_element.get_attribute('aria-label').split()[0]
                    except NoSuchElementException:
                        pass
                    
                    # Extract date (should now be newest first)
                    try:
                        card_data['date'] = card.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
                    except NoSuchElementException:
                        pass
                    
                    # Extract review text (check both possible locations)
                    try:
                        card_data['text'] = card.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                    except NoSuchElementException:
                        try:
                            card_data['text'] = card.find_element(By.CSS_SELECTOR, 'span.MyEned').text
                        except NoSuchElementException:
                            pass
                    
                    # Extract owner response if exists
                    try:
                        card_data['response'] = card.find_element(By.CSS_SELECTOR, 'div.CDe7pd').text
                    except NoSuchElementException:
                        pass
                    
                    # Append all data for this card
                    for key in data:
                        data[key].append(card_data[key])    
                except Exception as e:
                    print(f"⚠️ Error processing card: {str(e)}")
                    continue
            df = pd.DataFrame(data)

            return df,total_reviews
        else:
            print(f"No New Reviews")
            print("Aborting .....")

            return None,last
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return None,last

    finally:
        driver.quit()

if __name__ == "__main__":
    company = "Uber office"
    a,c= scrape_google_maps(company,2000)
    print(a,c)
