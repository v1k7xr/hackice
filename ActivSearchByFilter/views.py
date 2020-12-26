import json
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait



dictTranslate = { #TODO вынести в конфиг
    'onplace' : 'аэропорт',
    'hotel': 'отель',
    'entertainment' : 'развлечения',
    'entertainment_kidfriendly': 'развлечения можно с детьми',
    'eat': 'покушать',
    'interesting_places': 'интересные места',
}

def parseActivities(activities, city):
    options = Options()
    options.add_argument("--lang=ru")
    driver = webdriver.Chrome(chrome_options=options)

    if 'entertainment_kidfriendly' in activities:
        activities.remove('entertainment')

    qString = f'https://www.google.it/maps/search/{city}+';
    for activitie in activities:
        tempURL = f'{qString}{dictTranslate.get(activitie)}'
        driver.get(tempURL)
        wait = WebDriverWait(driver, 10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ourResult = soup.find_all('div', class_='section-layout section-scrollbox scrollable-y scrollable-show section-layout-flex-vertical')
        print(ourResult)
        break # во время тестов зря не обращаться к гуглу

        print(tempURL)
    pass

@csrf_exempt 
def index(request):
    if request.method == "POST":
        json_request = json.loads(request.body)
        print(json_request)
        parseActivities(json_request['activList'], json_request['cityName'])

        response_data = {}
        return JsonResponse(response_data)
    

# Create your views here.
