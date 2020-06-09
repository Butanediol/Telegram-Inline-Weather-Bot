import requests
import json

location_api = "https://restapi.amap.com/v3/geocode/regeo"

def get_location(longitude, latitude, key):
	params = {
		"key": key,
		"location": str(longitude) + "," + str(latitude)
	}

	r = requests.get(location_api, params=params)
	loaded = json.loads(r.text)
	return loaded["regeocode"]["addressComponent"]["adcode"]