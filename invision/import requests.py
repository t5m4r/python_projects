import requests
import datetime
from datetime import date
import diskcache as dc
from googlesearch import search
from bs4 import BeautifulSoup
cache = dc.Cache('tushar_ai')
def restart():
    if input("Do you have anymore questions?").lower() == 'yes':
        start()
_ = '_'
def search_by(filter):
    y = 0
    if filter.lower() == 'date':
        filter_date = input("Enter date (DD/MM/YYYY)")
        for key in cache:
            data = cache[key]
            if data[0:10] == filter_date:
                y += 1
                print(f'{y}) {key}')
                print('____________________________________________')
                print(data)
    elif filter == 'content':
        content = input("Enter Search word / phrase: ")
        for key in cache:
            data = cache[key]
            dat = f'{data}'.lower()
            if content.lower() in dat:
                y += 1
                print(f'{y}) {key}')
                print('____________________________________________')
                print(data)
    restart()
def start():
    today = date.today()
    year = today.year
    month = today.month
    if len(str(month)) == 1: month = f'0{month}'
    day = today.day
    value = f"{day}/{month}/{year}"
    num_results = 3
    choice = input("Select filter option (Date,Content,Question) ")
    if choice.lower() == 'date'or choice.lower() ==  'by date':
        search_by('date')
    elif choice.lower() == 'content' or choice.lower() ==  'by content':
        search_by('content')
    elif choice.lower() == 'question':
        topic = input ("ENTER QUESTION: ").lower()
        print()
        key = (topic)
        print(key)
        if key in cache:
            print("In cache")
            print(cache[key])
        else:
            print("Not in cache")
            print()
            print()
            for search2 in search(f'{topic}',num_results = num_results,unique='true'):
                re_send = 'N'
                page = requests.get(search2)
                if page != 200:
                    num_results +=1
                else:
                    print("Data retrieved")
                    print(search2) 
                soup = BeautifulSoup(page.text, 'html.parser')
                paragraphs = soup.find_all("p")
                for p in paragraphs:
                    p = p.get_text()
                    print(p)
                    value = f'{value}: {p}'
                re_send = input('Expand? (Y) or (N)')
                if re_send.lower() == 'y':
                    paragraphs = soup.find_all("p")[0:5]
                    print(search2)
                    for p in paragraphs:
                        p = (p.get_text())
                        print(p)
                        value = f'{value}: {p}'
                print("")
                print("___________________________________________________________________________")
                print("")
            cache[key] = value
            restart()
    else: print("INVALID OPTION")
start()

