import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import quote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.filter import rating_reviews_and_price_filter
from Utils.currencyConverter import CurrencyConverter

def get_rating(rating: WebElement):
    try:
        rating = rating.get_attribute('class').split()[2]
        return rating[13:].replace('-','.')
    except:
        return ""

def amazon_scraper(query: str, maxPages: int):
    if query == "" or maxPages < 1:
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")

    pageNo = 1

    url = f'https://www.amazon.com/s?page={pageNo}&k={query}'

    Name = []
    Price = []
    Rating = []
    Reviews = []
    # Country = []
    ProductUrl = []
    Image = []

    C = CurrencyConverter()

    while pageNo <= maxPages:
        driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
        driver.get(url)

        try:
            products = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16']"))
            )
        except:
            print("Unable to load products in webpage")
            driver.close()
            break
        else:
            products = driver.find_elements(By.CSS_SELECTOR, "div[class='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16']")

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, "div[class='a-section a-spacing-none puis-padding-right-small s-title-instructions-style']").text
            except:
                name = ""
            Name.append(name)
            
            try:
                price = product.find_element(By.CSS_SELECTOR,"span[class='a-price']").text.replace('\n','.').replace('$','')
                price = str(C.convert('USD', 'PKR', float(price)))
            except:
                price = ""
            Price.append(price)

            try:
                productUrl = product.find_element(By.CSS_SELECTOR, "a[class='a-link-normal s-no-outline']").get_attribute('href')
            except:
                productUrl = ""
            ProductUrl.append(productUrl)
            
            try:
                image = product.find_element(By.CSS_SELECTOR, "img[class='s-image']").get_attribute('src')
            except:
                image = ""
            Image.append(image)

            try:
                reviews = product.find_element(By.CSS_SELECTOR,"a[class='a-link-normal s-underline-text s-underline-link-text s-link-style']").text.replace(',','')
            except:
                reviews = ""
            Reviews.append(reviews)
            
            try:
                rating = product.find_element(By.CSS_SELECTOR, "i[class^='a-icon a-icon-star-small']")
                rating = get_rating(rating)
            except:
                rating = ""

            Rating.append(rating)

            # try:
            #     country = product.find_element(By.CSS_SELECTOR,"div[class='a-row a-size-base a-color-secondary s-align-children-center']").text
            # except:
            #     country = ""
            # Country.append(country)
            
        driver.close()
        pageNo += 1

    df = pd.DataFrame({
        'name':Name, 
        'price':Price, 
        'rating':Rating, 
        'reviews':Reviews, 
        # 'country':Country, 
        'image':Image, 
        'url':ProductUrl,
        'site':['amazon' for _ in range(len(Name))]
    })
    df = rating_reviews_and_price_filter(df)
    return df

# if __name__ == "__main__":
#     query = input("Enter your search: ")
#     query = quote(query)
#     df = amazon_scraper(query, 1)
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', None)
#     print(df)