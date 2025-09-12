import requests
import tkinter as t
import wikipedia
import datetime
from datetime import date
import diskcache as dc
from googlesearch import search
from bs4 import BeautifulSoup
today = date.today()
base = t.Tk()
base.title("Research Bot v1.0")
heading = t.Label(base, text="Research Bot", font = ('Sans',30))
heading.grid(row = 0,column= 4)
inpt = t.Entry(base, text = 'Enter Question')
inpt.grid(row=3,column=4)
lbl = t.Text(base,font = ('Sans',8),wrap = 'word')
lbl.grid(row=6,column=4)
year = today.year
topic = ''
month = today.month
if len(str(month)) == 1: month = f'0{month}'
day = today.day
value = f"{day}/{month}/{year}"
cache = dc.Cache('tushar_ai')
def restart():
    if input("Do you have anymore questions?").lower() == 'yes':
        start()
_ = '_'
def search_by(filter):
    y = 0
    if filter.lower() == 'date':
        filter_date = input("Enter date (DD/MM/YYYY): ")
        try:
            day, month, year = map(int, filter_date.split('/'))
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY.")
            return
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
#re_send = ''
#def yes():
    #re_send = 'yes'
#def no():
    #re_send = 'no'
#expand = t.Button(base , text = 'Expand',command = yes)
#n_expand = t.Button(base,text = 'Next Search',command = no)
def conduct_search():
    topic = inpt.get()
    num_results = 3
    key = topic
    results = []
    try:
        for search2 in search(topic, num_results=3, unique='true'):
            page = requests.get(search2)
            lbl.config(text='Searching...')
            if page.status_code != 200:
                num_results += 1
                continue
            print("Data retrieved")
            print(search2)
            soup = BeautifulSoup(page.text, 'html.parser')
            paragraphs = soup.find_all("p")[0:3]
            for p in paragraphs:
                p_text = p.get_text()
                print(p_text)
                results.append(p_text)
            print(search2)
            print("")
            print("___________________________________________________________________________")
            print("")
        if results:
            value = f"{day}/{month}/{year} : {value}:\n" + "\n".join(results)
        else:
            print('Failed to retrieve data')
            print("Wikipedia - ")
            value = f"{day}/{month}/{year} : {wikipedia.summary(topic)} : From Wikepedia"
    except Exception:
        print('Failed to retrieve data')
        print("Wikipedia - ")
        value = wikipedia.summary(topic)
    lbl.delete(1.0, t.END)
    lbl.insert(1.0, value)
    cache[key] = value
sumbit = t.Button(base, text = 'Search', command = conduct_search)
sumbit.grid(row = 4,column = 4)
base.mainloop()
purpose = input("Update or Access Data: ").lower()
if purpose == 'update':
    for key in cache:
        info_check = cache[key]
        f_date = date.today()
        date_str_2 = info_check[0:10]
        print(date_str_2)
        day1, month1, year1 = map(int, date_str_2.split('/'))
        date1 = date(year1, month1, day1)
        diff =  date.today()-date1
        if diff.days > 500:
            cache.delete(key)
            cache[key] = conduct_search(key)            
elif purpose == 'access data':
    start()
else: print("INVALID OPERATION")
_ = '_'



