from bs4 import BeautifulSoup
import requests

from classes import Weather, WeatherInfo
from funcs.config_parser import ConfigParser


def get_weather():
    bs = BeautifulSoup(
        requests.get(
            ConfigParser.get("Data", "accu_weather"),
            headers={
                'User-Agent': ConfigParser.get("Data", "user_agent")
            }
        ).text,
        'html.parser'
    )
    data = bs.find("div", {'class': 'current-weather'})
    return Weather(
        temp=int(data.find('div', {'class': 'temp'}).text.strip()[:-2]),
        weather=WeatherInfo.get(data.find('div', {'class': 'phrase'}).text),
        raw=data
    )
