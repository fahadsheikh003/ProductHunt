import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import quote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.filter import rating_reviews_and_price_filter

def get_rating(rating: WebElement):
    try:
        x = 0
        for i in rating:
            attr = i.get_attribute('class').split()[1]
            pos1 = attr.find('-')
            pos2 = attr.find('--')
            intx = int(attr[pos1+1:pos2])
            x += intx
        return str(x / 10)
    except:
        return ""

def daraz_scraper(query: str, maxPages: int):
    if query == "" or maxPages < 1:
        return None

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")

    pageNo = 1

    url = f'https://www.daraz.pk/catalog/?from=input&page={pageNo}&q={query}'

    Name = []
    Price = []
    Rating = []
    Reviews = []
    # Country = []
    ProductUrl = []
    Image = []

    while pageNo <= maxPages:
        driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
        driver.get(url)

        try:
            products = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='gridItem--Yd0sa']"))
            )
        except:
            print("Unable to load products in webpage")
            driver.close()     
            break
        else:
            products = driver.find_elements(By.CSS_SELECTOR, "div[class='gridItem--Yd0sa']")

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, "div[class='title--wFj93']").text
            except:
                name = ""
            Name.append(name)
            
            try:
                price = product.find_element(By.CSS_SELECTOR,"div[class='price--NVB62']").text.replace('Rs. ','').replace(',','')
            except:
                price = ""
            Price.append(price)

            try:
                productUrl = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except:
                productUrl = ""    
            ProductUrl.append(productUrl)
            
            try:
                image = product.find_element(By.CSS_SELECTOR, "img[class='image--WOyuZ ']").get_attribute('src')
            except:
                image = ""
            Image.append(image)
            
            try:
                reviews = product.find_element(By.CSS_SELECTOR, "span[class='rating__review--ygkUy']").text.replace('(','').replace(')', '').replace(',','')
            except:
                reviews = ""
            Reviews.append(reviews)
            
            try:
                rating = product.find_elements(By.CSS_SELECTOR, "i[class^='star-icon--k88DV']")
            except:
                rating = ""
            Rating.append(get_rating(rating))

            # try:
            #     country = product.find_element(By.CSS_SELECTOR,"span[class^='location--eh0Ro ']").text
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
        'site':['daraz' for _ in range(len(Name))]
    })
    df = rating_reviews_and_price_filter(df)
    return df

# if __name__ == "__main__":
#     query = input("Enter your search: ")
#     query = quote(query)
#     df = daraz_scraper(query, 1)
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', None)
#     print(df)