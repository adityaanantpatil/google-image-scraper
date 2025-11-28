from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
import requests
import hashlib
import os
import io
import time
from PIL import Image

# Define the path to chrome driver
DRIVER_PATH = r'C:\Users\adi12\Desktop\chromedriver-win64\chromedriver.exe'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')

# Initialize the webdriver with Service
service = Service(DRIVER_PATH)
wd = webdriver.Chrome(service=service, options=chrome_options)

# Base folder for downloads
folder = r"C:\Users\adi12\Desktop\speedsign"

# Create the scraper class
class GoogleScraper():
    '''Downloads images from google based on the query.
       webdriver - Selenium webdriver
       max_num_of_images - Maximum number of images that we want to download
    '''
    def __init__(self, webdriver: webdriver.Chrome, max_num_of_images: int):
        self.wd = webdriver
        self.max_num_of_images = max_num_of_images

    def _scroll_page(self, target_images):
        """Scroll down the page to load more images"""
        last_height = self.wd.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down multiple times
            for _ in range(3):
                self.wd.execute_script("window.scrollBy(0, 1000);")
                time.sleep(0.3)
            
            # Try to click "Show more results" button if it appears
            try:
                show_more = self.wd.find_element(By.CSS_SELECTOR, ".mye4qd")
                self.wd.execute_script("arguments[0].click();", show_more)
                print("Clicked 'Show more results' button...")
                time.sleep(2)
            except NoSuchElementException:
                pass
            except Exception:
                pass
            
            # Check how many images we have now
            try:
                image_elements = self.wd.find_elements(By.CSS_SELECTOR, "div[jsname='dTDiAc']")
                if not image_elements:
                    image_elements = self.wd.find_elements(By.CSS_SELECTOR, "div.isv-r")
                
                print(f"Currently loaded {len(image_elements)} images (target: {target_images})...")
                
                # If we have enough images, break
                if len(image_elements) >= target_images:
                    break
                    
            except Exception:
                pass
            
            # Check if we've reached the bottom
            new_height = self.wd.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Try scrolling one more time to be sure
                time.sleep(1)
                new_height = self.wd.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("Reached the end of the page.")
                    break
            last_height = new_height

    def _build_query(self, query: str):
        return f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"

    def _get_info(self, query: str):
        image_urls = []  # Changed from set to list to maintain order

        self.wd.get(self._build_query(query))
        time.sleep(2)
        
        # Scroll to load more images - pass target number
        print(f"Scrolling to load at least {self.max_num_of_images} images...")
        self._scroll_page(self.max_num_of_images)

        # Find all image elements - try different selectors
        print("Searching for images...")
        
        # Try to find clickable image containers
        try:
            # This selector targets the actual clickable div elements
            image_elements = self.wd.find_elements(By.CSS_SELECTOR, "div[jsname='dTDiAc']")
            
            if not image_elements:
                image_elements = self.wd.find_elements(By.CSS_SELECTOR, "div.isv-r")
            
            if not image_elements:
                # Fallback: try to get all images directly
                image_elements = self.wd.find_elements(By.TAG_NAME, "img")
                
        except Exception as e:
            print(f"ERROR: Could not find images - {e}")
            return image_urls

        print(f"Found {len(image_elements)} image elements...")
        print(f"Extracting image URLs...")

        # Try to extract URLs directly from thumbnails first
        thumbnails = self.wd.find_elements(By.CSS_SELECTOR, "img.rg_i, img.Q4LuWd, img")
        
        for thumb in thumbnails[:self.max_num_of_images]:
            if len(image_urls) >= self.max_num_of_images:
                break
                
            try:
                src = thumb.get_attribute('src')
                data_src = thumb.get_attribute('data-src')
                
                # Prefer data-src over src
                url = data_src if data_src else src
                
                if url and url.startswith('http') and 'gstatic' not in url:
                    image_urls.append(url)  # Changed from add to append
                    
            except Exception as e:
                continue

        # Now try clicking method for higher resolution images
        count = len(image_urls)
        for i, element in enumerate(image_elements[:self.max_num_of_images]):
            if count >= self.max_num_of_images:
                break
                
            try:
                # Scroll element into view
                self.wd.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.2)
                
                # Click the element
                element.click()
                time.sleep(0.3)
                
                # Try to find the large image in the preview panel
                try:
                    # Look for images in the preview area
                    large_images = self.wd.find_elements(By.CSS_SELECTOR, "img.sFlh5c.pT0Scc.iPVvYb, img.n3VNCb, img.iPVvYb")
                    
                    for img in large_images:
                        src = img.get_attribute('src')
                        if src and src.startswith('http') and 'gstatic' not in src:
                            image_urls.append(src)  # Changed from add to append
                            count += 1
                            if count % 10 == 0:  # Print every 10 images
                                print(f"Extracted image {count}/{self.max_num_of_images}")
                            break
                            
                except Exception as e:
                    pass
                    
            except ElementClickInterceptedException:
                # Try JavaScript click
                try:
                    self.wd.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
                except:
                    continue
            except Exception as e:
                continue

        # Only keep the first max_num_of_images
        image_urls = image_urls[:self.max_num_of_images]
        
        print(f"Collected {len(image_urls)} image URLs (first {len(image_urls)} in order)")
        return image_urls

    def download_image(self, folder_path: str, url: str, index: int):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }
            image_content = requests.get(url, headers=headers, timeout=15).content

        except Exception as e:
            print(f"ERROR: Could not download {url} - {e}")
            return

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            
            # Use index-based naming to maintain order
            file_name = f"image_{index:04d}.jpg"  # Changed to 4 digits for up to 9999 images
            file_path = os.path.join(folder_path, file_name)

            # Check if file already exists
            if os.path.exists(file_path):
                print(f"SKIP: {file_name} already exists")
                return

            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS: saved as {file_name}")

        except Exception as e:
            print(f"ERROR: Could not save {url} - {e}")

    def scrape_images(self, query: str, folder_path='path'):
        folder = os.path.join(folder_path, '_'.join(query.lower().split(' ')))
        
        if not os.path.exists(folder):
            os.makedirs(folder)

        image_info = self._get_info(query)
        print(f"\nDownloading {len(image_info)} images...")

        for i, image_url in enumerate(image_info, 1):
            print(f"[{i}/{len(image_info)}] ", end="")
            self.download_image(folder, image_url, i)

        print(f"\nDownload complete! Images saved to: {folder}")

# Run scrape command
try:
    gs = GoogleScraper(wd, 1000)
    gs.scrape_images('speed sign 10', folder)
finally:
    # Close the browser
    print("\nClosing browser...")
    wd.quit()