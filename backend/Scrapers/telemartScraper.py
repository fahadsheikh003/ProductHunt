import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import urllib.parse
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_stars(star: WebElement):
    try:
        star = star.get_attribute('class').split()[2]
        return star[13:].replace('-','.')
    except:
        return ""


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

query=input("Enter your search: ")
query = urllib.parse.quote(query)
url = f'https://telemart.pk/search?query={query}'
print(url)
driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
driver.get(url)
namelist=[]
Price=[]
Stars=[]
Reviews=[]
countries=[]
Urls = []
Images = []


driver.implicitly_wait(30)
# products = driver.find_elements(By.CSS_SELECTOR, "div[class='col-span-3 bg-white relative cursor-pointer p-0.5']")
try:
    products = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='col-span-3 bg-white relative cursor-pointer p-0.5']"))
    )
except:
    driver.close()
    exit()
finally:
    products = driver.find_elements(By.CSS_SELECTOR, "div[class='col-span-3 bg-white relative cursor-pointer p-0.5']")
    
for product in products:
    name = product.find_element(By.CSS_SELECTOR, "h4[class='mt-2 text-gray-600 hover:text-blue-600 roboto-new font-normal leading-tight product-title-size text-ellipsis']").text
    namelist.append(name)
    
    try:
        price = product.find_element(By.CSS_SELECTOR,"span[class='inline-block tracking-tighter roboto-new font-normal product-title-size mt-1 text-green-600']").text.replace('\n','.').replace('$', '')
    except:
        price = 0

    Price.append(price)

    # mainImage = product.find_element(By.CSS_SELECTOR, "div[class='col-span-3 bg-white relative cursor-pointer p-0.5']")

    url = product.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
    Urls.append(url)
    
    image = product.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
    Images.append(image)

    try:
        rev=product.find_element(By.CSS_SELECTOR,"a[class='a-link-normal s-underline-text s-underline-link-text s-link-style']").text
    except:
        rev=0

    Reviews.append(rev)
    
    try:
        star = product.find_element(By.CSS_SELECTOR, "span[class='rounded-md bg-green-500 text-xs py-1 roboto-new px-1 text-white']").text
    except:
        star = 0

    Stars.append(star)

    try:
        con = product.find_element(By.CSS_SELECTOR,"div[class='a-row a-size-base a-color-secondary s-align-children-center']").text
    except:
        con = "NULL"
    countries.append(con)
    
# driver.close()
# for i in range(len(namelist)):
#     print(str(i) + ": " + str(namelist[i]) + " " + str(Price[i]) + " " + str(Reviews[i]) + " " + str(Stars[i]) + " " + str(countries[i]), end='\n\n')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df=pd.DataFrame({'Name':namelist, 'Price':Price, 'Rating':Stars, 'Reviews':Reviews, 'Country':countries, 'Images':Images, 'Urls':Urls})
print(df)
