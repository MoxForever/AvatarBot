from enum import Enum


class WeatherInfo(Enum):
    sun = 1
    rain = 2
    fog = 3
    cloud = 4
    smog = 5

    @staticmethod
    def get(data: str):
        f_data = data.strip().lower()
        if "ясно" in f_data:
            return WeatherInfo.sun
        elif "солнечно" in f_data:
            return WeatherInfo.sun
        elif "облачно" in f_data:
            return WeatherInfo.fog
        elif "ливень" in f_data:
            return WeatherInfo.rain
        elif "дождь" in f_data:
            return WeatherInfo.rain
        elif "смог" in f_data:
            return WeatherInfo.smog

        return None


class Weather:
    def __init__(self, temp: int, weather: WeatherInfo, raw = None):
        self.temp = temp
        self.weather = weather
        self.raw = raw
