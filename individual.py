import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

images_save_dir = 'C:\\Images\\Individual'
html_file_list_path = 'C:\\Users\\HP\\OneDrive\\Desktop\\Tensoic\\httrack\\html.txt'  

os.makedirs(images_save_dir, exist_ok=True)

def init_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def capture_element_screenshot(driver, element, save_path):
    # Check if element size is valid
    size = element.size
    if size['width'] == 0 or size['height'] == 0:
        print(f"Cannot capture screenshot, element size is 0 for {save_path}")
        return

    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    element.screenshot(save_path)
    driver.set_window_size(original_size['width'], original_size['height'])


def read_html_file_paths(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def process_html_files(driver, html_file_paths):
    for file_path in html_file_paths:
        driver.get('file://' + file_path)
        time.sleep(2)  

        images = driver.find_elements(By.TAG_NAME, 'img')
        for index, image in enumerate(images):
            driver.execute_script("arguments[0].scrollIntoView(true);", image)
            time.sleep(1)  
            
            file_name = os.path.basename(file_path)
            image_save_path = os.path.join(images_save_dir, f'{os.path.splitext(file_name)[0]}_image_{index}.png')
            capture_element_screenshot(driver, image, image_save_path)

            print(f'Image screenshot saved: {image_save_path}')
            
            scroll_height = image.size['height']
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(1)

def main():
    html_file_paths = read_html_file_paths(html_file_list_path)
    driver = init_webdriver()
    try:
        process_html_files(driver, html_file_paths)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
