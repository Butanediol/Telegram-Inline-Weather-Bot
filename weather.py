import requests
import json

weather_api = "https://restapi.amap.com/v3/weather/weatherInfo"

class LiveWeather(object):
	def __init__(self, **kwargs):
		self.province = kwargs["province"]
		self.city = kwargs["city"]
		self.adcode = kwargs["adcode"]
		self.weather = kwargs["weather"]
		self.temperature = kwargs["temperature"]
		self.winddirection = kwargs["winddirection"]
		self.windpower = kwargs["windpower"]
		self.humidity = kwargs["humidity"]
		self.reporttime = kwargs["reporttime"]

class Forecasts(object):
	def __init__(self, **kwargs):
		self.city = kwargs["city"]
		self.adcode = kwargs["adcode"]
		self.province = kwargs["province"]
		self.reporttime = kwargs["reporttime"]
		self.casts = kwargs["casts"]

class CastWeather(object):
	def __init__(self, **kwargs):
		self.date = kwargs["date"]
		self.week = kwargs["week"]
		self.dayweather = kwargs["dayweather"]
		self.daytemp = kwargs["daytemp"]
		self.nighttemp = kwargs["nighttemp"]
		self.daywind = kwargs["daywind"]
		self.nightwind = kwargs["nightwind"]
		self.daypower = kwargs["daypower"]
		self.nightpower = kwargs["nightpower"]

def get_weather(city, extensions="base", output="JSON"):
	params = {
		"key": "6a43d91d6d0243f6a0eb3d24f38fdba5",
		"city": city,
		"extensions": extensions,
		"output": output
	}

	r = requests.get(weather_api, params=params)
	if extensions == "base":
		return resolve_base_weather(json.loads(r.text))
	if extensions == "all":
		return resolve_all_weather(json.loads(r.text))

def resolve_base_weather(j):
	if not j["status"] == "1":	return False
	if not j["info"] == "OK":	return False
	if not j["infocode"] == "10000":	return False

	count = int(j["count"])
	live_weather = LiveWeather(
		province=j["lives"][0]["province"],
		city=j["lives"][0]["city"],
		adcode=j["lives"][0]["adcode"],
		weather=j["lives"][0]["weather"],
		temperature=j["lives"][0]["temperature"],
		winddirection=j["lives"][0]["winddirection"],
		windpower=j["lives"][0]["windpower"],
		humidity=j["lives"][0]["humidity"],
		reporttime=j["lives"][0]["reporttime"]
		)
	return live_weather

def resolve_all_weather(j):
	if not j["status"] == "1":	return False
	if not j["info"] == "OK":	return False
	if not j["infocode"] == "10000":	return False

	casts = []

	for cast in j["forecasts"][0]["casts"]:
		casts.append(
			CastWeather(
				date = cast["date"],
				week = cast["week"],
				dayweather = cast["dayweather"],
				nightweather = cast["nightweather"],
				daytemp = cast["daytemp"],
				nighttemp = cast["nighttemp"],
				daywind = cast["daywind"],
				nightwind = cast["nightwind"],
				daypower = cast["daypower"],
				nightpower = cast["nightpower"]
				)
			)
	return casts