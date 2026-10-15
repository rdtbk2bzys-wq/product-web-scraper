import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0.0.0 Safari/537.36",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9"}

products = []
num = 0

def get_data(link,html,**kwargs):
    data = None
    response = requests.get(link, headers=headers, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find(html,**kwargs)
        response.status_code
    return data, response.status_code

def basic_column(data,html,**kwargs):
    column = data.find(html,**kwargs)
    if column is None:
        return None
    else:
        return column.text.strip()

def not_basic_column(data,next_sibling,html,**kwargs):
    column = data.find(html,**kwargs)
    if column is not None:
        column1 = column.parent.find_next_sibling(next_sibling)
        if column1 is not None:
            column = column1.text.strip()
        else:
            column = None
    else:
        column = None
    return column

while True:
    num += 1
    print(num)
    time.sleep(1)
    link = "https://scrapingsandbox.com/product/" + str(num)

    data = get_data(link,"div", class_="grid grid-cols-1 lg:grid-cols-2 gap-8")
    if not data:
        break

    product_id = int(num)
    title = basic_column(data, "h1", class_="text-2xl font-bold text-foreground")
    vendor = basic_column(data, "span", class_="text-xs font-mono uppercase tracking-wider text-muted-foreground")
    category = basic_column(data, "span", attrs = {"data-variant": "secondary"})
    description = basic_column(data, "p", class_="text-sm text-muted-foreground leading-relaxed")
    sku = not_basic_column(data, "span", "span", string="SKU")
    created_at = not_basic_column(data, "span", "span", string="Scraped")


    price = data.find("span", class_="text-3xl font-bold font-mono text-primary")
    if not price:
        price = None
    else:
        price = float(price.text.replace("$",""))

    old_price = data.find("span", class_="text-lg font-mono text-muted-foreground line-through")
    if  not old_price:
        old_price = None
    else:
        old_price = old_price.text
        old_price = float(old_price.replace("$", ""))

    image = data.find("img", class_="h-full w-full object-cover")
    if not image:
        image = None
    else:
        image = image.get("src")

    tags = data.find_all("span", {"data-variant":"outline"})
    if  not tags:
        tags = None
    else:
        tags1 = []
        for i in tags:
            tags1.append(i.text.strip())
        tags = ",".join(tags1)

    in_stock = data.find("span", class_="rounded-full bg-destructive/90 px-4 py-1.5 text-sm font-mono text-destructive-foreground")
    if not in_stock :
        in_stock = True
    else:
        in_stock = False

    review_count = data.find("span", class_="text-xs text-muted-foreground font-mono")
    if not revive_count:
        revive_count = None
    else:
        revive_count = int(revive_count.text.replace("(","",).replace(")","").replace("reviews",""))

    rating = data.find("span", class_="text-sm font-mono font-semibold text-foreground")
    if not rating:
        rating = None
    else:
        rating = float(rating.text)

    product = {
        "id": product_id,
        "title": title,
        "vendor": vendor,
        "category": category,
        "price": price,
        "old_price": old_price,
        "description": description,
        "image": image,
        "tags": tags,
        "in_stock": in_stock,
        "review_count": review_count,
        "rating": rating,
        "sku": sku,
        "created_at": created_at
    }

    products.append(product)

df = pd.DataFrame(products)
df.to_csv("products.csv", index=False, encoding="utf-8-sig")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

df = pd.read_csv("products.csv")
print(df.info())