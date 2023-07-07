from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(executable_path="/usr/bin/chromedriver")

#driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
#driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
#driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome()

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://python.org")
print(driver.title)
driver.close()