import weather
import logging
import loc
import json
import argparse
from uuid import uuid4
from rich.logging import RichHandler
from telegram import ParseMode, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram.ext.dispatcher import run_async

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("log")

parser = argparse.ArgumentParser(description="Launch telegram inline weather bot.")
parser.add_argument("-c", "--cache-time", type=int, default=300, help="Set telegram server cache time, default is 300 seconds.")
parser.add_argument("-k", "--key", type=str, default="6a43d91d6d0243f6a0eb3d24f38fdba5", help="Amap API key.")
parser.add_argument("token", nargs=1, help="You must provide a telegram bot token.")
args = parser.parse_args()

def at(t, v, rh):
	"""
	Apparent tempreature formula.
	:params t: float, celcius temperature
	:params v: float, wind of speed
	:params rh: float, relative 
	"""
	return 0.7*t + 0.2*(rh/100 * 6.105 * math.exp((1.27*t)/(237.7+t))) - 0.65*v - 2.7

def pre_parse(text):
	text = text.replace('(','\\(')
	text = text.replace(')','\\)')
	text = text.replace('*','\\*')
	text = text.replace('-','\\-')
	text = text.replace('!','\\!')
	text = text.replace('[','\\[')
	text = text.replace(']','\\]')
	text = text.replace('.','\\.')
	text = text.replace('|','\\|')
	text = text.replace('_','\\_')
	text = text.replace('+','\\+')
	return text

@run_async
def inline_weather(update, context):
	location = update.inline_query.location
	results = []
	if location:
		query = loc.get_location(location.longitude, location.latitude, args.key)
	else:
		results.insert(0,
			InlineQueryResultArticle(
				id=uuid4(),
				title="⚠️ 没有获取到您的位置。",
				input_message_content=InputTextMessageContent(
					pre_parse("本 Bot 不储存您的位置信息，请放心使用。"), parse_mode=ParseMode.MARKDOWN_V2)))

		update.inline_query.answer(results, cache_time=300)
		return False

	live_weather = weather.get_weather(query)

	reply = ''
	reply = reply + "天气：" + live_weather.weather
	reply = reply + "\n温度：" + live_weather.temperature + "℃"
	reply = reply + "\n风向：" + live_weather.winddirection + "风"
	reply = reply + "\n风力：" + live_weather.windpower + " 级"
	reply = reply + "\n湿度：" + live_weather.humidity + "%"
	reply = reply + "\n体感温度：" + live_weather.humidity
	reply = reply + "\n发布时间：" + live_weather.reporttime

	results.insert(0,
	    InlineQueryResultArticle(
	        id=uuid4(),
	        title="仅显示城区",
	        input_message_content=InputTextMessageContent(
	            pre_parse("城区：" + live_weather.city + "\n" + reply), parse_mode=ParseMode.MARKDOWN_V2)))

	results.insert(0,
	    InlineQueryResultArticle(
	        id=uuid4(),
	        title="显示省/地区和城区",
	        input_message_content=InputTextMessageContent(
	            pre_parse("省区：" + live_weather.province + "\n" + "城区：" + live_weather.city + "\n" + reply), parse_mode=ParseMode.MARKDOWN_V2)))

	results.insert(0,
	    InlineQueryResultArticle(
	        id=uuid4(),
	        title="仅显示省/地区",
	        input_message_content=InputTextMessageContent(
	            pre_parse("省区：" + live_weather.province + "\n" + reply), parse_mode=ParseMode.MARKDOWN_V2)))

	results.insert(0,
	    InlineQueryResultArticle(
	        id=uuid4(),
	        title="屏蔽位置",
	        input_message_content=InputTextMessageContent(
	            pre_parse(reply), parse_mode=ParseMode.MARKDOWN_V2)))

	update.inline_query.answer(results, cache_time=args.cache_time)

def main():
	updater = Updater(token=args.token, use_context=True)
	dp = updater.dispatcher

	weather_handler = InlineQueryHandler(inline_weather)
	dp.add_handler(weather_handler)

	updater.start_polling()

if __name__ == "__main__":
	main()