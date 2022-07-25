from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import copy
import urllib.request
import os
import pandas as pd
from urllib.parse import quote_plus          
from bs4 import BeautifulSoup as bs 
from xvfbwrapper import Xvfb
import time
from multiprocessing.pool import ThreadPool
import threading
import gc
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pdb
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import json
import asyncio
import multiprocessing
import numpy as np
import psutil
import concurrent.futures
from joblib import Parallel, delayed
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth
import undetected_chromedriver.v2 as uc
from Screenshot import Screenshot_Clipping

def accord_element(url,xpath_data, chrome_options, PROXY):
    text = []
    ratio = []
    driver = get_driver(chrome_options, url, PROXY)
    p = re.compile('(?<=width: ).*')
    if driver:
    
        try:
            grid = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,xpath_data['accord_grid'])))
            num = len(grid.find_elements(by = By.CLASS_NAME, value = 'accord-bar'))

            for i in range(1,num+1):
                try:
                    xpath_f = xpath_data['accord_bar_f']
                    xpath_b = xpath_data['accord_bar_b']
                    xpath = xpath_f + str(i) + xpath_b
                    
                    accord = driver.find_element(by = By.XPATH, value = xpath)
                    accord_text = accord.get_attribute("textContent")
                    accord_score = accord.get_attribute("style")
                    accord_score = p.findall(accord_score)[0].strip(';').strip('%')
                    
                    text.append(accord_text)
                    ratio.append(accord_score)
        
                except Exception as e:
                    continue
                    
            driver.quit()
            return text, ratio
        except Exception as e:
            print('---------Time Out-------------')
            driver.quit()
            return None, None
    else: return None, None
    
    

def season_element(url, xpath_data):

    ratio = []
    season = ['winter','spring','summer','fall','day','night']
    p = re.compile('(?<=width: ).*')
    driver = get_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['season_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['season_grid'])))
        for i in range(1,7):
            try:
                #pdb.set_trace()
                xpath_f = xpath_data['season_score_f']
                xpath_b = xpath_data['season_score_b']
                xpath = xpath_f+ str(i) + xpath_b
                
                season_score = driver.find_element(by = By.XPATH, value = xpath)
                bar = season_score.get_attribute("style")
                bar = p.findall(bar)[0].strip(';').strip(' ')
                bar = list(bar)
                cut = bar.index('%')
                bar = bar[:cut]
                bar = "".join(bar)
            
                ratio.append(bar)

            except NoSuchElementException:
                continue
        driver.close()
        return ratio
        
    except Exception as e:
        
        driver.close()
        return None

def note_element(url, xpath_data):
    driver = get_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['notes_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['notes_grid'])))

        try: ## top
            top_notes = driver.find_element(by = By.XPATH, value = xpath_data['top_notes_num'])
            t_num = len(top_notes.find_elements(by = By.TAG_NAME, value = 'div'))
            top_note = notes_finder(driver, xpath_data, t_num, 'top')
            

        except NoSuchElementException:
            top_note = None

        try: ## middle
            middle_notes = driver.find_element(by = By.XPATH, value = xpath_data['middle_notes_num'])
            m_num = len(top_notes.find_elements(by = By.TAG_NAME, value = 'div'))
            mid_note = notes_finder(driver, xpath_data, m_num, 'middle')

        except NoSuchElementException:
            mid_note = None

        try: ## base
            base_notes = driver.find_element(by = By.XPATH, value = xpath_data['base_notes_num'])
            b_num = len(top_notes.find_elements(by = By.TAG_NAME, value = 'div'))
            base_note = notes_finder(driver, xpath_data, b_num, 'base')
        except NoSuchElementException:
            base_note = None

        driver.close()
        return top_note, mid_note, base_note

    except TimeoutException:
        driver.close()
        return None, None, None

def notes_finder(driver, xpath_data, num, type):
    notes = []

    for i in range(1, num+1): ##top note
        xpath_f = xpath_data[type+'_note_f']
        xpath_b = xpath_data[type+'_note_b']
        xpath = xpath_f+ str(i) + xpath_b
        try:
            note = driver.find_element(by = By.XPATH, value = xpath)
            note = note.get_attribute("textContent")
            notes.append(note)
        except NoSuchElementException:
            continue
    
    return notes

def rating_element(url, xpath_data):
    driver = get_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['rating_grid'])))

        try:
       
            rating_score = driver.find_element(by = By.XPATH, value = xpath_data['rating_score'])
            rating_num = driver.find_element(by = By.XPATH, value = xpath_data['rating_num'])
            
            rating_score = rating_score.get_attribute("textContent")
            rating_num = rating_num.get_attribute("textContent")
            driver.close()
            return rating_score, rating_num

        except NoSuchElementException:
            driver.close()
            return None, None

    except TimeoutException:
        driver.close()
        return None, None

