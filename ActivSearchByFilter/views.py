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
    # for i in activities:
    #     apiUrl = f"https://geocode-maps.yandex.ru/1.x/?apikey={config.api_key}&format=json&geocode={city}, {i['location']}"
    #     print(apiUrl)
        
    #     response =  requests.get(apiUrl).json()
    #     point = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']
    #     point_a = point['pos'].split()
    #     i['lon'] = point_a[0]
    #     i['lan'] = point_a[1]
    #     time.sleep(1.5)
        
    # for i in activities:
    #     print(i, '\n')

    return [
        {'name': 'Кафе быстрого питания на Большой Полянке', 'location': 'ул. Большая Полянка, 28, строение 3', 'type': 'фастфуд', 'countofvoted': '(1)', 'raiting': '4,0', 'lon': '37.618659', 'lan': '55.736012'},

        {'name': 'Пита-бар Meat Me', 'location': 'ул. Шаболовка, 29к2', 'type': 'фастфуд', 'countofvoted': '(739)', 'raiting': '4,4', 'lon': '37.6107', 'lan': '55.721686'},

        {'name': 'Meat Point', 'location': 'Вознесенский пер., 14', 'type': 'фастфуд', 'countofvoted': '(314)', 'raiting': '4,6', 'lon': '37.605697', 'lan': '55.75899'},

        {'name': 'Nagoya', 'location': 'Старокирочный пер., 16/2с1', 'type': 'фастфуд', 'countofvoted': '(991)', 'raiting': '4,5', 'lon': '37.683976', 'lan': '55.768127'},

        {'name': 'MacGrill', 'location': '1-я Останкинская ул., 55', 'type': 'фастфуд', 'countofvoted': '(24)', 'raiting': '5,0', 'lon': '37.634434', 'lan': '55.824005'},

        {'name': 'Макдоналдс', 'location': 'ул. Арбат, 52с1', 'type': 'фастфуд', 'countofvoted': '(9\xa0438)', 'raiting': '4,3', 'lon': '37.584254', 'lan': '55.747424'},

        {'name': 'Крошка Картошка', 'location': 'ТЦ "Охотный Ряд, Манежная пл., 1с2', 'type': 'фастфуд', 'countofvoted': '(175)', 'raiting': '3,9', 'lon': '37.614608', 'lan': '55.755773'},

        {'name': 'Hesburger', 'location': 'ул. Арбат, 22/2с4', 'type': 'фастфуд', 'countofvoted': '(233)', 'raiting': '4,3', 'lon': '37.593183', 'lan': '55.75015'},

        {'name': 'Теремок', 'location': 'ул. Маросейка, д. 6', 'type': 'фастфуд', 'countofvoted': '(547)', 'raiting': '4,4', 'lon': '37.635332', 'lan': '55.757501'},

        {'name': 'Бол Бол Фуд', 'location': 'Щёлковское ш., д 45а', 'type': 'фастфуд', 'countofvoted': '(180)', 'raiting': '4,3', 'lon': '37.787821', 'lan': '55.810233'},

        {'name': 'City grill', 'location': 'Ленинский пр-т., 2A', 'type': 'фастфуд', 'countofvoted': '(2)', 'raiting': '2,5', 'lon': '37.610988', 'lan': '55.728778'},

        {'name': 'Гриль Бар', 'location': 'Дмитровское шоссе, 25, корп. 1', 'type': 'фастфуд', 'countofvoted': '(1)', 'raiting': '5,0', 'lon': '37.571228', 'lan': '55.825108'},

        {'name': 'KFC', 'location': 'ул, 1-я Тверская-Ямская ул., д. 2', 'type': 'фастфуд', 'countofvoted': '(4\xa0904)', 'raiting': '4,2', 'lon': '37.595501', 'lan': '55.770816'},

        {'name': 'Чебуречная СССР', 'location': 'Большая Бронная ул., 27/4с1', 'type': 'фастфуд', 'countofvoted': '(1\xa0562)', 'raiting': '4,5', 'lon': '37.602759', 'lan': '55.764268'},

        {'name': 'Крошка Картошка', 'location': 'ул. Остоженка, 42', 'type': 'фастфуд', 'countofvoted': '(54)', 'raiting': '4,1', 'lon': '37.594854', 'lan': '55.737583'},

        {'name': 'Макдоналдс', 'location': 'Таганская ул., 1, строение 1', 'type': 'фастфуд', 'countofvoted': '(1\xa0466)', 'raiting': '4,0', 'lon': '37.655894', 'lan': '55.741784'},

        {'name': 'Теремок', 'location': 'Новый Арбат ул., 17', 'type': 'фастфуд', 'countofvoted': '(633)', 'raiting': '4,4', 'lon': '37.590865', 'lan': '55.752055'},

        {'name': 'Кебаб 24', 'location': 'Кожевническая ул., 6', 'type': 'фастфуд', 'countofvoted': '(2)', 'raiting': '4,5', 'lon': '37.643543', 'lan': '55.729726'},

        {'name': 'Idola Turkish Doner', 'location': 'Карманицкий пер., 9', 'type': 'фастфуд', 'countofvoted': '(46)', 'raiting': '4,2', 'lon': '37.583553', 'lan': '55.748326'},

        {'name': 'Макдоналдс', 'location': 'Малая Сухаревская пл., 12', 'type': 'фастфуд', 'countofvoted': '(2\xa0316)', 'raiting': '4,3', 'lon': '37.631505', 'lan': '55.772335'},
            ]


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
