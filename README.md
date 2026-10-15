# Product Web Scraper

## About
A Python web scraper that collects product data from Scraping Sandbox, processes it, and exports the results to a CSV file.

## Technologies

* Python
* Requests
* BeautifulSoup (lxml)
* Pandas

## Data Collected
* **Product Details:** Name, vendor, category
* **Pricing:** Current and original prices
* **Media & Classification:** Description, image URL, tags
* **Inventory:** Stock availability
* **Metrics:** Rating and review count
* **Metadata:** SKU and date information

## How It Works
1. Sends HTTP requests to product pages.
2. Extracts data from HTML using BeautifulSoup.
3. Processes values and handles missing fields.
4. Saves the results to `products.csv`.


