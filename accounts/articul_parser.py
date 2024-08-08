import requests
import math

def parse_products(articul: str):
    URL = "https://card.wb.ru/cards/list?appType=1&curr=rub&dest=-1257786&spp=27&nm={articul}"
    response = requests.get(URL.format(articul=articul))
    
    products = []
    products_dict = response.json()['data']['products']
    for product_dict in products_dict:
        if '__sort' in product_dict:
            product_dict['sort'] = product_dict['__sort']
            del product_dict['__sort']
        
        product_dict['image_url'] = generate_image(product_dict['id'], size="big")
        product_dict['formatted_price'] = format_price(product_dict['salePriceU'])
        products.append(product_dict)
    
    return products

def generate_image(article: int, size: str = "small", type_: str = "image"):
    def generate_image_number():
        if 0 <= vol <= 143:
            return "01"
        elif 144 <= vol <= 287:
            return "02"
        elif 288 <= vol <= 431:
            return "03"
        elif 432 <= vol <= 719:
            return "04"
        elif 720 <= vol <= 1007:
            return "05"
        elif 1008 <= vol <= 1061:
            return "06"
        elif 1062 <= vol <= 1115:
            return "07"
        elif 1116 <= vol <= 1169:
            return "08"
        elif 1170 <= vol <= 1313:
            return "09"
        elif 1314 <= vol <= 1601:
            return "10"
        elif 1602 <= vol <= 1655:
            return "11"
        elif 1656 <= vol <= 1919:
            return "12"
        elif 1920 <= vol <= 2045:
            return "13"
        elif 2046 <= vol <= 2189:
            return "14"
        else:
            return "15"

    try:
        vol = math.floor(int(article) / 1e5)
        part = math.floor(int(article) / 1e3)
    except TypeError:
        return ""
    
    image_number = generate_image_number()

    if type_ == "card":
        return f"https://basket-{image_number}.wbbasket.ru/vol{vol}/part{part}/{article}/info/ru/card.json"
    elif type_ == "seller":
        return f"https://basket-{image_number}.wbbasket.ru/vol{vol}/part{part}/{article}/info/sellers.json"
    if size == "small":
        return f"https://basket-{image_number}.wbbasket.ru/vol{vol}/part{part}/{article}/images/tm/1.jpg"
    elif size == "big":
        return f"https://basket-{image_number}.wbbasket.ru/vol{vol}/part{part}/{article}/images/big/1.jpg"
    else:
        return f"https://basket-{image_number}.wbbasket.ru/vol{vol}/part{part}/{article}/images/tm/1.jpg"

def format_price(price: int) -> str:
    rubles = price // 100
    return "{:,}".format(rubles).replace(",", " ")

def parse_address():
    response = requests.get("https://www.wildberries.ru/webapi/spa/modules/pickups")
    response.json()
    result = []
    pickups = response.json()['value']['pickups']
    for pickup in pickups:
        result.append({
            "address": pickup['address'],
            "id": pickup['id'],
            "coordinates": pickup['coordinates'],  
        })
    return result



