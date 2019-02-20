import pandas as pd
from bs4 import BeautifulSoup

from django.shortcuts import render


# Create your views here.
def merge_fields(df):
    def remove_nan():
        soup = BeautifulSoup(df, 'lxml')
        soup = soup.find('tbody')
        
        move_on = (x for x in soup.find_all('tr'))
        go = True
        question = next(move_on).find_all('td')[0].text
        while go:
            count = 1
            next_question = next(move_on).find_all('td')[0].text
            while next_question == 'NaN':
                count += 1
                try:
                    next_question = next(move_on).find_all('td')[0].text
                except StopIteration:
                    next_question = None
                    go = False
            yield question, count
            question = next_question

    df2 = df
    
    for question, count in remove_nan():
#         print('<td>{0}</td>'.format(question).replace('<td>{0}</td>'.format(question), '<td rowspan="{1}">{0}</td>'.format(question, count)))
        df2 = df2.replace('<td>{0}</td>'.format(question), '<td rowspan="{1}">{0}</td>'.format(question, count))
        df2 = df2.replace('<td>NaN</td>', '')
    return df2


def data(request, name):
    if name == 'Coding Key':
        header = [0]
    else:
        header = [0, 1]

    dfs = pd.read_excel(r'C:\Users\CTMayers\Desktop\Research Toolkit\Creating Reports\Python\Deliverables\Raw Data.xlsx', header=header, sheet_name=None)
    
    dfs['Coding Key'] = dfs['Coding Key'].rename(columns={'Unnamed: 1':'', 'Unnamed: 2':''})
    dfs['Coding Key'] = dfs['Coding Key'].iloc[1:]
    
    df = dfs[name].to_html(index=False).replace('<thead>', '<thead style = "background-color: gray">')

    if name == 'Coding Key':
        df = df.replace('<th></th>\n', '')
        # df = df.replace('<td>Values</td>\n      <td>NaN</td>\n      <td>Labels</td>', '<th style="background-color: gray" colspan="2" style="text-align: center;">Values</th>\n<th style="background-color: gray">Labels</th>')
        df = df.replace(' <th>Variable Values', '<th colspan="3" style="text-align: center;">Variable Values')
        df = merge_fields(df)

    return render(
        request,
        'raw_data/raw.html',
        {
            'title': 'Hello, Django',
            'content': df,
        }
    )


def main2(request):
    import sys
    sys.path.append(r'C:\Users\CTMayers\Desktop\Research Toolkit\Creating Reports\Python')
    import Report

    
    main = Report.CESS(r'C:\Users\CTMayers\Desktop\Research Toolkit\Creating Reports\Python\Files\Working Files\California+Lutheran+University+2018+CESS_November+25%2C+2018_18.29.csv', 'California Lutheran University')

    

    data = {}
    for i, j in main.run_report():
        data[i] = j.to_html()
    
    context = {
        'data': data
    }
    
    return render(request, "raw_data/index.html", context)