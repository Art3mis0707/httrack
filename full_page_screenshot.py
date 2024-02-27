import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By


downloaded_site_path = 'C:\\Users\\HP\\OneDrive\\Desktop\\Tensoic\\httrack'
images_save_dir = 'C:\\Images'

os.makedirs(images_save_dir, exist_ok=True)

def init_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scroll_and_capture_full_page(driver, save_path):
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    overlap_correction = 100  # Pixels to overlap between screenshots to prevent content repetition
    screenshots = []
    
    current_height = 0
    while current_height < total_height:
        driver.execute_script(f"window.scrollTo(0, {current_height})")
        time.sleep(0.5)  # Adjust timing as necessary
        screenshot = driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshots.append(screenshot)
        current_height += viewport_height - overlap_correction
        if current_height + viewport_height > total_height:
            current_height = total_height - viewport_height  # Adjust to end at the bottom
            driver.execute_script(f"window.scrollTo(0, {current_height})")
            time.sleep(0.5)  # Adjust timing as necessary
            screenshot = driver.get_screenshot_as_png()
            screenshot = Image.open(BytesIO(screenshot))
            screenshots.append(screenshot)
            break

    # Stitch screenshots with adjustment for overlap
    final_image = stitch_screenshots_with_overlap(screenshots, overlap_correction)
    final_image.save(save_path)

def stitch_screenshots_with_overlap(screenshots, overlap):
    total_width = screenshots[0].size[0]
    total_height = sum(img.size[1] for img in screenshots) - overlap * (len(screenshots) - 1)
    stitched_image = Image.new('RGB', (total_width, total_height))
    y_offset = 0
    for img in screenshots:
        stitched_image.paste(img, (0, y_offset))
        y_offset += img.size[1] - overlap  # Decrement overlap for next image
    return stitched_image


def process_html_files(driver, base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                driver.get('file://' + file_path)
                time.sleep(2)  # Adjust timing as necessary
                
                # Full page screenshot with scrolling and stitching
                full_page_screenshot_path = os.path.join(images_save_dir, f'{os.path.splitext(file)[0]}_full_page.png')
                scroll_and_capture_full_page(driver, full_page_screenshot_path)
                print(f'Full page screenshot saved: {full_page_screenshot_path}')
                return full_page_screenshot_path

def main():
    driver = init_webdriver()
    try:
       process_html_files(driver, downloaded_site_path)
       
    finally:
        driver.quit()

if __name__ == "__main__":
    main()