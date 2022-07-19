from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time
import urllib.request
import os
import pandas as pd
from urllib.parse import quote_plus          
from bs4 import BeautifulSoup as bs 
from xvfbwrapper import Xvfb
import time
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import re
from selenium.webdriver.chrome.service import Service
import os 
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pdb
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import traceback         
def selenium_scroll_down(driver):
    SCROLL_PAUSE_SEC = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")
  
        if new_height == last_height:
            return 1
        last_height = new_height
        
    

def Fragrance_crawler(url_data, brand_url,brand_name):
    
    data = pd.DataFrame(columns = ['Brand', 'Fragrance','Url'])
    failed_fragrance_list = []
    failed_country_list = []
    index = 0
    print("-------------Start------------")
    for current, country_url in enumerate((url_data)):
        
        #try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        try:
            driver.set_window_size(1920, 1080)
            driver.get(country_url)
            
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]')))
            WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]')))
            brand_grid = driver.find_element(by = By.XPATH, value = '//*[@id="main-content"]/div[1]/div[1]/div[2]')
            num = len(brand_grid.find_elements(by = By.TAG_NAME, value = 'div'))  ## number of brands

            for i in tqdm((range(1, num+1))):
                try:

                    b_xpath_f = '//*[@id="main-content"]/div[1]/div[1]/div[2]/div['
                    b_xpath_b = ']/a'
                
                    xpath = b_xpath_f + str(i) + b_xpath_b 
                    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, xpath)))
                    brand = driver.find_element(by = By.XPATH, value = xpath)
                    brand_name = brand.get_attribute("textContent").strip('\n')
                    brand_url = brand.get_attribute('href')
                    
                    fr_name, fr_url, count = brand_driver(brand_url,brand_name)
                    print("\n"+brand_name +"|"+str(count)+"\n")

                    if fr_name != None:
                        brand_name_list = [brand_name] * count

                        br_data = pd.DataFrame({'Brand':brand_name_list,
                                        'Fragrance':fr_name,
                                        'Url':fr_url},index = range(index, index+count))
                        
                        index = index + count
                        data = data.append(br_data)
                    else:
                        failed_fragrance_list.append(brand_name)

                except NoSuchElementException:
                    continue
            data.to_csv('/home/dhkim/Fragrance/data/data.csv')
        except Exception as e:
            print(e)
            failed_country_list.append(country_url)
            continue

        driver.quit()


        #except Exception as e:
            #driver.quit()
            #traceback.print_exc()
            #Fragrance_crawler(url_data[current:], brand_url,brand_name)
            #return data, failed_country_list, failed_fragrance_list

    return data, failed_country_list, failed_fragrance_list


def brand_driver(brand_url,brand_name):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(1920, 1080)
 

    time.sleep(1)
    driver.get(brand_url)

    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="brands"]')))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="brands"]')))
        brand_grid = driver.find_element(by = By.XPATH, value = '//*[@id="brands"]')
        num = len(brand_grid.find_elements(by = By.TAG_NAME, value = 'div'))
        
        fr_xpath_f = '//*[@id="brands"]/div['
        fr_xpath_b = ']/div[1]/div[3]/h3/a'

        name_list = []
        url_list = []
        
        for i in (range(1, num+1)):
            try:
                
                xpath = fr_xpath_f + str(i) + fr_xpath_b
                url =  driver.find_element(by = By.XPATH, value = xpath).get_attribute('href')
                name = driver.find_element(by = By.XPATH, value = xpath).get_attribute("textContent").strip('\n')
                
                url_list.append(url)
                name_list.append(name)
            
            except NoSuchElementException:
                continue

        num = len(url_list)
    except Exception:
        print('---------------'+brand_name+'---------------')
        return None, None, None
    driver.quit()
    time.sleep(5)
    return name_list, url_list, num            


if __name__ == '__main__':

    vdisplay = Xvfb(width=1920, height=1080)
    vdisplay.start()
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    #chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--incognito')
    mobile_emulation = { "deviceName" : "iPhone X" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("disable-infobars")

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOG'] = "false"

    chrome_path = "/home/dhkim/chromedriver"


    url = pd.read_csv('/home/dhkim/Fragrance/failed_country.csv')
    url = url['0']
    data, failed_country_list, failed_fragrance_list= Fragrance_crawler(url,chrome_path,chrome_options)
    failed_country_list = pd.DataFrame(failed_country_list)
    failed_country_list.to_csv('/home/dhkim/Fragrance/failed_country.csv')
    failed_fragrance_list = pd.DataFrame(failed_fragrance_list)
    failed_fragrance_list.to_csv('/home/dhkim/Fragrance/failed_fragrance.csv')
    data.to_csv('/home/dhkim/Fragrance/data/data.csv')

