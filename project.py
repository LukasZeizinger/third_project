from bs4 import BeautifulSoup

import requests

import pandas as pd


url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html")


mydivs = soup.find_all('a', href=True)
key_string = "kraj"
key_string_direct = "xvyber"
#print(mydivs)


lib_url = []

for a in mydivs:
    
    if (a['href']) in lib_url:
        pass
    elif key_string in str(a):
        
        if key_string_direct in str(a):
            lib_url.append(str(a['href']))

        else:
            url_temp = "https://volby.cz/pls/ps2017nss/" + str(a['href'])
            page_temp = requests.get(url_temp)
            soup_temp = BeautifulSoup(page_temp.text, "html")
            print("Search for ", url_temp)
            mydivs_temp = soup_temp.find_all('a', href=True)
            

            for b in mydivs_temp:

                if (b['href']) in lib_url:
                    pass
                elif key_string in str(b) and key_string_direct in str(b) and (b['href']) not in lib_url:
                    lib_url.append(str(b['href']))
                                 
    else:
        pass

print("All URL was downloaded")

for x in lib_url:
    url_temp = "https://volby.cz/pls/ps2017nss/" + str(x)
    page_temp = requests.get(url_temp)
    soup_temp = BeautifulSoup(page_temp.text, "html")
    print("Download data from: ", url_temp)

    mydivs_temp = soup_temp.find_all('a')
        
    world_titles = mydivs_temp.find_all("a")

world_table_titles = [title.text.strip() for title in world_titles]
print(world_table_titles)
#<table class="wikitable sortable jquery-tablesorter">
#<caption>

#df = pd.DataFrame(columns=world_table_titles)

#column_data = table.find_all("tr")

#for row in column_data[1:]:
#    row_data = row.find_all("td")
#    individual_row_data = [data.text.strip() for data in row_data]
#    lenght = len(df)

#    df.loc[lenght] = individual_row_data

#print(df)
#df.to_csv(r"C:\Users\Lukas\Desktop\Python-output\Companies.csv", index = False)

#prostejov
#https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103


