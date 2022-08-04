import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import quote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Utils.supposition import get_reviews_from_sold_quantity
from Utils.filter import rating_reviews_and_price_filter

def get_sold_quantity(sold: str):
    pos = sold.find(' sold')
    return sold[:pos]

def aliexpress_scraper(query: str, maxPages: int):
    if query == "" or maxPages < 1:
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")

    pageNo = 1

    url = f'https://www.aliexpress.com/wholesale?page={pageNo}&SearchText={query}'

    Name = []
    Price = []
    Rating = []
    SoldQuantity = []
    ProductUrl = []
    Image = []
    # Shipping = []
    Reviews = []

    while pageNo <= maxPages:
        driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
        driver.get(url)

        try:
            products = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='_3t7zg _2f4Ho'"))
            )
        except:
            driver.close()
            break
        
        # to render page contents
        height = driver.execute_script("return document.body.scrollHeight")
        xt = height/10
        i = xt
        while i <= height:
            driver.execute_script(f"window.scrollTo(0,{i});")
            time.sleep(0.5)
            height = driver.execute_script("return document.body.scrollHeight")
            i = i + xt

        products = driver.find_elements(By.CSS_SELECTOR, "a[class='_3t7zg _2f4Ho'")

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, "div[class='_1tu1Z Vgu6S']").text
            except:
                name = ""
            Name.append(name)
            
            try:
                price = product.find_element(By.CSS_SELECTOR,"div[class='mGXnE _37W_B']").text
            except:
                price = ""
            price = price.replace('PKR','').replace(',','')
            Price.append(price)

            try:
                productUrl = product.get_attribute('href')
            except:
                productUrl = ""
            ProductUrl.append(productUrl)
            
            try:
                image = product.find_element(By.CSS_SELECTOR, "img[class='_1RtJV product-img']").get_attribute('src')
            except:
                image = ""
            Image.append(image)

            try:
                sold = product.find_element(By.CSS_SELECTOR,"span[class='_1kNf9']").text
                sold = str(get_sold_quantity(sold))
            except:
                sold = ""
            SoldQuantity.append(sold)
            
            if sold != "":
                reviews = str(get_reviews_from_sold_quantity(int(sold)))
            else:
                reviews = ""
            Reviews.append(reviews)

            try:
                rating = product.find_element(By.CSS_SELECTOR, "span[class='eXPaM']").text
            except:
                rating = ""
            Rating.append(rating)
            
            # try:
            #     shipping = product.find_element(By.CSS_SELECTOR, "span[class='_2jcMA']").text
            # except:
            #     shipping = ""
            # Shipping.append(shipping)

        driver.close()
        pageNo += 1
        
    df = pd.DataFrame({
        'name':Name, 
        'price':Price, 
        'rating':Rating, 
        'reviews':Reviews,
        # 'Quantity Sold':SoldQuantity, 
        # 'Shipping Charges':Shipping, 
        'image':Image, 
        'url':ProductUrl,
        'site':['aliexpress' for _ in range(len(Name))]
    })
    df = rating_reviews_and_price_filter(df)
    return df

# if __name__ == "__main__":
#     query = input("Enter your search: ")
#     query = quote(query)
#     df = aliexpress_scraper(query, 1)
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', None)
#     print(df)