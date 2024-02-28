from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time
from bs4 import BeautifulSoup

downloaded_site_path = 'C:\\Websites\\Main_Trial_1'
screenshots_save_dir = 'C:\\Images\\Complete'
html_save_dir = 'C:\\Images\\HTML'  
js_save_dir = 'C:\\Images\\JS' 

os.makedirs(screenshots_save_dir, exist_ok=True)
os.makedirs(html_save_dir, exist_ok=True)

def init_webdriver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extract_js_and_save(html_content, save_file_path):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')
    
    js_content = '\n'.join(tag.text for tag in script_tags if tag.text.strip() != '')
    if js_content:  # Save only if there's some JS content
        with open(save_file_path, 'w', encoding='utf-8') as file:
            file.write(js_content)
        print(f'JavaScript extracted and saved: {save_file_path}')
    else:
        print(f'No JavaScript found in {save_file_path}')


def capture_full_page_screenshot(driver, save_file_path):
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(width, height)
    time.sleep(2)
    driver.save_screenshot(save_file_path)

def save_html_source(driver, save_file_path):
    html_source = driver.page_source
    with open(save_file_path, 'w', encoding='utf-8') as file:
        file.write(html_source)

def process_html_files(driver, base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                url = 'file://' + os.path.abspath(file_path)
                driver.get(url)
                time.sleep(2)

                screenshot_save_path = os.path.join(screenshots_save_dir, f'{os.path.splitext(file)[0]}.png')
                html_save_path = os.path.join(html_save_dir, f'{os.path.splitext(file)[0]}.txt') 
                js_save_path = os.path.join(js_save_dir, f'{os.path.splitext(file)[0]}.txt') 

                capture_full_page_screenshot(driver, screenshot_save_path)
                save_html_source(driver, html_save_path)
                
                # Read the saved HTML file content
                with open(html_save_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                
                # Now pass the actual HTML content to extract_js_and_save
                extract_js_and_save(html_content, js_save_path)
                
                print(f'Full page screenshot saved: {screenshot_save_path}')
                print(f'HTML source saved: {html_save_path}')


def main():
    driver = init_webdriver()
    try:
        process_html_files(driver, downloaded_site_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
