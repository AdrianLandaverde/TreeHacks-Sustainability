import requests
import json

def get_google_api():
    with open("secrets.json", 'r') as file:
        keys = json.load(file)
    return keys["GOOGLE_API_KEY"]

def get_open_ai_api():
    with open("app/secrets.json", 'r') as file:
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