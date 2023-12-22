import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


URL = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

d_m_w_local_data = []
meta_url = []
dflocal = []

def _find_topic_data(html):
    """Separate soup and find registred votes and process it."""
    soup = BeautifulSoup(html,features="html.parser")
    #group = ["sa2", "sa3", "sa6"]

    ingredience = soup.find_all(class_="cislo", headers="sa2")
    _data_1 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="cislo", headers="sa3")
    _data_2 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="cislo", headers="sa6")
    _data_3 = [data.text.strip() for data in ingredience]
    ingredience_data = _data_1 + _data_2 + _data_3
    return ingredience_data

def _find_table_data(html):
    """Separate soup and find votes data and process it - table 1."""
    soup = BeautifulSoup(html,features="html.parser")
    #group = ["t1sb3", "t2sb3"]

    ingredience = soup.find_all(class_="cislo", headers="t1sb3")
    _data_1 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="cislo", headers="t2sb3")
    _data_2 = [data.text.strip() for data in ingredience]
    ingredience_table_data = _data_1 + _data_2
    return ingredience_table_data


def flatten_extend(matrix):
    """Uniforming list of row data. 
    Procedure prepare smooth list of data."""
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
        
    return flat_list

def download_data(webpage):
    """Check responce webpage and download it. 
    Then call procedure for uniform procedure."""
    while True:
        d_local_data = []
        d_local_data.clear()
        claim = requests.get(webpage)
        claim.raise_for_status()
       
        d_local_data.append(_find_topic_data(claim.text))
        d_local_data.append(_find_table_data(claim.text))
        #print(local_data)
        return (flatten_extend(d_local_data))

def _find_ID(html):
    """Separate soup and find ID and process it."""
    soup = BeautifulSoup(html,features="html.parser")
    
    ingredience = soup.find_all(class_="cislo", headers="t1sa1")
    _data_ID1 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="cislo", headers="t2sa1")
    _data_ID2 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="cislo", headers="t3sa1")
    _data_ID3 = [data.text.strip() for data in ingredience]
    ingredience_data_ID = _data_ID1 + _data_ID2 + _data_ID3
    return ingredience_data_ID

def _find_name(html):
    """Separate soup and find name of city and process it."""
    soup = BeautifulSoup(html,features="html.parser")
    ingredience = soup.find_all(class_="overflow_name", headers="t1sa1")
    _data_name1 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="overflow_name", headers="t2sa1")
    _data_name2 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(class_="overflow_name", headers="t3sa1")
    _data_name3 = [data.text.strip() for data in ingredience]
    ingredience_data_name = _data_name1 + _data_name2 + _data_name3
    return ingredience_data_name

def _url_creator(ID_city):
    counter = -1
    dfl = []
    for a in ID_city[0]:
        counter += 1
        url_temp = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=" + str(a) + "&xvyber=7103"
        print("Progress {:2}/".format(counter),len(ID_city[0]), end="\r")
        #print(counter, url_temp, end="\r")
        dfl.append(download_data(url_temp))
    
    df2 = pd.DataFrame(np.array(dfl))
    return (df2)

def dwn_main_webpage(www):
    """"""
    while True:
        task = requests.get(www)
        task.raise_for_status()

        d_m_w_local_data.append(_find_ID(task.text))
        d_m_w_local_data.append(_find_name(task.text))
        df = pd.DataFrame(np.array(d_m_w_local_data))
        dft = df.transpose()
        print(dft)

        df2 = _url_creator(d_m_w_local_data)
        print(df2)
        result = pd.concat([dft, df2], axis=1)
        print(result)

        break

if __name__ == "__main__":
#    download_data(URL)
    dwn_main_webpage(URL)
    

