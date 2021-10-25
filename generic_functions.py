# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 20:08:32 2021

@author: Charles
"""

import requests as r
import lxml.html
import regex as re

def fetch_axs_price():
    
    url = 'https://www.coingecko.com/en/coins/axie-infinity'
    
    response = r.get(url).text
    
    html = lxml.html.fromstring(response)
    
    str_usd_price = html.xpath('/html/body/div[4]/div[4]/div[1]/div/div[1]/div[4]/div/div[1]/span[1]/span')[0].text
    usd_price = float(str_usd_price.replace('$', ''))
    
    str_eth_price = html.xpath('/html/body/div[4]/div[4]/div[1]/div/div[1]/div[4]/div/div[3]/div[2]/text()')[0]
    eth_price = float(re.findall(r"(.+) ETH", str_eth_price)[0])
    return usd_price, eth_price
    
def fetch_slp_price():
    
    url = 'https://www.coingecko.com/en/coins/smooth-love-potion'
    
    response = r.get(url).text
    
    html = lxml.html.fromstring(response)
    
    str_usd_price = html.xpath('/html/body/div[4]/div[4]/div[1]/div/div[1]/div[4]/div/div[1]/span[1]/span')[0].text
    usd_price = float(str_usd_price.replace('$', ''))
    
    str_eth_price = html.xpath('/html/body/div[4]/div[4]/div[1]/div/div[1]/div[4]/div/div[3]/div[2]/text()')[0]
    eth_price = float(re.findall(r"(.+) ETH", str_eth_price)[0])
    
    return usd_price, eth_price


if __name__ == '__main__':
    
    print(fetch_slp_price())
    
    
    