from flask import Flask, request
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import json

from Scrapers.aliexpressScaper import aliexpress_scraper
from Scrapers.amazonScraper import amazon_scraper
from Scrapers.darazScraper import daraz_scraper
from Scrapers.flipkartScraper import flipkart_scraper
from Scrapers.ebayScraper import ebay_scraper
from Utils.filter import product_sorting

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def get_products():
    if request.method == 'GET':
        query = request.args.get('query')
        if query == None:
            return {'status': 'Error! no argument found'}

        try:
            maxPages = 1
            with ThreadPoolExecutor(max_workers=5) as executor:
                aliexpress = executor.submit(aliexpress_scraper, query, maxPages)
                amazon = executor.submit(amazon_scraper, query, maxPages)
                daraz = executor.submit(daraz_scraper, query, maxPages)
                flipkart = executor.submit(flipkart_scraper, query, maxPages)
                ebay = executor.submit(ebay_scraper, query, maxPages)

                aliexpress = aliexpress.result()
                amazon = amazon.result()
                daraz = daraz.result()
                flipkart = flipkart.result()
                ebay = ebay.result()

                frames = [aliexpress, amazon, daraz, flipkart, ebay]
                result = pd.concat(frames)
                            
                # print(json.loads(result.to_json(orient="records")))
            result = json.loads(result.to_json(orient="records"))
            product_sorting(result)
            return {
                'status': 'success',
                'data': result
            }
        except:
            return {
                'status': 'Internal Server Error!'
            }

if __name__ == "__main__":
    app.run(debug=False)