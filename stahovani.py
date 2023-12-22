import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib.parse import urlparse, parse_qs



URL = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"
url_parts = []
d_loc_data = []
title_data = []
meta_url = []
dflocal = []
url_title = []

def _find_topic_data(html):
    """Separate soup and find registred votes and process it. 
    Output is overall data.
    """
    soup = BeautifulSoup(html, features="html.parser")
    header_classes = ["sa2", "sa3", "sa6"]
    ingredience_data = []

    for header_class in header_classes:
        ingredience = soup.find_all(class_="cislo", headers=header_class)
        ingredience_data.extend([data.text.strip() for data in ingredience])

    return ingredience_data

def _find_table_data(html):
    """Separate soup and find votes data and process it - table 1.
    Output is table data - votes data."""
    soup = BeautifulSoup(html, features="html.parser")
    header_classes = ["t1sb3", "t2sb3"]
    ingredience_table_data = []

    for header_class in header_classes:
        ingredience = soup.find_all(class_="cislo", headers=header_class)
        ingredience_table_data.extend([data.text.strip() for data in ingredience])

    return ingredience_table_data

def flatten_extend(matrix):
    """Uniforming list of row data. 
    Procedure prepare smooth list of data.
    Output is uniformed data list."""
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
        
    return flat_list

def download_data(webpage):
    """Check responce webpage and download it. 
    Then call procedure for uniform procedure. 
    Output is downloaded raw data."""
    while True:
        d_local_data = []
        d_local_data.clear()
        claim = requests.get(webpage)
        claim.raise_for_status()
       
        d_local_data.append(_find_topic_data(claim.text))
        d_local_data.append(_find_table_data(claim.text))
        
        
        return (flatten_extend(d_local_data))

def _find_ID(html):
    """Separate soup and find ID and process it. Output is ID data."""
    soup = BeautifulSoup(html, features="html.parser")
    header_classes = ["t1sa1", "t2sa1", "t3sa1"]
    ingredience_data_ID = []

    for header_class in header_classes:
        ingredience = soup.find_all(class_="cislo", headers=header_class)
        ingredience_data_ID.extend([data.text.strip() for data in ingredience])

    return ingredience_data_ID

def _find_name(html):
    """Separate soup and find name of city and process it.
    Output is list of city's name."""
    soup = BeautifulSoup(html, features="html.parser")
    header_classes = ["t1sa1", "t2sa1", "t3sa1"]
    ingredience_data_name = []

    for header_class in header_classes:
        ingredience = soup.find_all(class_="overflow_name", headers=header_class)
        ingredience_data_name.extend([data.text.strip() for data in ingredience])

    return ingredience_data_name

def _url_creator(ID_city,column):
    """For each ID is creating unique URL 
    and then call data_mining. Here is printing load sequence.
    Output is dataframe 2."""
    base_url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj="
    counter = -1
    dfl = []
    for a in ID_city[0]:
        counter += 1
        url_temp = base_url + str(url_parts[0]) + "&xobec=" + str(a) + "&xvyber=" + str(url_parts[1])
        
        print("Progress {:2}/".format(counter),len(ID_city[0]), end="\r")
        dfl.append(download_data(url_temp))
        
    df2 = pd.DataFrame(np.array(dfl), columns=column)
    return (df2)

def _dframe(main_data, column2, column1):
    """Transpose the Info(ID and name) data, then merge 
    Info data together with dataframe. Output is dataframe."""
    df = main_data
    df1 = pd.DataFrame(np.array(df.transpose()), columns=column1)
    #print(dft)
    df2 = _url_creator(d_loc_data, column2)
    #print(df2)
    result_frame = pd.concat([df1, df2], axis=1)
    
    return (result_frame)

def _find_titles_lvl_1(html):
    """Separate soup and find title on level-1 page and process it. 
    Then add information to output. Output is title-data."""
    soup = BeautifulSoup(html, features="html.parser")
    
    title_ids = ["t1sb1", "t1sb2"]
    title_classes = ["fixed45", "fixed150"]
    
    ingredience_title = []

    for title_id, title_class in zip(title_ids, title_classes):
        ingredience = soup.find_all(id=title_id, class_=title_class)
        ingredience_title.extend([data.text.strip() for data in ingredience])

    return ingredience_title

def _title_url(ID_city):
    """For each ID is creating unique URL 
    and then call data_mining. Here is printing load sequence.
    Output is dataframe 2."""
    base_url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj="
    url_temp = base_url + str(url_parts[0]) + "&xobec=" + ID_city + "&xvyber=" + str(url_parts[1])
    task = requests.get(url_temp)
    task.raise_for_status()
    
    dft = (_find_titles_lvl_2(task.text))
    
    return (dft)

def _find_titles_lvl_2(html):
    """Separate soup and find votes data and process it - table 1.
    Output is table data - votes data."""
    soup = BeautifulSoup(html, features="html.parser")
    
    title_ids = ["sa2", "sa3", "sa6"]
    title_classes = ["overflow_name", "overflow_name"]
    title_headers = ["t1sa1", "t2sa1"]
    
    ingr_title_data = []

    for title_id in title_ids:
        ingredience = soup.find_all(id=title_id)
        ingr_title_data.extend([data.text.strip() for data in ingredience])

    for title_class, title_header in zip(title_classes, title_headers):
        ingredience = soup.find_all(class_=title_class, headers=title_header)
        ingr_title_data.extend([data.text.strip() for data in ingredience])

    return ingr_title_data

def _strip_url(www):
    """Used to parse the query string of the URL and create a dictionary 
    of parameter names and values."""
    # Parse the URL
    parsed_url = urlparse(www)

     # Extract query parameters
    query_params = parse_qs(parsed_url.query)

    # Get the values of xkraj and xnumnuts
    xkraj_value = query_params.get('xkraj', [])[0]
    xnumnuts_value = query_params.get('xnumnuts', [])[0]

    url_parts.append(xkraj_value)
    url_parts.append(xnumnuts_value)
    return

def dwn_main_webpage(www):
    """Raise for status www page and start up process 
    to find ID, name, titles and data. After collecting data 
    prepare lists to merge."""
    while True:
        task = requests.get(www)
        task.raise_for_status()
        _strip_url(www)
        
        d_loc_data.append(_find_ID(task.text))      
        d_loc_data.append(_find_name(task.text))
        title_data.append(_find_titles_lvl_1(task.text))

        d_f = _dframe((pd.DataFrame(np.array(d_loc_data))),_title_url((d_loc_data[0][0])), title_data)
        print(d_f)
        d_f.to_csv(r"C:\Users\Lukas\Desktop\Python-output\volby.csv", index = False)
        break

if __name__ == "__main__":

    dwn_main_webpage(URL)
    

