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



baseurl = 'https://www.ratebeer.com'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

r = requests.get('https://www.ratebeer.com/breweries/unitedstates/14/213/')
soup = BeautifulSoup(r.content, 'lxml')

brewerylist = soup.find_all("table", class_ = 'tablesorter table borderless table-hover')
brewerylinks = []

char = '#'


for item in brewerylist:
    for link in item.find_all('a', href = True):
        brewerylinks.append(baseurl + link['href'])

brewerylinks = [i for i in brewerylinks if char not in i]       


breweryName = []
beerName = []
status = []
beerType = []
ABV = []
avgRating = []
ratingCount = []
dateAdded = []
numbers = []
address = []
zipcode = []
breweryType = []
presentb = []
retiredb = []
state = []


chrome_options = Options()
#argument to switch off suid sandBox and no sandBox in Chrome 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")

for link in brewerylinks:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.visibility_of_element_located((By.XPATH, './/*[@id="root"]/div[2]/div[1]/div[3]/div[1]/div[2]/table/tfoot/tr/td/div/div[2]/div/div[3]/button[2]')))
    
    while True:

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        base_soup = BeautifulSoup(r.content, 'lxml')
        

        name_html = soup.findAll("div", {"class": ["MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn text-500 colorized__WrappedComponent-hrwcZr bRPQdN MuiTypography-body1",
                                            "MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn text-500 colorized__WrappedComponent-hrwcZr gRvDpm MuiTypography-body1"]})
        for name in name_html:
            beerName.append(name.get_text())
            breweryName.append(soup.find("title").get_text())
            breweryType.append(soup.find("div", {"class":"MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn colorized__WrappedComponent-hrwcZr hwjOn MuiTypography-subtitle1"}).get_text())
            address.append(soup.find("div", {"class":"MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn colorized__WrappedComponent-hrwcZr hwjOn MuiTypography-body2"}).get_text())
            state.append("IL")            

        p_name_html = soup.findAll("div", {"class": "MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn text-500 colorized__WrappedComponent-hrwcZr bRPQdN MuiTypography-body1"})

        for pname in p_name_html:
            presentb.append(pname.get_text())

        r_name_html = soup.findAll("div", {"class": "MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn text-500 colorized__WrappedComponent-hrwcZr gRvDpm MuiTypography-body1"})
        for rname in r_name_html:
            retiredb.append(rname.get_text())               
            
        type_html = soup.findAll("div", {"class":"MuiTypography-root Text___StyledTypographyTypeless-bukSfn pzIrn colorized__WrappedComponent-hrwcZr bRPQdN fd-r fa-c MuiTypography-body2"})

        for types in type_html:
            beerType.append(types.get_text())

        rating_html = soup.findAll("td", {"class":"MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall"})

        for rates in rating_html:
            numbers.append(rates.get_text())

        avgRating = numbers[1::6]

        ratingCount = numbers[4::6]

        ABV = numbers[5::6]

        date_html = soup.findAll("td", {"style":"white-space: nowrap;"})

        for dates in date_html:
            dateAdded.append(dates.get_text())

        time.sleep(1)
        
        if next_button.is_enabled():
            driver.execute_script("arguments[0].click();", next_button)
    

        else:
            break

    ratebeer = {'State': state, 'Brewery Name': breweryName, 'Brewery Type': breweryType, 'Beer Name': beerName, 'Beer Type': beerType, 'ABV': ABV, 'Average Rating':avgRating,
                'Rating Count':ratingCount, 'Date Added': dateAdded, 
                 'Address': address}

    #    ratebeer['Zip Code'] = ratebeer['Address'].str.extract(r '(\d{5}\-?\d{0,4})')

    ratebeer["Status"] = []
    beerlist = list(ratebeer["Beer Name"])

    for beer in beerlist:
        if beer in presentb:
            ratebeer["Status"].append("Present")
        elif beer in retiredb:
            ratebeer["Status"].append("Retired")
        else:
            print("error")
            print(beer)
