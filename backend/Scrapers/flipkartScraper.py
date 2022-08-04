import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import quote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.currencyConverter import CurrencyConverter
from Utils.filter import rating_reviews_and_price_filter

def get_reviews(reviews: str):
    try:
        pos1 = reviews.find('& ')
        pos2 = reviews.find(' Reviews')
        return reviews[pos1+1:pos2].replace(',','')
    except:
        return ""

def flipkart_scraper(query: str, maxPages: int):
    if query == "" or maxPages < 1:
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")

    pageNo = 1

    url = f'https://www.flipkart.com/search?page={pageNo}&q={query}'

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
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='_13oc-S']"))
            )
        except:
            print("Unable to load products in webpage")
            driver.close()
            break
        else:
            products = driver.find_elements(By.CSS_SELECTOR, "div[class='_13oc-S']")

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, "div[class='_4rR01T']").text
            except:
                name = ""
            Name.append(name)
            
            try:
                price = (product.find_element(By.CSS_SELECTOR,"div[class='_30jeq3 _1_WHN1']").text)[1:].replace(',','')
                price = str(C.convert('INR', 'PKR', float(price)))
            except:
                price = ""
            Price.append(price)

            try:
                productUrl = product.find_element(By.CSS_SELECTOR, "a[class='_1fQZEK']").get_attribute('href')
            except:
                productUrl = ""
            ProductUrl.append(productUrl)
            
            try:
                image = product.find_element(By.CSS_SELECTOR, "img[class='_396cs4 _3exPp9']").get_attribute('src')
            except:
                image = ""
            Image.append(image)

            try:
                reviews = product.find_element(By.CSS_SELECTOR,"span[class='_2_R_DZ']").text
                reviews = get_reviews(reviews)
            except:
                reviews = ""
            Reviews.append(reviews)
            
            try:
                rating = product.find_element(By.CSS_SELECTOR, "div[class='_3LWZlK']").text
            except:
                rating = ""
            Rating.append(rating)
            
        driver.close()
        pageNo += 1

    df=pd.DataFrame({'name':Name, 'price':Price, 'rating':Rating, 'reviews':Reviews, 'image':Image, 'url':ProductUrl, 'site':['flipkart' for _ in range(len(Name))]})
    df = rating_reviews_and_price_filter(df)
    return df

# if __name__ == "__main__":
#     query = input("Enter your search: ")
#     query = quote(query)
#     df = flipkart_scraper(query, 1)
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', None)
#     print(df)