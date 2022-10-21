import requests
from bs4 import BeautifulSoup
import psycopg2
import re
import time
import random


conn = psycopg2.connect(host="LOCAL_HOST", database='LOCAL_DATABASE', user='USERNAME', password='PASSWORD')
heroku_conn = psycopg2.connect(host="HEROKU_HOST", database='HEROKU_DATABASE', user='HEROKU_USER', password='HEROKU_PASSWORD')
heroku_cursor = heroku_conn.cursor()
cursor = conn.cursor()
 # We are fetching all politicians websites and id number for state. 
cursor.execute("SELECT politician_id, website from politician WHERE state= 'New York'")

for row in cursor.fetchall(): # Looping through each politician's website!!
    # row[1] is indexing into website
    theirwebsite = row[1] # This is there website so it would be like "https://google.com"
    print(theirwebsite)
    if theirwebsite == None:
        cursor.execute(""" INSERT INTO transportation(info_or_not, quotes, website_found, politician_id) VALUES (%s, %s, %s, %s); """, ( 'No Info Found', None, None, row[0]))
        heroku_cursor.execute(""" INSERT INTO transportation(info_or_not, quotes, website_found, politician_id) VALUES (%s, %s, %s, %s); """, ( 'No Info Found', None, None, row[0]))
        # row[0] is indexing into their ID
        conn.commit()
        heroku_conn.commit()
        print("Politician has no Website.")

    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        thelink = requests.get(theirwebsite, headers=headers).text
        webpages = BeautifulSoup(thelink, 'html.parser')
        transit = [] # transportation quote's 
        DataURLarray = [] # data URL quotes
        visited = {}  
        for index, webpage in enumerate(webpages.find_all('a')): # For each website we want to loop through all their webpages 
            # Examples include  google.com, google.com/images, google.com/advance_search
            try:
                if webpage['href'] not in visited: # Check if webpage is been visited!
                    if theirwebsite in webpage['href']: # if statements to see how URL is formatted
                        DataURL = webpage['href']
                        time.sleep(random.randint(1, 4))
                        newlink = requests.get(DataURL, headers=headers).text
                        getting = BeautifulSoup(newlink, "html.parser")
                        for data in getting(['style', 'script']):
                            # Remove script and styles tags
                            data.decompose()
                        if len(transit) == 0: # looking for common public transportation words! 
                            new = getting.find_all(text=re.compile(r'\bBIKES\b | \bBIKE\b |\bSUBWAYS\b | \bMETRO\b | \bRAIL\b | \bBUSES\b | \bBIKING\b | \bPEDESTRIANS\b | \bPEDESTRIAN\b | \bTRANSIT\b | \bBUS\b | \bAMTRAK\b | \bTROLLEY\b | \bTRAM\b | \bTROLLEYS\b | \bTRAMS\b'  , flags=re.I | re.X))
                            if len(new) != 0:
                                i = 0  
                                while i < len(new):
                                    DataURLarray.append(DataURL) 
                                    i = i + 1 
                                transit.extend(new) # if we find the words we extend the new list into our transit list.
                    
                        elif len(transit) !=0:
                            appending = getting.find_all(text=re.compile(r'\bBIKES\b | \bBIKE\b |\bSUBWAYS\b | \bMETRO\b | \bRAIL\b | \bBUSES\b | \bBIKING\b | \bPEDESTRIANS\b | \bPEDESTRIAN\b | \bTRANSIT\b | \bBUS\b | \bAMTRAK\b | \bTROLLEY\b | \bTRAM\b | \bTROLLEYS\b | \bTRAMS\b'  , flags=re.I | re.X))
                            if len(appending) != 0:  # if we have quotes in our list we want to check for any repeating quotes
                                if any(x in transit for x in appending):
                                    for i in len(appending):
                                        if appending[i] in transit:
                                            appending.pop(i)  # if we find any repeating quotes we remove it with the pop function
                                    if len(appending) != 0:
                                        i = 0
                                        while i < len(appending):
                                            DataURLarray.append(DataURL)
                                            i = i + 1
                                        transit.extend(appending)
                                    else:
                                        print('The whole appending array was a duplicate.')
                                else:
                                    i = 0
                                    while i < len(appending):
                                        DataURLarray.append(DataURL)
                                        i = i + 1
                                    transit.extend(appending) # if we find the words we extend the new list into our transit list.
                    
                    elif requests.get(f"{theirwebsite[:-1]}{webpage['href']}").status_code != 404: # if statements to see how URL is formatted
                        DataURL = theirwebsite[:-1] + webpage['href']
                        time.sleep(random.randint(1, 5))
                        newlink = requests.get(DataURL, headers=headers).text
                        getting = BeautifulSoup(newlink, "html.parser")
                        for data in getting(['style', 'script']):
                            # Remove script and styles tags
                            data.decompose()
                        if len(transit) == 0:
                            new = getting.find_all(text=re.compile(r'\bBIKES\b | \bBIKE\b |\bSUBWAYS\b | \bMETRO\b | \bRAIL\b | \bBUSES\b | \bBIKING\b | \bPEDESTRIANS\b | \bPEDESTRIAN\b | \bTRANSIT\b | \bBUS\b | \bAMTRAK\b | \bTROLLEY\b | \bTRAM\b | \bTROLLEYS\b | \bTRAMS\b'  , flags=re.I | re.X))
                            if len(new) != 0:
                                i = 0
                                while i < len(new):
                                    DataURLarray.append(DataURL)
                                    i = i + 1
                                transit.extend(new)
                    
                        elif len(transit) !=0:
                            appending = getting.find_all(text=re.compile(r'\bBIKES\b | \bBIKE\b |\bSUBWAYS\b | \bMETRO\b | \bRAIL\b | \bBUSES\b | \bBIKING\b | \bPEDESTRIANS\b | \bPEDESTRIAN\b | \bTRANSIT\b | \bBUS\b | \bAMTRAK\b | \bTROLLEY\b | \bTRAM\b | \bTROLLEYS\b | \bTRAMS\b'  , flags=re.I | re.X))
                            if len(appending) != 0:
                                if any(x in transit for x in appending):
                                    for i in len(appending):
                                        if appending[i] in transit:
                                            appending.pop(i)
                                    if len(appending) != 0:
                                        i = 0
                                        while i < len(appending):
                                            DataURLarray.append(DataURL)
                                            i = i + 1
                                        transit.extend(appending)
                                    else:
                                        print('The whole appending array was a duplicate.')
                                else:
                                    i = 0
                                    while i < len(appending):
                                        DataURLarray.append(DataURL)
                                        i = i + 1
                                    transit.extend(appending)


                    elif requests.get(f"{theirwebsite}{webpage['href']}").status_code != 404:
                        DataURL = theirwebsite+webpage['href']
                        newlink = requests.get(DataURL, headers=headers).text
                        time.sleep(random.randint(1, 5))
                        getting = BeautifulSoup(newlink, "html.parser")
                        for data in getting(['style', 'script']):
                            # Remove script and styles tags
                            data.decompose()
                        if len(transit) == 0:
                            new = getting.find_all(text=re.compile(r'\bBIKES\b | \bBIKE\b |\bSUBWAYS\b | \bMETRO\b | \bRAIL\b | \bBUSES\b | \bBIKING\b | \bPEDESTRIANS\b | \bPEDESTRIAN\b | \bTRANSIT\b | \bBUS\b | \bAMTRAK\b | \bTROLLEY\b | \bTRAM\b | \bTROLLEYS\b | \bTRAMS\b'  , flags=re.I | re.X))
                            if len(new) != 0:
                                i = 0
                                while i < len(new):
                                    DataURLarray.append(DataURL)
                                    i = i + 1
                                transit.extend(new)
                    
                        elif len(transit) !=0:
                            appending = getting.find_all(text=re.compile(r'\bBIKES\b | \bBIKE\b |\bSUBWAYS\b | \bMETRO\b | \bRAIL\b | \bBUSES\b | \bBIKING\b | \bPEDESTRIANS\b | \bPEDESTRIAN\b | \bTRANSIT\b | \bBUS\b | \bAMTRAK\b | \bTROLLEY\b | \bTRAM\b | \bTROLLEYS\b | \bTRAMS\b'  , flags=re.I | re.X))
                            if len(appending) != 0:
                                if any(x in transit for x in appending):
                                    for i in len(appending):
                                        if appending[i] in transit:
                                            appending.pop(i)
                                    if len(appending) != 0:
                                        i = 0
                                        while i < len(appending):
                                            DataURLarray.append(DataURL)
                                            i = i + 1
                                        transit.extend(appending)
                                    else:
                                        print('The whole appending array was a duplicate.')
                                else:
                                    i = 0
                                    while i < len(appending):
                                        DataURLarray.append(DataURL)
                                        i = i + 1
                                    transit.extend(appending)
                                    
                visited[webpage['href']] = 1 # Check if webpage is has been visited 


            except requests.exceptions.ConnectionError: # Request error
                print("All Connection Errors: ", index)
                time.sleep(random.randint(1, 3))
                pass

            except Exception as e: # Any other error like... looping through an image URL we could not do that.
                print('Other errors ', index)
                pass


        if len(transit) != 0: # if transportation data exists insert quotes
            cursor.execute(""" INSERT INTO transportation(info_or_not, quotes, website_found, politician_id) VALUES (%s, %s, %s, %s); """, ( 'Pro Transit', transit, DataURLarray, row[0]))
            heroku_cursor.execute(""" INSERT INTO transportation(info_or_not, quotes, website_found, politician_id) VALUES (%s, %s, %s, %s); """, ( 'Pro Transit', transit, DataURLarray, row[0]))
            conn.commit()
            heroku_conn.commit()
            print('LENGTH OF TRANSIT AND DATAURL', len(transit), len(DataURLarray))
        else: # else we say no quotes found !
            print("no info found")
            cursor.execute(""" INSERT INTO transportation(info_or_not, quotes, website_found, politician_id) VALUES (%s, %s, %s, %s); """, ( 'No Info Found', None, None, row[0]))
            heroku_cursor.execute(""" INSERT INTO transportation(info_or_not, quotes, website_found, politician_id) VALUES (%s, %s, %s, %s); """, ( 'No Info Found', None, None, row[0]))
            conn.commit()
            heroku_conn.commit()


            
heroku_conn.close()
conn.close()
