import json
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pickle
import config
import time


dictTranslate = { #TODO вынести в конфиг
    'onplace' : 'аэропорт',
    'hotel': 'отель',
    'entertainment' : 'развлечения',
    'entertainment_kidfriendly': 'развлечения можно с детьми',
    'eat': 'cafe restoran fastfood',
    'interestingPlaces': 'интересные места',
}


def getLikedActivitiesAsIt():

    pass

def getLikedActivitiesWithTime(hours):

    pass

def getLatLong(activities, city):
    apiUrl = ''
    for i in activities:
        apiUrl = f"https://geocode-maps.yandex.ru/1.x/?apikey={config.api_key}&format=json&geocode={city}, {i['location']}"
        print(apiUrl)
        
        response =  requests.get(apiUrl).json()
        point = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']
        point_a = point['pos'].split()
        i['lon'] = point_a[0]
        i['lan'] = point_a[1]
        time.sleep(1.5)
        
    for i in activities:
        print(i, '\n')

    return activities


def parseActivities(activities, city):
    parsedActivities = []

    options = Options()
    options.add_argument("--lang=ru")
    driver = webdriver.Chrome(chrome_options=options)

    if 'entertainment_kidfriendly' in activities:
        activities.remove('entertainment')

    qString = f'https://www.google.it/maps/search/{city}+';

    for activitie in activities:
        tempURL = f'{qString}{dictTranslate.get(activitie)}/data=!4m4!2m3!5m1!4e1!6e5'
        driver.get(tempURL)
        wait = WebDriverWait(driver, 10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')


        p_names = soup.find_all('h3', {'class' : 'section-result-title', 'jsan': '7.section-result-title'}) #TODO RERELIS! do not use on proda
        s_raiting = soup.find_all('span', {'class' : 'cards-rating-score'})
        c_raiting = soup.find_all('span', {'class' : 'section-result-num-ratings'})
        name = soup.find_all('span', {'class' : 'section-result-details'})
        location = soup.find_all('span', {'class' : 'section-result-location'})
        #hourswork = soup.find_all('span', {'class' : ['section-result-info section-result-opening-hours', 'section-result-info section-result-closed']})

        for i in range(len(p_names)):
            print(f'Название: {p_names[i].text}\nРейтинг: {s_raiting[i].text}\nКол-во голосов: {c_raiting[i].text}\nТип: {name[i].text}\nАдрес: {location[i].text}\n-------')
            parsedActivities.append({
                'name': p_names[i].text,
                'location': location[i].text,
                'type': name[i].text,
                'countofvoted': c_raiting[i].text,
                'raiting': s_raiting[i].text,
            })

        print(parsedActivities)
        break # во время тестов зря не обращаться к гуглу

    return parsedActivities

@csrf_exempt 
def index(request):
    if request.method == "POST":
        json_request = json.loads(request.body)
        print(json_request)
        parsedActivities = parseActivities(json_request['activList'], json_request['cityName'])
        finalInfo = getLatLong(parsedActivities, json_request['cityName'])
        response_data = {
            'data': finalInfo,
        }
        return JsonResponse(response_data)
    

# Create your views here.
