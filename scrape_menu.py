import certifi
import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import os
import re
from pymongo import MongoClient



# Including the credentials in the code is not a good practice.Here I am doing this for ease of replication
connection_string="mongodb+srv://21ucs047:42xlsZJGju4lGnzF@cluster0.ql4huew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
dbname = "menu_scraper"
collection_name = "menu"

def extract_menu_items(text):
    # A regular expression to match the dish name and price
    pattern = r'[•\-\s>]+\s*([A-Za-z\s\(\)\']+)\s*[•\-\s>]+\s*(\d+)(?:\n|$)'
    
    matches = re.findall(pattern, text, re.MULTILINE)
    menu_items = []
    
    for match in matches:
        dish = match[0].strip()
        price = match[1]
        menu_items.append({"dish": dish, "price": price})
    
    return menu_items

def store_in_mongodb(menu_items):
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    try:
        db = client[dbname]
        collection = db[collection_name]
        if menu_items:
            try:
                collection.insert_one(menu_items)
            except Exception as e:
                print(f"Error occurred while storing menu items: {e}")
    finally:
        client.close()

def fetch_menu_from_mongodb(restaurant_name):
    client = MongoClient(connection_string,tlsCAFile=certifi.where())
    try:
        db = client[dbname]
        collection = db[collection_name]
        menu = collection.find_one({"restaurant_name":restaurant_name})
        
        return menu
    except Exception as e:
         print(f"Error occurred while fetching menu items: {e}")
    finally:
        client.close()

def run(rest_id):
    response = requests.get(f"https://www.dineout.co.in{rest_id}/menu")
    soup = BeautifulSoup(response.content, 'html.parser')

    restaurant_name = soup.find('h1', {'class': 'restnt-name'}).find('a').text.strip().replace(' ', '')
    fetched_menu=fetch_menu_from_mongodb(restaurant_name)
    if(fetched_menu):
        return fetched_menu
    try:
        menu_images = soup.find('section' ,{'class':'menu-wrapper'}).find_all('a')
        print(len(menu_images))
        menu={}
        menu['restaurant_name']=restaurant_name
        for i, image in enumerate(menu_images):
            print(i)
            image_url = image['data-med']
            response = requests.get(image_url)
            file_path=f"menu_images/{restaurant_name}_{i}.jpg"
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)   
            text = pytesseract.image_to_string(Image.open(f"menu_images/{restaurant_name}_{i}.jpg"))
            menu_items = extract_menu_items(text)
            menu[f"page{i+1}"]=menu_items
        store_in_mongodb(menu)
        fetched_menu=fetch_menu_from_mongodb(restaurant_name)
        return fetched_menu
    except Exception as e:
        print(f"Error occurred while extracting menu items: {e}")
    


def fetch_restaurant_name(query):
    response = requests.get(f"https://www.dineout.co.in/mumbai-restaurants/?search_str={query}")
    soup = BeautifulSoup(response.content, 'html.parser')
    if(soup.find('h2') and soup.find('h2').text=='Food not found'):
        return ''
    res=soup.find('div', {'class': 'restnt-detail'})
    rest_id=res['data-link']
    return rest_id

