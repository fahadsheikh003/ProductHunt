import pandas as pd
from operator import itemgetter

def rating_reviews_and_price_filter(df: pd.DataFrame):
    return df[(df['rating'] != "") & (df['reviews'] != "") & (df['price'] != "")]

def product_sorting(products: list):
    for product in products:
        product['index'] = float(product['rating']) * int(product['reviews'])

    products.sort(key=itemgetter('index'), reverse=True)