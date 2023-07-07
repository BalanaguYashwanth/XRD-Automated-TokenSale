import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_info(hash):
    info = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    
    user_data_dir = '/home/ubuntu/chrome-profile'
    log_dir = '/home/ubuntu/chrome-logs/file.log' 
    
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument(f'--enable-logging --v=1 --log-file={log_dir}')
    options.add_argument('--disable-dev-shm-usage')

    #options.add_argument('start-maximized')
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_experimental_option('useAutomationExtension', False)
    
    #chrome_path = '/usr/bin/google-chrome-stable'
    #options.binary_location = chrome_path


    service = Service(executable_path="/usr/local/bin/chromedriver")
    
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    driver = webdriver.Chrome(service=service, options=options)
    url = f'https://www.radixscan.io/search/{hash}'
    driver.get(url)
    time.sleep(5)

    table = driver.find_element(By.ID, 'datatable1')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:

        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            try:
                link_element = cell.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')
                if 'address' in link:
                    info.append(link[33:])
                elif "token" in link:
                    info.append(link[31:])
            except:
                values = cell.text
                info.append(values)
    element = driver.find_element(By.ID, 'Message')
    text = element.text
    info.append(text)
    #driver.quit()
    # print(info)
    return info