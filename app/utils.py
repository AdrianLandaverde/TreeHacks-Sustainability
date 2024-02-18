import requests
import json
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image 
import pytesseract

def get_google_api():
    with open("secrets.json", 'r') as file:
        keys = json.load(file)
    return keys["GOOGLE_API_KEY"]

def get_open_ai_api():
    with open("secrets.json", 'r') as file:
        keys = json.load(file)
    return keys["OPEN_AI_API_KEY"]

def get_coordinates(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    parameters = {
        'address': address, 
        'key': get_google_api(),
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'OK':
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']
        else:
            print(f'Error: {data["status"]}')
    else:
        print(f'Request failed with status code: {response.status_code}')
    
    return {'lat': lat, 'lon': lon}

def get_green_restaurants(address):

    coordinates = get_coordinates(address)
    lat = coordinates['lat']
    lon = coordinates['lon']

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'keyword': 'sustainable veggie plant-based',
        'location': f"{lat},{lon}",
        'radius': 1500,
        'type': 'restaurant',
        'key': get_google_api(),
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # The request was successful
        data = response.json()
        # Process the response data as needed
        print("Ok")
    else:
        # There was an error with the request
        print(f"Error: {response.status_code}, {response.text}")

    address= data['results'][0]['vicinity']
    name= data['results'][0]['name']

    complete= address + name
    swap = complete.replace(" ", "+")
    main_map= f"https://www.google.com/maps/embed/v1/place?key={get_google_api()}&q={swap}"
    
    results= []

    for i in range(min([len(data["results"]), 9])):
        results.append(data["results"][i]["name"] + " " + data["results"][i]["vicinity"])

    base_link= f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=13&size=600x400"
    markers=""
    for i in range(min([len(data["results"]), 9])):
        temp_lat=data["results"][i]["geometry"]["location"]["lat"]
        temp_lon=data["results"][i]["geometry"]["location"]["lng"]
        marker= f"&markers=color:green%7Clabel:{i+1}%7C{temp_lat},{temp_lon}"
        markers+= marker
    link= base_link+markers+"&key="+get_google_api()

    return {'names': results, 'main_map': main_map, 'static_map': link}

def route_map(origin, destination, mode):
    link= f"""https://www.google.com/maps/embed/v1/directions?key={get_google_api()}&origin={origin}&destination={destination}&mode={mode.lower()}"""
    return link

def RAG_planet(place:str, question:str):

    chroma_client = chromadb.PersistentClient(path="Chromadb/")
    SentenceTransformerEmbeddings= embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
    collection= chroma_client.get_collection("EarthVoice", embedding_function=SentenceTransformerEmbeddings)

    dict_places={"Amazon Rain Forest": "data/amazon.md", "Mesoamerican Reef": "data/mesoamerican_reef.md",
                "Northern Great Plains": "data/northern_great_plains.md", "Chihuahuan Dessert":"data/chihuahuan_dessert.md", "Galapagos":"data/galapagos.md", 
                "Pantanal":"data/pantanal.md", "Southern Chile":"data/southern_chile.md",
                "Amur Heilong":"data/amur_heilong.md", "Arctic":"data/arctic.md", "Atlantic Forest":"data/atlantic_forest.md",
                "Coastal East Africa":"data/coastal_east_africa.md", "Congo Basin":"data/congo_basin.md", 
                "Coral Triangle":"data/coral_triangle.md", "Eastern Himalayas":"data/eastern_himalayas.md",
                "Greater Mekong":"data/greater_mekong.md", "Madagascar":"data/madagascar.md", 
                "Namibia":"data/namibia.md", "Yagtze":"data/yangtze.md"
                }
    

    file= dict_places[place]

    results= collection.query(
        query_texts=[question],
        n_results=10,
        where= {"source":file},
        include= [ "documents" ]
    )

    context= results["documents"][0][0]

    client = OpenAI(api_key= get_open_ai_api())

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a personification of the {place} speaking as the planet. You know this: {context}"},
        {"role": "user", "content": f"""Answer briefly the following question using only the following context. If it is not related to the {place}, you don't know the anser and it doesn't come in the context, you can skip it. 
        
        QUESTION: {question}"""},
    ]
    )

    return {"Question": question, "Context": context, "Answer":completion.choices[0].message.content}

def heatmap_solar_panels(address):
    coordinates = get_coordinates(address)
    lat = coordinates['lat']
    lon = coordinates['lon']

    url = "https://solar.googleapis.com/v1/dataLayers:get"
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "radiusMeters": 100,
        "view": "FULL_LAYERS",
        "requiredQuality": "HIGH",
        "pixelSizeMeters": 0.5,
        "key": get_google_api()
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Request was successful
        data = response.json()
        print(data)
    else:
        # Request failed
        print(f"Error: {response.status_code}, {response.text}")

    print(data)
    urls_base= ["rgbUrl", "maskUrl", "annualFluxUrl"]
    for url_base in urls_base:
        url_map= data[url_base]
        url_map+= "&key="+get_google_api()
        response = requests.get(url_map)
        if response.status_code == 200:
            # Request was successful
            # Assuming the response is a binary file, you might want to save it
            with open(url_base+".tif", "wb") as f:
                f.write(response.content)
            print("File saved successfully.")
        else:
            # Request failed
            print(f"Error: {response.status_code}, {response.text}")

    geotiff_path = 'rgbUrl.tif'

    # Open the GeoTIFF file
    dataset = rasterio.open(geotiff_path)
    data_r = dataset.read(1)
    data_g = dataset.read(2)
    data_b = dataset.read(3)
    data_rgb = np.dstack((data_r, data_g, data_b))

    geotiff_path = 'maskUrl.tif'
    dataset = rasterio.open(geotiff_path)
    data_mask = dataset.read(1) 
    complement_mask = 1 - data_mask

    broadcasted_complement_mask = np.expand_dims(complement_mask, axis=-1)

    masked_image = data_rgb * broadcasted_complement_mask
    masked_image_norm = masked_image / 255.0

    # Path to your GeoTIFF file
    geotiff_path = 'annualFluxUrl.tif'

    # Open the GeoTIFF file
    dataset = rasterio.open(geotiff_path)
    data_heat = dataset.read(1)
    cmap_hot = plt.get_cmap('hot')
    norm = mcolors.Normalize(vmin=data_heat.min(), vmax=data_heat.max())
    data_hot = cmap_hot(norm(data_heat))
    data_hot= data_hot[:, :, :3]

    geotiff_path = 'maskUrl.tif'
    dataset = rasterio.open(geotiff_path)
    data_mask = dataset.read(1) 

    broadcasted_mask = np.expand_dims(data_mask, axis=-1)
    broadcasted_mask
    data_hot_final = data_hot * broadcasted_mask

    image_final= np.array((masked_image_norm + data_hot_final)*255, dtype=np.uint8)
    return image_final

def get_label_info(image_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = image_path

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    print(text)

    client = OpenAI(api_key= get_open_ai_api())

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """You are an expert in sustainable fashion. You know this about materials: 
            - High carbon efficiency: Linen, Hemp
            - Mid-level carbon efficiency: Carbon, Wool, Denim, Silk
            - Low carbon efficiency: Polyester, Rayon, Nylon 
        """},
        {"role": "user", "content": f"""Classify into one of this categories (High carbon efficiency, Mid-level carbon efficiency, Low carbon efficiency) the following label of the cloth. Based on the percentages and classification, give a rating from 1 (low efficiency) to 10 (high efficiency).   
        
        LABEL: {text}"""},
    ]
    )

    # Return the text
    return completion.choices[0].message.content