def property_element(url, xpath_data, property):
    driver = get_driver()
    try:
        driver.get(url)
    except Exception:
        driver.close()
        return None

    for i in [7,8,9]:
        try:
            
            grid = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['property_grid'])))
            grid = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['property_grid'])))
            driver.switch_to.frame(grid)
            xpath_f = xpath_data['property_grid_f']
            xpath_b = xpath_data['property_grid_b']
            xpath = xpath_f + str(i) + xpath_b

            grid = driver.find_element(by = By.XPATH, value = xpath).get_attribute("class")

            if grid == 'grid-x grid-padding-x grid-padding-y':
                count = property_finder(driver,xpath_data, property, xpath)
        
        except Exception:
            driver.close()
            return None

def property_finder(driver,xpath_data, property, grid_path):

    for i in range(1,15):
        try:
            text_path = grid_path + xpath_data['property_mid'] + str(i) + xpath_data['property_text']
            found_property = driver.find_element(by = By.XPATH, value = xpath).get_attribute("textContent")

            if property == found_property:
                if property == 'SILLAGE': ## -2 -1 1 2
                    count = property_score(driver,xpath_data, grid_path, i, 4)

                elif property == 'GENDER': ##-1 -2 0 2 1 ---- negative female positive male
                    count = property_score(driver,xpath_data, grid_path, i, 4)

                else:   ## -2 -1 0 1 2
                    count = property_score(driver,xpath_data, grid_path, i, 4)

            else:
                continue
        except Exception:
    
            return None
   
    return count

def property_score(driver,xpath_data, grid_path, property_index, num):
    count = []
    for i in range(1, num+1):
        try:
            score_path = grid_path + str(property_index) + xpath_data['score+f'] + str(i) + xpath_data['score_b']
            score = driver.find_element(by = By.XPATH, value = score_path).get_attribute("textContent")
            count.append(score)
        except Exception:
            continue
    return count
    
def img_finder(url,xpath_data):
    driver = get_driver()

    try:
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, xpath_data['img_url'])))
        img_url = driver.find_element(by = By.XPATH, value = xpath_data['img_url'])
        img_url = img_url.get_attribute('src')
        driver.close()
        return img_url  
    except Exception:
        driver.close()
        return None

def perfumer_finder(driver,xpath_data):
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, xpath_data['perfumer'])))
        perfumer = driver.find_element(by = By.XPATH, value = xpath_data['perfumer']).get_attribute("textContent")
        return perfumer
    except Exception:
        return perfumer

def kill_process(name):
    try:
        for proc in psutil.process_iter():
            if proc.name() == name:
                proc.kill()
    except Exception:
        return

def get_driver(chrome_options, url, PROXY):
    driver = None
    count = 0
    
    while (driver == None) and (count < 10):
            try:

                #webdriver.DesiredCapabilities.CHROME['proxy'] = {"httpProxy": PROXY,
                #                                                    "ftpProxy": PROXY,
                #                                                    "sslProxy": PROXY,
                 #                                                   "proxyType": "MANUAL"}
                #webdriver.DesiredCapabilities.CHROME["pageLoadStrategy"] = "none" 

                #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                
                try:
                    driver = uc.Chrome(version_main=103, patcher_force_close=True, use_subprocess=True, chrome_options=chrome_options)
                except Exception:
                    driver = uc.Chrome(version_main=101, patcher_force_close=True, use_subprocess=True, chrome_options=chrome_options)
                stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)
            except Exception:
                count = count + 1
                if driver: driver.quit()
                continue
    
    time.sleep(random.randrange(1,10))
    connect = False
    while connect == False:
        try:
            driver.get(url)
            driver.implicitly_wait(10)
            connect = True
        except Exception:
            continue
    
    ob=Screenshot_Clipping.Screenshot()
    pdb.set_trace()
    img_url=ob.full_Screenshot(driver, save_path=r'./', image_name= str(random.randrange(1,10)) + '.png')
    return driver




