from requests_html import HTMLSession
import requests
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re



baseurl = "https://www.beeradvocate.com"

brewerylinks = []
base = "https://www.beeradvocate.com"



# change state name in the brewery_url for each state
for i in range(3):
    brewery_url = "https://www.beeradvocate.com/place/list//?start={}&c_id=US&s_id=SD&brewery=Y&sort=name".format(i*20)
    brewery_r = requests.get(brewery_url.format(i*20))
    brewery_soup = BeautifulSoup(brewery_r.content, "lxml")
    bt = brewery_soup.find_all("td", {"colspan" : "2", "align":"left", "valign":"top"})

    for item in bt:
        for link in item.find_all("a", href = True):
            brewerylinks.append(baseurl + link['href'])

breweryName = []
beerName = []
status = []
style = []
abv = []
numbers = []
address = []
zipcode = []
lastactive = []
state = []
pdev = [] 
score = []
last = []
average = []
review = []
added = []
rating = []

# adding options to control errors
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--window-position=2000,0")
#chrome_options.add_argument('disable-infobars')

beerlinks = []    

for link in brewerylinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    rr = requests.get(link + "?view=beers&show=retired#lists")
    rsoup = BeautifulSoup(rr.content, "html.parser")
    pp = soup.find("div", {"id": "info_box"})
    # change state name
    try:
        if re.search('South Dakota</a>, (.*)<br/><a href="/place/directory/9/US/"', str(pp)) != None:
            result = re.search('South Dakota</a>, (.*)<br/><a href="/place/directory/9/US/"', str(pp))
    except:
        result = re.search('South Dakota</a>, (.*), <a href="/place/directory/9/US/"', str(pp))

    
    beerlist = soup.find_all("tbody")
    rbeerlist = rsoup.find_all("tbody")
    # loops for beer urls
    for item in beerlist:
        for link in item.find_all('a', href = True):
            beerlinks.append(base + link['href'])
            zipcode.append(result.group(1))

    for item in rbeerlist:
        for link in item.find_all('a', href = True):
            beerlinks.append(base + link['href'])
            zipcode.append(result.group(1))
            
        
beerlinks = beerlinks[0::2]
zipcode = zipcode[0::2]
    
for blink in beerlinks:
    beerr = requests.get(blink)
    bsoup = BeautifulSoup(beerr.content, "html.parser")
    tool_html = bsoup.findAll("dd", {"class": "beerstats"})

    
    beerName.append(bsoup.find("title").get_text())
        
    test = []

    for tool in tool_html:
        test.append(tool.get_text())

    for name in test[0::13]:
        breweryName.append(name)
        
        # change state name
        state.append("SD")
        
    for s in test[2::13]:
        style.append(s)

    for x in test[3::13]:
        abv.append(x)

    for y in test[4::13]:
        re.findall("\d+\.\d+", y)
        score.append(y[0:2])

    for avg in test[5::13]:
        re.findall("\d+\.\d+", avg)
        average.append(avg[0:4])

    for pdevs in test[5::13]:
        re.findall("\d+\.\d+", pdevs)
        pdev.append(pdevs[13:])

    for i in test[6::13]:
        review.append(i)

    for rat in test[7::13]:
        rating.append(rat)

    for stat in test[8::13]:
        status.append(stat)

    for lastdate in test[9::13]:
        re.findall("\d+\.\d+", lastdate)
        last.append(lastdate[1:])

    for date in test[10::13]:
        added.append(date)


beerad = {'State': state, 'Brewery_Name': breweryName, 'Address': zipcode, 'Beer_Name': beerName,
          'Style': style, 'ABV':abv, 'Score': score, 'Avg': average, 'pDev': pdev, 
          'Review': review, 'Rating': rating, 'Status':status, 'Added': added,
          'Last_Active':last
         }


import pandas as pd

beerad = pd.DataFrame(beerad)
beerad.to_csv("beerad_SD.csv")
