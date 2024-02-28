import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By

downloaded_site_path = 'C:\\Websites\\Main_Trial_1'
images_save_dir = 'C:\\Images\\Individual'

# Ensure the directories exist
os.makedirs(images_save_dir, exist_ok=True)

def init_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def capture_element_screenshot(driver, element, save_path):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    element.screenshot(save_path)
    driver.set_window_size(original_size['width'], original_size['height'])


def process_html_files(driver, base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                driver.get('file://' + file_path)
                time.sleep(2)  # Allow time for page to load

                images = driver.find_elements(By.TAG_NAME, 'img')
                for index, image in enumerate(images):
                    driver.execute_script("arguments[0].scrollIntoView(true);", image)
                    time.sleep(1)  # Adjust timing as necessary
                    
                    image_save_path = os.path.join(images_save_dir, f'{os.path.splitext(file)[0]}_image_{index}.png')
                    capture_element_screenshot(driver, image, image_save_path)

                    print(f'Image screenshot saved: {image_save_path}')
                    
                    scroll_height = image.size['height']
                    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
                    time.sleep(1)

def main():
    driver = init_webdriver()
    try:
        process_html_files(driver, downloaded_site_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