def information_crawler(input_args):

    url = input_args[0]
    index = input_args[1]
    xpath_data = input_args[2]
    chrome_options = input_args[3]
    proxy = input_args[4]
    
    accord_text, accord_ratio = accord_element(url, xpath_data, chrome_options, proxy)
    



    #data1, data2 = accord_element(url, xpath_data)

    #data1 = season_element(driver, xpath_data)                  ##['winter','spring','summer','fall','day','night'] error

    #top_note, mid_note, base_note = note_element(driver, xpath_data)
    
    #longevity = property_element(driver, xpath_data, "LONGEVITY")       ##0~5 error


    #sillage = property_element(driver, xpath_data, "SILLAGE")           ##0~4 error
    

    #gender = property_element(driver, xpath_data, "GENDER")             ##f~m error


    #price_value = property_element(driver, xpath_data, "PRICE VALUE")   ##0~5 error


    #erfumer = perfumer_finder(driver,xpath_data)


    
    return index, accord_text, accord_ratio



if __name__ =="__main__":

    #vdisplay = Xvfb(width=1920, height=1080)
    #vdisplay.start()
    chrome_options =uc.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    PROXY =  ['66.29.154.103:3128',
     '66.29.154.105:3128',
     "216.250.156.89:80",
      '154.16.63.16:8080',
       '20.110.214.83:80',
        '5.161.105.105:80',
         '67.212.186.102:80']
    

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("--disable-extensions")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOG'] = "false"



    with open('/home/dhkim/Fragrance/xpath.json', 'r') as f:
        
        xpath_data = json.load(f)
        DB = pd.read_csv('/home/dhkim/Fragrance/data/DB.csv',encoding='latin_1')
        failed = {}
        num_threads = 10
        start = 1116
        end = start + num_threads
        loop = 0

        failed1 = []
        failed2 = []
        pv = []
        for loop in tqdm(range(14008)):
            vdisplay = Xvfb(width=1920, height=1080)
            vdisplay.start()
            datas = []

            proxy = PROXY[random.randrange(0,6)]
            for index in range(start, end):
                tmp = [
                    DB.loc[index,'Url'],
                    index,
                    xpath_data,
                    chrome_options,
                    proxy]
                datas.append(tmp)
                del tmp
            try:
                results = Parallel(n_jobs=num_threads, prefer="threads")(delayed(information_crawler)(data) for data in (datas))
                #pdb.set_trace()
                fail = num_threads
                for result in results:

                    DB.at[result[0], 'accord_txt'] = result[1]
                    DB.at[result[0], 'accord_ratio'] = result[2]
                    if result[1] == None: 
                        failed1.append(result[0])
                        fail = fail - 1
                        
                    if result[2] == None: failed2.append(result[0])
                    rate = fail/num_threads * 100
                print('------------------'+ str(rate) + '%'+'Success------------------')
                if (pv == 0) and (rate == 0):
                    time.sleep(120)

            except Exception as e:
                print(e)

            vdisplay.stop()
            kill_process('chrome')
            kill_process('chromedriver')
            kill_process('chromium-browse')
            kill_process('Xvfb')
            time.sleep(random.randrange(1,10))


            start = start + num_threads
            end = end + num_threads
            loop = loop + 1
       
            if loop % 10 == 0:
                failed_txt = pd.DataFrame(failed1)
                failed_ratio = pd.DataFrame(failed2)

                DB.to_csv('/home/dhkim/Fragrance/data/DB.csv',encoding='latin_1')
                failed_txt.to_csv('/home/dhkim/Fragrance/failed/accord_txt.csv',encoding='latin_1')
                failed_ratio.to_csv('/home/dhkim/Fragrance/failed/accord_ratio.csv',encoding='latin_1')
           
                time.sleep(30)
      
    
     
        