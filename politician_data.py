import requests
from bs4 import BeautifulSoup
import psycopg2
import re
import time
import random


conn = psycopg2.connect(host="LOCALHOST", database='DATABASE', user='USERNAME', password='PASSWORD')
cursor = conn.cursor()
heroku_conn = psycopg2.connect(host="HEROKU_HOST", database='HEROKU_DATABASE', user='HEROKU_USER', password='HEROKU_PASSWORD')

heroku_cursor = heroku_conn.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
URL = "" # THE URL I USED to gather data from. 
r = requests.get(URL, headers=headers).text
soup = BeautifulSoup(r, 'html.parser') 
div = soup.find("div", class_="mw-parser-output")
tags = div.contents
h3 = div.find_all("h3")
general_election = div.find_all("p", text="General election candidates")
for tag in tags:
    if tag in h3:
        str_district = re.sub('[^0-9\.]','', tag.text)
        int_district = int(str_district)
        politician_district = tag.text # store politician_district 
        print("politician_district: ", int_district)
    if tag in general_election:
        ultags = tag.next_element.next_element.next_element.next_element
        for li in ultags:
            politician_name = li.next_element.text
            print("Name: ", politician_name) # Name of Politician 
            print(li.next_element['href'])  #<= ballotpedia url for each politcian 
            politicianURL = li.next_element['href']
            time.sleep(random.randint(10, 27))
            request = requests.get(politicianURL, headers=headers).text
            politician = BeautifulSoup(request, "html.parser")
            infobox = politician.find("div", class_="infobox person")
            politicianwebsite = infobox.find("a", text="Campaign website") 
            politicalparty = infobox.find(text=re.compile(r'\bPARTY\b', flags=re.I | re.X)) # politician party 
            time.sleep(random.randint(9, 20))

            if politicianwebsite is None:
                print(f"{li.next_element.text} does not have a website") # does not have a site
                cursor.execute(""" INSERT INTO politician(full_name, house_or_senate, state, district, party, website) VALUES (%s,%s, %s, %s, %s, %s) """, (politician_name, 'House', 'STATE', int_district, politicalparty, None))
                heroku_cursor.execute(""" INSERT INTO politician(full_name, house_or_senate, state, district, party, website) VALUES (%s,%s, %s, %s, %s, %s) """, (politician_name, 'House', 'STATE', int_district, politicalparty, None))
                conn.commit()
                heroku_conn.commit()
                time.sleep(random.randint(10, 25))

                print("NO WEBSITEEEEEEEE")

            else:
                print(politicianwebsite['href']) #politician site 
                theirwebsite = politicianwebsite['href'] #store politician website
                cursor.execute(""" INSERT INTO politician(full_name, house_or_senate, state, district, party, website) VALUES (%s,%s, %s, %s, %s, %s) """, (politician_name, 'House', 'STATE', int_district, politicalparty, theirwebsite))
                heroku_cursor.execute(""" INSERT INTO politician(full_name, house_or_senate, state, district, party, website) VALUES (%s,%s, %s, %s, %s, %s) """, (politician_name, 'House', 'STATE', int_district, politicalparty, theirwebsite))
                heroku_conn.commit()
                conn.commit()
                time.sleep(random.randint(14, 25))
                print("Website completed")

conn.close()
heroku_conn.close()

