import sys
import re
import pandas as pd
from bs4 import BeautifulSoup

from django.shortcuts import render

sys.path.append(r'C:\Users\CTMayers\denpython\Reports')
import Report

# Create your views here.
def home(request):
    return render(request, 'reports/home.html')


def reportchoice(request):
    reports = Report.get_reports()
    choices = {k: re.sub(r'\+|_|%2C', ' ', k) for k in reports}
    
    context = {'choices': choices}

    return render(request, 'reports/reportchoice.html', context)


def report(request):
    report = Report.get_reports()
    context = {'report': report}

    return render(request, 'reports/report.html', context)


def main_report(request):
    main = Report.CESS(r'C:\Users\CTMayers\denpython\Reports\Files\Working Files\California+Lutheran+University+2018+CESS_November+25%2C+2018_18.29.csv', 'California Lutheran University')
    data = {}
    for section, frame in main.run_report():
        data[section] = frame
    
    print(data['Q1_IMP'])
    for index, row in data['Q1_IMP'].iterrows():
        for i, j in zip(row.index, row):
            print(i, j)

    # context = {data['Q1_IMP']}
    return render(request, 'reports/main.html')