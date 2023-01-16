from bs4 import BeautifulSoup
import requests

from .config_parser import ConfigParser


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
    return int(bs.find('div', {'class': 'temp'}).text.strip()[:-2])
