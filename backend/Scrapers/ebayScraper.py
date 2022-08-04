import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import quote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from Utils.currencyConverter import CurrencyConverter
from Utils.filter import rating_reviews_and_price_filter

def ebay_scraper(query: str, maxPages: int):
    if query == "" or maxPages < 1:
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")

    pageNo = 1

    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_pgn={pageNo}&LH_ItemCondition=1000&&LH_BIN=1"

    Name = []
    Price = []
    Rating = []
    Reviews = []
    ProductUrl = []
    Image = []
    C = CurrencyConverter()

    while pageNo <= maxPages:
        driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
        driver.get(url)

        try:
            products = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='s-item__wrapper clearfix']"))
            )
        except:
            print("Unable to load products in webpage")
            driver.close()
            break
        else:
            products = driver.find_elements(By.CSS_SELECTOR, "div[class='s-item__wrapper clearfix']")

        sponsoredClass = re.findall('span\.([^\s\{]+)\s*\{\s*display\:\s*inline;', driver.page_source)[0]

        for product in products:
            try:
                product.find_element(By.CSS_SELECTOR, f"span[class^='{sponsoredClass}']")
                sponsored = True
            except:
                sponsored = False

            if sponsored:
                continue

            try:
                name = product.find_element(By.CSS_SELECTOR, "h3[class='s-item__title']").text.replace('NEW LISTING','')
            except:
                name = ""
            Name.append(name)
            
            try:
                price = product.find_element(By.CSS_SELECTOR,"span[class='s-item__price']").text

                if 'to' in price:
                    price = price.split()[2]

                price = price.replace('$','').replace(',','')
                price = str(C.convert('USD','PKR',float(price)))
            except:
                price = ""
            Price.append(price)

            try:
                productUrl = product.find_element(By.CSS_SELECTOR, "a[class='s-item__link']").get_attribute('href')
            except:
                productUrl = ""
            ProductUrl.append(productUrl)
            
            try:
                image = product.find_element(By.CSS_SELECTOR, "img[class='s-item__image-img']").get_attribute('src')
            except:
                image = ""
            Image.append(image)

            try:
                reviews = product.find_element(By.CSS_SELECTOR,"span[class='s-item__reviews-count']").find_element(
                    By.CSS_SELECTOR, "span").text.split()[0].replace(',','')
            except:
                reviews = ""
            Reviews.append(reviews)
            
            try:
                rating = product.find_element(By.CSS_SELECTOR, "div[class='x-star-rating']").find_element(
                    By.CSS_SELECTOR, "span[class='clipped']").text.split()[0]
            except:
                rating = ""
            Rating.append(rating)
            
        driver.close()
        pageNo += 1

    df = pd.DataFrame({'name':Name, 'price':Price, 'rating':Rating, 'reviews':Reviews, 'image':Image, 'url':ProductUrl, 'site':['ebay' for _ in range(len(Name))]})
    df = rating_reviews_and_price_filter(df)
    return df

# if __name__ == "__main__":
#     query = input("Enter your search: ")
#     query = quote(query)
#     df = ebay_scraper(query, 1)
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', None)    
#     print(df)