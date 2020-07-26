from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re
import os
# Create your views here.

def chart(data):
	data.reverse()
	data_new = [['Day', 'Cases']]
	for k in range(0, len(data)):
		data_new.append([k + 1, data[k]])

	html_page = '''
  <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable(''' + str(data_new) + ''');

        var options = {
          title: 'KDMC Daily cases',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 900px; height: 500px"></div>
  </body>
</html>


	'''
	return(html_page)

def index(request):
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
    
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
    # return HttpResponse('<pre>' + str(patients_list) + '</pre>')
    return HttpResponse(chart(patients_list))



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
