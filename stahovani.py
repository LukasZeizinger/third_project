from bs4 import BeautifulSoup

import requests

import pandas as pd

L = [list("")]
big_data = []
url_temp = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=505587&xvyber=7102"
page_temp = requests.get(url_temp)
soup_temp = BeautifulSoup(page_temp.text, "html")
print("Download data from: ", url_temp)




Xcom = soup_temp.find_all("table")[1]
#print(Xcom)

table_titles = Xcom.find_all("th")

volby_table_title = [title.text.strip() for title in table_titles]
#print(volby_table_title)

#df = pd.DataFrame(columns = volby_table_title)
df = pd.DataFrame()

DTP = Xcom.find_all("tr")

for row in DTP[2:]:
    row_data = row.find_all("td")
    individual_row_data = [data.text.strip() for data in row_data]
    
    big_data.append(individual_row_data)

print(big_data)
#Xcom1 = soup_temp.find("table", class_ = "table")
#print(Xcom1)

#<table id="ps311_t1" class="table">


#<table class="table">

#<div class="t2_470">
