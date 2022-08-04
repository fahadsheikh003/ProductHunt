Welcome to ProductHunt

The backend of this project scrapes data from daraz, aliexpress, amazon, flipkart, and ebay using selenium at runtime, standardize that data and sends that data in response to the request using flask.

The frontend of this project is very minimalistic and designed in React js.

Please install all the backend requirements that are specified in "backend/requirements.txt" and frontend requirements that are specified in "frontend/package.json"
NOTE: It is recommended to install these requirements in a virtual environment and run this script in that environment

NOTE: selenium uses a browser as a driver in order to interact with the website

The version of the Chrome driver that is used for this project is "ChromeDriver 103.0.5060.134"

You can replace the chrome driver in the working directory if it isn't compatible with your device. Use link: https://chromedriver.chromium.org/downloads to download chrome driver.

Flow of Project:

    1. Search for the product you to hunt
    2. The search query is then sent to the backend server using GET request
    3. Upon receiving the search query, the backend starts five threads and starts scraping data from all the mentioned sites for the specified search query
    4. After scraping and standardizing data that is scraped, backend sorts the data on the basis of rating and reviews and sends the response to frontend accordingly
    5. Upon receiving data from backend, frontend loads the data, renders the data and displays that data on the screen (by the way the site is fully responsive)

Credits:
developed by Devil