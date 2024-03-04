from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time
from bs4 import BeautifulSoup


screenshots_save_dir = 'C:\\Images\\Complete'
html_save_dir = 'C:\\Images\\HTML'  
js_save_dir = 'C:\\Images\\JS' 
html_file_list_path = 'C:\\Users\\HP\\OneDrive\\Desktop\\Tensoic\\httrack\\html.txt'  


os.makedirs(screenshots_save_dir, exist_ok=True)
os.makedirs(html_save_dir, exist_ok=True)
os.makedirs(js_save_dir, exist_ok=True)

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
    if js_content:
        with open(save_file_path, 'w', encoding='utf-8') as file:
            file.write(js_content)
        print(f'JavaScript extracted and saved: {save_file_path}')
    else:
        print(f'No JavaScript found in {save_file_path}')

def capture_full_page_screenshot(driver, save_file_path):
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    driver.set_window_size(1920, 1080)  # Set initial window size
    driver.execute_script("window.scrollTo(0, 0)")  # Scroll to the top of the page
    time.sleep(2)  # Wait for any lazy-loaded content
    
    scrolled_height = 0
    while scrolled_height < total_height:
        driver.execute_script(f"window.scrollTo(0, {scrolled_height + 1080});")
        time.sleep(1)  # Adjust time as needed to ensure content loads
        scrolled_height += 1080
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > total_height:
            total_height = new_height
    
    driver.set_window_size(1920, total_height)  # Resize window to full page height
    time.sleep(2)  # Wait for resize
    driver.save_screenshot(save_file_path)

def save_html_source(driver, save_file_path):
    html_source = driver.page_source
    with open(save_file_path, 'w', encoding='utf-8') as file:
        file.write(html_source)

def read_html_file_paths(file_list_path):
    with open(file_list_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def process_html_files(driver, html_file_paths):
    for file_path in html_file_paths:
        if file_path.endswith('.html'):
            url = 'file://' + os.path.abspath(file_path)
            driver.get(url)
            time.sleep(2)

            file_name = os.path.basename(file_path)
            screenshot_save_path = os.path.join(screenshots_save_dir, f'{os.path.splitext(file_name)[0]}.png')
            html_save_path = os.path.join(html_save_dir, f'{os.path.splitext(file_name)[0]}.txt') 
            js_save_path = os.path.join(js_save_dir, f'{os.path.splitext(file_name)[0]}.txt') 

            capture_full_page_screenshot(driver, screenshot_save_path)
            save_html_source(driver, html_save_path)
            
            with open(html_save_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            extract_js_and_save(html_content, js_save_path)
            
            print(f'Full page screenshot saved: {screenshot_save_path}')
            print(f'HTML source saved: {html_save_path}')

def main():
    html_file_paths = read_html_file_paths(html_file_list_path)
    driver = init_webdriver()
    try:
        process_html_files(driver, html_file_paths)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
