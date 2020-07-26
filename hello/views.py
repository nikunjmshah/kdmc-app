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
	html_page = '''
	<html>
	<body>

	<h1>Chart</h1>

	<div id="linechart"></div>
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script> 

	<script type="text/javascript">

	google.charts.load('current', {packages: ['corechart', 'line']});
	google.charts.setOnLoadCallback(drawLineColors);

	function drawLineColors() {
	      var data = new google.visualization.DataTable();
	      data.addColumn('number', 'X');
	      data.addColumn('number', 'Dogs');
	      data.addColumn('number', 'Cats');

	      data.addRows([
	        [0, 0, 0],    [1, 10, 5],   [2, 23, 15],  [3, 17, 9],   [4, 18, 10],  [5, 9, 5],
	        [6, 11, 3],   [7, 27, 19],  [8, 33, 25],  [9, 40, 32],  [10, 32, 24], [11, 35, 27],
	        [12, 30, 22], [13, 40, 32], [14, 42, 34], [15, 47, 39], [16, 44, 36], [17, 48, 40],
	        [18, 52, 44], [19, 54, 46], [20, 42, 34], [21, 55, 47], [22, 56, 48], [23, 57, 49],
	        [24, 60, 52], [25, 50, 42], [26, 52, 44], [27, 51, 43], [28, 49, 41], [29, 53, 45],
	        [30, 55, 47], [31, 60, 52], [32, 61, 53], [33, 59, 51], [34, 62, 54], [35, 65, 57],
	        [36, 62, 54], [37, 58, 50], [38, 55, 47], [39, 61, 53], [40, 64, 56], [41, 65, 57],
	        [42, 63, 55], [43, 66, 58], [44, 67, 59], [45, 69, 61], [46, 69, 61], [47, 70, 62],
	        [48, 72, 64], [49, 68, 60], [50, 66, 58], [51, 65, 57], [52, 67, 59], [53, 70, 62],
	        [54, 71, 63], [55, 72, 64], [56, 73, 65], [57, 75, 67], [58, 70, 62], [59, 68, 60],
	        [60, 64, 56], [61, 60, 52], [62, 65, 57], [63, 67, 59], [64, 68, 60], [65, 69, 61],
	        [66, 70, 62], [67, 72, 64], [68, 75, 67], [69, 80, 72]
	      ]);

	      var options = {
	        hAxis: {
	          title: 'Day'
	        },
	        vAxis: {
	          title: 'Cases'
	        },
	        colors: ['#a52714', '#097138']
	      };

	      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	      chart.draw(data, options);
	    }
	</script>
	</body>
	<html>        
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
