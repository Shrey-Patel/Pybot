# -*- coding: utf-8 -*-
from utilities.GeneralUtilities import print_say
from colorama import Fore
import json
import mapps
import requests
from utilities.dateTime import WeekDay


def main(self, s):
    cmd_key_words = ['check', 'weather', 'forecast', 'in', 'for']
    cmd_words = s.strip().split()
    # location will be defined by the words given that are not the key words
    location = ' '.join(filter(lambda word: word.lower()
                               not in cmd_key_words, cmd_words)).strip()

    current_location = mapps.get_location()

    # if no location is given, use the current location
    if not location:
        location = "{},{}".format(
            current_location['city'], current_location['country_code'])
    country = current_location['country_name']

    # If country is not US, shows weather in Celsius
    units = {
        'url_units': 'metric',
        'str_units': 'ºC'
    }
    # If country is US, shows weather in Fahrenheit
    if country == 'United States':
        units = {
            'url_units': 'imperial',
            'str_units': 'ºF'
        }

    send_url = (
        "http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&cnt={1}"
        "&APPID=ab6ec687d641ced80cc0c935f9dd8ac9&units={2}".format(
            location, '7', units['url_units'])
    )

    r = requests.get(send_url)
    j = json.loads(r.text)

    week_from_today = WeekDay().get_week_from_today()

    try:
        print_say(
            "Weather forecast in {} for the next 7 days.".format(
                j['city']['name'].title()
            ),
            self,
            Fore.BLUE
        )
        for cnt, day_dict in enumerate(j['list']):
            print_say("{}:".format(week_from_today[cnt]), self, Fore.BLUE)
            print_say("\tWeather: {}".format(
                day_dict['weather'][0]['main']), self, Fore.BLUE)
            print_say(
                "\tMax temperature: {} {}".format(
                    round(day_dict['temp']['max'], 1), units['str_units']),
                self,
                Fore.BLUE
            )
            print_say(
                "\tMin temperature: {} {}\n".format(

                    round(day_dict['temp']['min'], 1), units['str_units']),
                self,
                Fore.BLUE
            )
    except KeyError:
        print_say("The forecast information could not be found.", self, Fore.RED)
