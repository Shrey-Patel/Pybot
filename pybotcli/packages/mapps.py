# -*- coding: utf-8 -*-
import json
import webbrowser
import requests
from colorama import Fore

location = 0


def get_location():
    global location
    if not location:
        print("Getting Location ... ")
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        location = json.loads(r.text)
    return location


def directions(to_city, from_city=0):
    if not from_city:
        from_city = get_location()['city']
    url = "https://www.google.com/maps/dir/{0}/{1}".format(from_city, to_city)
    webbrowser.open(url)


def locate_me():
    hcity = get_location()['city']
    print(Fore.BLUE + "You are at " + hcity + Fore.RESET)


def weather(city=None):
    if not city:
        city = get_location()['city']

    # Checks country
    country = get_location()['country_name']

    # If country is US, shows weather in Fahrenheit
    if country == 'United States':
        send_url = (
            "http://api.openweathermap.org/data/2.5/weather?q={0}"
            "&APPID=ab6ec687d641ced80cc0c935f9dd8ac9&units=imperial".format(
                city)
        )
        unit = ' ºF in '

    # If country is not US, shows weather in Celsius
    else:
        send_url = (
            "http://api.openweathermap.org/data/2.5/weather?q={0}"
            "&APPID=ab6ec687d641ced80cc0c935f9dd8ac9&units=metric".format(
                city)
        )
        unit = ' ºC in '
    r = requests.get(send_url)
    j = json.loads(r.text)

    # check if the city entered is not found
    if 'message' in j and j['message'] == 'city not found':
        print(Fore.BLUE + "City Not Found" + Fore.RESET)
        return False

    else:
        temperature = j['main']['temp']
        description = j['weather'][0]['main']
        print(Fore.BLUE + "It's " + str(temperature) + unit +
              str(city) + " (" + str(description) + ")" + Fore.RESET)

    return True


def search_near(things, city=0):
    if city:
        print(Fore.GREEN + "Hold on!, I'll show " + things +
              " near " + city + Fore.RESET)
        url = "https://www.google.com/maps/search/{0}+{1}".format(things, city)
    else:
        print(Fore.GREEN + "Hold on!, I'll show " +
              things + " near you" + Fore.RESET)
        url = "https://www.google.com/maps/search/{0}/@{1},{2}".format(
            things, get_location()['latitude'], get_location()['longitude'])
    webbrowser.open(url)
