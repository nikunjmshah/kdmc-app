from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re
# Create your views here.

def index(request):
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    
    browser = wd
    browser.get('https://www.kdmc.gov.in/RtsPortal/CitizenHome.html')
    form_elem = browser.find_element_by_id('frm597')
    #print(form_elem)
    form_elem.submit()
    out = browser.page_source
    #print(out)
    soup = BeautifulSoup(out, 'html.parser')
    divs = soup.findAll("table", {"class": "gridtable"})
    patients_list = []
    for div in divs:
        row = ''
        rows = div.findAll('tr')
    
        for row in rows:        
            if(row.text.find("Today's patients") > -1):
                start = row.text.find("Today's patients")
                start = start
                end = start + 1
                while(row.text[end] != "|"):
                    end += 1
                patients = int(re.search(r'\d+', row.text[start:end]).group())
                #print(row.text[start:end])
                #print(patients)
                patients_list.append(patients)
            if(row.text.find("Todays patients") > -1):
                start = row.text.find("Todays patients")
                start = start
                end = start + 1
                while(row.text[end] != "|" and row.text[end] != "\n"):
                    end += 1
                patients = int(re.search(r'\d+', row.text[start:end]).group())
                #print(row.text[start:end])
                #print(patients)
                patients_list.append(patients)

    r = requests.get('http://httpbin.org/status/418')
    #print("Hello")
    #print(r.text)
    return HttpResponse('<pre>' + str(patients_list) + '</pre>')



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
