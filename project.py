from bs4 import BeautifulSoup

import requests

import pandas as pd


url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html")


table = soup.find_all("table")[1]

world_titles = table.find_all("th")

world_table_titles = [title.text.strip() for title in world_titles]
#print(world_table_titles)
#3<table class="wikitable sortable jquery-tablesorter">
#<caption>

df = pd.DataFrame(columns=world_table_titles)

column_data = table.find_all("tr")

for row in column_data[1:]:
    row_data = row.find_all("td")
    individual_row_data = [data.text.strip() for data in row_data]
    lenght = len(df)

    df.loc[lenght] = individual_row_data

print(df)
df.to_csv(r"C:\Users\Lukas\Desktop\Python-output\Companies.csv", index = False)

# TODO zjistit tabulku na webu voleb - https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103

# TODO argument se kterym je spusten program je x na okresnich mestech viz odkaz

# TODO zjistit tabulku <td class="center" headers="t1sa2"><a href="https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103">

# TODO <ts class="cislo"header="s1"><a href="https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=589276&xokrsek=1&xvyber=7103">

# TODO If je obsazeno <th colspan="2" id="s1">Okrsek</th>, pak delej prohledani v zanorenych webech
# TODO jestlize neni, tak hledej v aktualnim
