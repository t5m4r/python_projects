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
lbl = t.Text(base,font = ('Sans',15),wrap = 'word')
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
            print("Starting Google search for your question...")
            found_any = False
            for count, search2 in enumerate(search(f'{topic}', num_results=num_results, unique='true')):
                print(f"Processing search result {count+1}: {search2}")
                try:
                    page = requests.get(search2)
                    if page.status_code != 200:
                        print(f"Failed to retrieve page: {search2} ")
                        num_results += 1
                        continue
                    print("Data retrieved successfully.")
                    soup = BeautifulSoup(page.text, 'html.parser')
                    paragraphs = soup.find_all("p")
                    if not paragraphs:
                        print("No paragraphs found on this page.")
                    else:
                        found_any = True
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
                            value = f"{value}: /n {paragraphs[0:10]}"
                    print("")
                    print("___________________________________________________________________________")
                    print("")
                except Exception:
                    print(f"Error fetching {search2}")
            if not found_any:
                print("No useful information found from search results.")
                print("Wikipedia - ")
                value = wikipedia.summary(topic)
                print(value)
            cache[key] = value
            restart()
    else: print("INVALID OPTION")
def conduct_search():
   topic = inpt.get().lower()
   num_results = 3
   key = topic
   value = f"{day}/{month}/{year}"
   num_results = 3
   try: 
    for search2 in search(topic,num_results = num_results,unique='true'):
            page = requests.get(search2)
            if page != 200:
                num_results +=1
            else:
                print("Data retrieved")
                print(search2) 
            soup = BeautifulSoup(page.text, 'html.parser')
            paragraphs = soup.find_all("p")[0:7]
            for p in paragraphs:
                p = p.get_text()
                print(p)
                value = f"""{value}: 
                {p}"""
            #re_send = input('Expand? (Y) or (N)')
            #if re_send.lower() == 'y':
                #paragraphs = soup.find_all("p")[0:5]
            print(search2)
            #for p in paragraphs:
                #p = p.get_text()
                #print(p)
            #value = f'{value}: {paragraphs[0:10]}'
            print("")
            print("___________________________________________________________________________")
            print("")
   except Exception:
    print('Failed to retireve data')
    print("Wikipedia - ")
    value = wikipedia.summary(topic)
   lbl.delete(1.0,t.END)
   lbl.insert(1.0,value)
   cache[key] = value
   return(value)
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



