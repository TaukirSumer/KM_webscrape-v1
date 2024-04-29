dbutils.library.restartPython()

%pip install selenium

pip install openpyxl

from datetime import datetime
import dateutil.relativedelta
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request, json 


with urllib.request.urlopen("https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json") as url:
    data = json.load(url)
    print(data['channels']['Stable']['version'])
    url = data['channels']['Stable']['downloads']['chromedriver'][0]['url']
    print(url)
    
    # set the url as environment variable to use in scripting 
    os.environ['url']= url


%sh
# Force download without caching
wget --no-cache -N $url -O /tmp/chromedriver_linux64.zip

# Unzip the downloaded file
unzip -o /tmp/chromedriver_linux64.zip -d /tmp/chromedriver/


#wget -N $url  -O /tmp/chromedriver_linux64.zip

#unzip /tmp/chromedriver_linux64.zip -d /tmp/chromedriver/


%sh
sudo rm -r /var/lib/apt/lists/* 
sudo apt clean && 
   sudo apt update --fix-missing -y


%sh
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable



def init_chrome_browser(download_path, chrome_driver_path,  url):
     
    options = Options()
    prefs = {'download.default_directory' : download_path, 'profile.default_content_setting_values.automatic_downloads': 1, "download.prompt_for_download": False,
  "download.directory_upgrade": True,   "safebrowsing.enabled": True ,
  "translate_whitelists": {"vi":"en"},
  "translate":{"enabled":"true"}}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')    # wont work without this feature in databricks can't display browser
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('window-size=2560,1440')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--lang=en')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    print(f"{datetime.now()}    Launching Chrome...")
    browser = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    print(f"{datetime.now()}    Chrome launched.")
    browser.get(url)
    print(f"{datetime.now()}    Browser ready to use.")
    return browser


driver = init_chrome_browser(
    download_path="/tmp/downloads",
    chrome_driver_path="/tmp/chromedriver/chromedriver-linux64/chromedriver",
    url= "https://www.google.com"
)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


driver.get("https://www.msamb.com/ApmcDetail/APMCPriceInformation#DistrictCommodityGird")
driver.maximize_window()
time.sleep(5)

expected_title = "Your Expected Title"  # Update this with the expected title of the webpage
actual_title = driver.title

element = driver.find_element(By.ID,"APMCTitle")
element.click()
time.sleep(3)

element = driver.find_element(By.ID, "APMCTitle")
print("Text content of the element:", element.text)

element1 = driver.find_element(By.XPATH,"//a[@title='District Commodity Wise']")
element1.click()
time.sleep(3)

dropdown_element=driver.find_element(By.NAME,'drpDistrictCommodity')
dropdown_select = Select(dropdown_element)
time.sleep(5)
print("End")
dropdown_select.select_by_visible_text('WARDHA')
time.sleep(15)

tbody = driver.find_element(By.XPATH,'//*[@id="tblDistrictCommodityGird"]')

listt=[]

for tr in tbody.find_elements(By.XPATH,'//tr'):
    rows =[item.text for item in tr.find_elements(By.XPATH,'.//td')]
    listt.append(rows)

headers = ["Commodity", "Variety", "Unit", "Quantity", "Low Rate", "High Rate", "Modal"]

df = pd.DataFrame(listt, columns=headers)

df.to_excel("output.xlsx", index=False)

driver.quit()
display(df)



df.sample(15)