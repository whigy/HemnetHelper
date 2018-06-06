# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:01:24 2018

@author: whigy
"""

import re
import os
import time
import json
import logging
from selenium import webdriver

def openBrowser(url):
    browser = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'))
    time.sleep(3)
    
    logging.info("Get URL {:s}".format(url))
    browser.get(url)
    logging.info("Brower ready.")
    return browser

def getHemnetBasic(url):
    browser = openBrowser(url)
    
    logging.info("Parsing Hemnet Webpage.")
    meta = {}
    # Get title
    meta['url'] = url
    meta['address'] = browser.find_element_by_class_name('property__address').text
    meta['location'] = browser.find_element_by_class_name('property-location').text
    meta['price'] = int(browser.find_element_by_class_name('property__price').text.replace(" ", "")[:-2])
    attributes = browser.find_element_by_class_name('property__attributes').text.split("\n")
    meta['attributes'] = dict(zip(attributes[::2], attributes[1::2]))
    ## TODO: GOOGLE MAPAPI
    
    # Visiting
    try:
        visnings = browser.find_elements_by_class_name('open-house__time')
        meta['open_time'] = [x.text for x in visnings]
    except Exception:
        meta['open_time'] = []
    
    logging.info("Jomping to bank web pages for loan information.")
    # Banks
    bank_elements = browser.find_elements_by_xpath("//li[@class='calculator-list__calculator']/a")
    meta["banks_info"] = getLoanComparison(bank_elements)
    
    return meta, browser
    
def getLoanComparison(bank_elements):
    bank_info = {}
    for bank in bank_elements:
        dic = {}
        name = bank.text
        url = bank.get_attribute("href")
        #new_browser = openBrowser(url)
        dic["url"] = url
        
        # Todo:fetch different information from different banks
        bank_info[name] = dic
    return bank_info

def getNeighbourhoodReport(address):
    # Hita!
    return

def calculateBasicInfo(meta):
    return
    
# Test 
if __name__ == "__main__":
    logging.info("Start!")
    
    url = "https://www.hemnet.se/bostad/bostadsratt-1,5rum-rasunda-solna-kommun-forradsgatan-7,-1-tr-12633936"
    meta, browser = getHemnetBasic(url)
    browser.quit()
    
    filename ="{:s}_{:s}".format(time.strftime('%Y%m%d_%H%M'), meta['address'])
    json_file = ".\\output\\{:s}.json".format(filename)
    logging.info("Done! Dumping meta data to Json file:\n{:s}".format(json_file))
    
    with open(json_file, 'w') as fp:
        json.dump(meta, fp)
    
    
    
    
    