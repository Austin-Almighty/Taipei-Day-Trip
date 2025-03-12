# custom functions that format the JSON file and save its data to MYSQL database

import json
import mysql.connector
import re
from config import config

cnx = mysql.connector.connect(**config)

def read_json(file):
    with open(file, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data["result"]["results"]

def image_urls(string):
    pattern = r"(https.+?(?:\.jpg|\.JPG|\.png|\.PNG))"
    image_urls = re.findall(pattern, string)
    return image_urls

def format_for_sql(file):
    attractions = read_json(file)
    tem = []
    for location in attractions:
        formatted_data = {}
        formatted_data["id"] = location["_id"]
        formatted_data["name"] = location["name"]
        formatted_data["category"] = location["CAT"]
        formatted_data["description"] = location["description"]
        formatted_data["address"] = location["address"]
        formatted_data["transport"] = location["direction"]
        formatted_data["mrt"] = location["MRT"]
        formatted_data["lat"] = location["latitude"]
        formatted_data["lng"] = location["longitude"]
        formatted_data["images"] = image_urls(location["file"])
        tem.append(formatted_data)
    return tem

def write_to_db(file):
    data = format_for_sql(file)
    cursor = cnx.cursor()

    query = """
        INSERT INTO attractions(
            id, name, category, description, address, transport, mrt, lat, lng, images, api
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    for location in data:
        row_id = location.get('id')
        name = location.get('name')
        category = location.get('category')
        description = location.get('description')
        address = location.get('address')
        transport = location.get('transport')
        mrt = location.get('mrt')
        lat = location.get('lat')
        lng = location.get('lng')
        images = json.dumps(location.get('images'))
        api = json.dumps(location)
        
        values = (row_id, name, category, description, address, transport, mrt, lat, lng, images, api)
        cursor.execute(query, values)

    cnx.commit()

file = "data/taipei-attractions.json"
write_to_db(file)



