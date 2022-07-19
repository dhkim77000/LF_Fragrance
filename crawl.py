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
from concurrent import futures
import numpy as np
import concurrent.futures
def accord_element(driver, xpath_data):
    text = []
    ratio = []
   
    p = re.compile('(?<=width: ).*')
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,xpath_data['accord_grid'])))
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_data['accord_grid'])))

        grid = driver.find_element(by = By.XPATH, value = xpath_data['accord_grid'])
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
    
            except NoSuchElementException:
                continue
      
        return text, ratio
    except TimeoutException:
        return None, None
    

def season_element(driver, xpath_data):

    ratio = []
    season = ['winter','spring','summer','fall','day','night']
    p = re.compile('(?<=width: ).*')

    try:
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

        return ratio
        
    except Exception as e:
        print(e)
        return None

def note_element(driver, xpath_data):

    try:
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
            
        return top_note, mid_note, base_note

    except TimeoutException:
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

def rating_element(driver, xpath_data):
    
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['rating_grid'])))

        try:
       
            rating_score = driver.find_element(by = By.XPATH, value = xpath_data['rating_score'])
            rating_num = driver.find_element(by = By.XPATH, value = xpath_data['rating_num'])
            
            rating_score = rating_score.get_attribute("textContent")
            rating_num = rating_num.get_attribute("textContent")
            return rating_score, rating_num

        except NoSuchElementException:
            return None, None

        
    except TimeoutException:
        return None, None

def property_element(driver, xpath_data, property):
    for i in [7,8,9]:
        try:
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['property_grid'])))
            WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['property_grid'])))

            xpath_f = xpath_data['property_grid_f']
            xpath_b = xpath_data['property_grid_b']
            xpath = xpath_f + str(i) + xpath_b

            grid = driver.find_element(by = By.XPATH, value = xpath).get_attribute("class")

            if grid == 'grid-x grid-padding-x grid-padding-y':
                count = property_finder(driver,xpath_data, property, xpath)
        
        except Exception:
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
    
def img_finder(driver,xpath_data):

    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, xpath_data['img_url'])))
        url = driver.find_element(by = By.XPATH, value = xpath_data['img_url'])
        url = url.get_attribute('src')
        return url  
    except Exception:
        return None

def perfumer_finder(driver,xpath_data):
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, xpath_data['perfumer'])))
        perfumer = driver.find_element(by = By.XPATH, value = xpath_data['perfumer']).get_attribute("textContent")
        return perfumer
    except Exception:
        return perfumer


def information_crawler(input_data):

    url_data = input_data[0] 
    index = input_data[1]
    xpath_data = input_data[2]
    write_data1  = input_data[3]
    write_data2 = input_data[4]
    chrome_options = input_data[5]
    

    failed_fragrance1 = []
    failed_fragrance2 = []

    for i in tqdm(list(url_data.index.values)):
        
        brand = url_data.loc[i,'Brand']
        fr_name = url_data.loc[i,'Fragrance']
        url = url_data.loc[i,'Url']
        driver = None
        try:

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
            #img_url = img_finder(driver,xpath_data)
    
            #pdb.set_trace()
            accord_text, accord_ratio = accord_element(driver, xpath_data)
            
            #rating, rating_count = rating_element(driver, xpath_data)   

            #season_count = season_element(driver, xpath_data)                  ##['winter','spring','summer','fall','day','night'] error

            #top_note, mid_note, base_note = note_element(driver, xpath_data)

            #longevity = property_element(driver, xpath_data, "LONGEVITY")       ##0~5 error

            #sillage = property_element(driver, xpath_data, "SILLAGE")           ##0~4 error

            #gender = property_element(driver, xpath_data, "GENDER")             ##f~m error

            #price_value = property_element(driver, xpath_data, "PRICE VALUE")   ##0~5 error

            #perfumer = perfumer_finder(driver,xpath_data)

        except Exception:
            accord_text, accord_ratio = None, None

        write_data1.loc[i, 'accord_text'] = accord_text
        write_data2.loc[i, 'accord_ratio'] = accord_ratio

        if accord_text == None: failed_fragrance1.append(url)
        if accord_ratio == None: failed_fragrance2.append(url)

        if i%200 == 0:
            write_data1.to_csv('/home/dhkim/Fragrance/data/DB_accord_text.csv')
            write_data1.to_csv('/home/dhkim/Fragrance/data/DB_accord_ratio.csv')

            failed1 = pd.DataFrame(failed_fragrance1)
            failed1.to_csv('/home/dhkim/Fragrance/failed_accord_text.csv')
            failed2 = pd.DataFrame(failed_fragrance2)
            failed2.to_csv('/home/dhkim/Fragrance/failed_accord_ratio.csv')

        if driver:    
           driver.close()

    return accord_text, accord_ratio

def crawl(data, *, loop):
    loop.run_in_executor(executor, information_crawler, data)

if __name__ =="__main__":

    vdisplay = Xvfb(width=1920, height=1080)
    vdisplay.start()
    
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--remote-debugging-port=9222")
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
        data = pd.read_csv('/home/dhkim/Fragrance/data/data_final.csv',encoding='latin_1')
        
        num_chunks = len(data) // 6
        
        write_data1 = pd.DataFrame(index = range(len(data)), columns = ['Fragrance','accord_text'])
        write_data2 = pd.DataFrame(index = range(len(data)), columns = ['Fragrance','accord_ratio'])
        write_data1.loc[:, 'Fragrance'] =  data['Fragrance']
        write_data2.loc[:, 'Fragrance'] =  data['Fragrance']

        url_chunks = np.array_split(data,num_chunks)
    

        datas = []
        for index in range(num_chunks):
            tmp = [
                pd.DataFrame(url_chunks[index]),
                index,
                xpath_data,
                write_data1,
                write_data2,
                chrome_options]
            datas.append(tmp)
            del tmp

      
        #pdb.set_trace()
        i = 0
        while i < num_chunks:
            datas = []
            for index in range(i, i + 6):
                tmp = [
                    pd.DataFrame(url_chunks[index]),
                    index,
                    xpath_data,
                    write_data1,
                    write_data2,
                    chrome_options]
                datas.append(tmp)
                del tmp

            with futures.ThreadPoolExecutor(6) as executor: # default/optimized number of threads
                result = list(executor.map(information_crawler, datas))
                

   


      
    
     
        