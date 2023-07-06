#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import argparse
import numpy as np
import time
import os

options = ["avg", "best"]

def getPrices(option="avg", sell=False, sleep=3):

    """
    Load the Binance page return prices of USDT

    options:

    > avg: return the average of the proces
    > best: return thr best price
    """


    if option not in options:
        print("Not a valid option!")
        return
        
    print("Loading data from binance...")

    # Set MOZ_HEADLESS environment variable
    os.environ['MOZ_HEADLESS'] = '1'


    # Instantiate the Chrome driver
    driver = webdriver.Firefox()
    
    prices = []

    url = "https://p2p.binance.com/en/trade/all-payments/USDT?fiat=DZD" if not sell else "https://p2p.binance.com/en/trade/sell/USDT?fiat=DZD&payment=all-payments"
    # Load a web page
    driver.get(url)

    # wait for the prices to load
    time.sleep(sleep)

    # Find all price elements
    element = driver.find_elements(By.CLASS_NAME, "css-1m1f8hn")

   
    for elem in element:
        prices.append(float(elem.get_attribute("innerHTML")))


    # Close the browser
    driver.quit()

    if prices == []: # If the page did not load, increase the sleep time
        print("Could not load prices info, retrying ...")
        price = getPrices(option,sell=sell, sleep=sleep + 2)
    elif option == "avg":
        price = round(np.mean(prices), 2)
    elif option == "best":
        price = prices[0]
   

    return price

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Command for Converting back and fourth between DZD and USD by using the USDT cryptocurrency")

    parser.add_argument("-b", "--best", dest="best", action='store_true', help="If specified give the best value of USDT in market, else give the average of the top sellers' prices")

    parser.add_argument("-s", "--sell", dest="sell", action='store_true', help="If specified give the best value of USDT in market, else give the average of the top sellers' prices")

    args = parser.parse_args()

    print(getPrices("best" if args.best else "avg", sell=args.sell))