![A complete mess](https://github.com/Butanediol/Telegram-Inline-Weather-Bot/blob/master/media/1.jpg?raw=true)

# Telegram Inline Weather Bot

~~又~~一个在 Inline 中查询天气的 Telegram Bot。（因为全局搜索能搜到的都挂掉了。）基于 [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)。

使用了高德地图的 Regeo 和 Weather API。（因此仅支持中国大陆和港澳台地区）

一个运行中的实例：[@inline_weather_bot](https://t.me/inline_weather_bot)。

# 用法

## 安装 Requirements

`pip(3) install python-telegram-bot rich`

## 运行

你需要：
- 一个 Telegram Bot Token
- 一台运行 Bot 的设备

```
usage: bot.py [-h] [-c CACHE_TIME] [-k KEY] token

Launch telegram inline weather bot.

positional arguments:
  token                 You must provide a telegram bot token.

optional arguments:
  -h, --help            show this help message and exit
  -c CACHE_TIME, --cache-time CACHE_TIME
                        Set telegram server cache time, default is 300
                        seconds.
  -k KEY, --key KEY     Amap API key.
```

例如：

`python(3) bot.py 123456789:abcdefghijklmnopqrstuvwxyzABCDEFGHI`

