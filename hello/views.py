from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

from bs4 import BeautifulSoup
import sys
import re
import os
import time
import mechanize
# Create your views here.

def chart(data):
	data.reverse()
	data_new = [['Day', 'Cases']]
	for k in range(0, len(data)):
		data_new.append([k + 1, data[k]])

	html_page = '''
  <html>
  <head>
  <h1> KDMC Analysis </h1>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable(''' + str(data_new) + ''');

        var options = {
          title: 'KDMC Daily cases',
          curveType: 'function',
          legend: { position: 'bottom' },
          hAxis: {
          title: 'Cases'
          },
          vAxis: {
          title: 'Day'
          }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 900px; height: 500px"></div>



	'''
	return(html_page)


def index(request):
    start = time.time()
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('https://www.kdmc.gov.in/RtsPortal/CitizenHome.html#')
    br.select_form(name='frm597')
    page = br.submit()
    
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

    html_page = chart(patients_list)
    end = time.time()
    
    return HttpResponse(html_page + '<p>' + str(end - start) + '</p></body</html>')



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
