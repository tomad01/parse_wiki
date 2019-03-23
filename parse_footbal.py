import requests
from lxml import html
from bs4 import BeautifulSoup
import pdb
import bs4
import datetime
import pandas as pd

dic = {}
dic['date'] = []
dic['game_type'] = []
dic['adversar'] = []
dic['score_ro'] = []
dic['romania'] = []
dic['score_ad'] = []
dic['location'] = []

months = {'ianuarie':1,
          'februarie':2,
          'martie':3,
          'aprilie':4,
          'mai':5,
          'iunie':6,
          'iulie':7,
          'august':8,
          'septembrie':9,
          'octombrie':10,
          'noiembrie':11,
          'decembrie':12,
          'April':4,
          'March':3,
          'December':12,
          'November':11,
          'October':10,
          'September':9,
          'August':8,
          'January':1,
          'February':2,
          'May':5,
          'June':6,
          'July':7}


#r = requests.get("https://ro.wikipedia.org/wiki/Rezultatele_echipei_na%C8%9Bionale_de_fotbal_a_Rom%C3%A2niei")
#r = requests.get("https://ro.wikipedia.org/wiki/Rezultatele_echipei_na%C8%9Bionale_de_fotbal_a_Rom%C3%A2niei_(1922-1939)")
r = requests.get("https://ro.wikipedia.org/wiki/Rezultatele_echipei_na%C8%9Bionale_de_fotbal_a_Rom%C3%A2niei_(1940-1959)")

content = r.content
soup = BeautifulSoup(content, "html.parser")

tables = soup.find_all('table')
cnt = 0
for my_table in tables:
    cnt += 1
    print ('=============== TABLE {} ==============='.format(cnt))
    rows = my_table.find_all('tr', recursive=True)                  # <-- HERE
    
    for row in rows:
        cells = row.find_all('td', recursive=True)          # <-- HERE
        if len(cells)==5:
            cell = cells[0]
            data = [cc for cc in cell.children]
            if len(data)<1:
                break
            if type(data[1])!=bs4.element.NavigableString:
                datetime_data = cell.find('time').contents[0]
                datetime_data = datetime_data.split()
            else:
                datetime_data = str(data[1]).split()
            
            day = int(datetime_data[0])
            month = months[datetime_data[1]]
            year = int(datetime_data[2])
            dic['date'].append(datetime.date(year,month,day))
            dic['game_type'].append(data[2].contents[0].encode('utf-8'))
            #############################################################
            cell = cells[1]
            foo = cell.find_all('a')
            if len(foo)!=1:                
                left_team = cell.find('b').contents[0]
            else:
                left_team = foo[0].contents[0]
            try:                
                left_team = left_team.strip().encode('utf-8')
            except:
                left_team = left_team.get('alt').encode('utf-8')
            #############################################################
            cell = cells[2]
            score = cell.find('span').find('b').contents[0]
            score = score.split(u"\u2013")
            left_score = int(score[0])
            right_score =int(score[-1])            
            #############################################################
            cell = cells[3]
            foo = cell.find_all('a')
            if len(foo)!=1:                
                right_team = cell.find('b').contents[0]
            else:
                right_team = foo[0].contents[0]
            try:
                right_team = right_team.strip().encode('utf-8')
            except:
                right_team = right_team.get('alt').encode('utf-8')
            left_team = left_team.rstrip('*')
            right_team = right_team.rstrip('*')
            if right_team == 'Rom\xc3\xa2nia':
                dic['romania'].append(right_team)
                dic['adversar'].append(left_team)
                dic['score_ro'].append(right_score)
                dic['score_ad'].append(left_score)                
            elif left_team == 'Rom\xc3\xa2nia':
                dic['romania'].append(left_team)
                dic['adversar'].append(right_team)
                dic['score_ro'].append(left_score)
                dic['score_ad'].append(right_score)                
            else:
                pdb.set_trace()
            #############################################################
            cell = cells[4]
            
            foo = cell.find_all('a')
            
            if len(foo)>0:                
                last = foo[-1]
                dic['location'].append(last.contents[0].strip().encode('utf-8'))
            else:
                dic['location'].append('')


df = pd.DataFrame(dic)
df.to_csv('meciuri_ro3.csv',index=False)
