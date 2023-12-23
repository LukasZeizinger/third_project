# importing the module 
import sys 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib.parse import urlparse, parse_qs
import os

# storing the arguments 

# arguments 
area_link = sys.argv[1] 
output_file = sys.argv[2]  
url_parts = []
d_loc_data = []
title_data = []
meta_url = []
dflocal = []
url_title = []

# function definition 
def concat(s1, s2):
    """Check if the correct number of arguments is provided"""
    if len(sys.argv) != 3:
        print("Usage: python script_name.py 'area_link' 'output_file.csv'")
        sys.exit(1) 
    elif "https://volby.cz/pls/ps2017nss/" not in s1:
        print(
            "Usage: python script_name.py 'area_link(in shape https://volby"\
            ".cz/pls/ps2017nss...)' 'output_file.csv'"
            )
        sys.exit(1) 

    print(s1 + " " + s2)

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
    ingre_table_data = []

    for header_class in header_classes:
        ingredience = soup.find_all(class_="cislo", headers=header_class)
        ingre_table_data.extend([data.text.strip() for data in ingredience])

    return ingre_table_data

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
    ingre_data_ID = []

    for header_class in header_classes:
        ingredience = soup.find_all(class_="cislo", headers=header_class)
        ingre_data_ID.extend([data.text.strip() for data in ingredience])

    return ingre_data_ID

def _find_name(html):
    """Separate soup and find name of city and process it.
    Output is list of city's name."""
    soup = BeautifulSoup(html, features="html.parser")
    header_classes = ["t1sa1", "t2sa1", "t3sa1"]
    ingre_data_name = []

    for header_class in header_classes:
        ingre = soup.find_all(class_="overflow_name", headers=header_class)
        ingre_data_name.extend([data.text.strip() for data in ingre])

    return ingre_data_name

def _url_creator(ID_city,column):
    """For each ID is creating unique URL 
    and then call data_mining. Here is printing load sequence.
    Output is dataframe 2."""
    base_url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj="
    counter = -1
    dfl = []
    for a in ID_city[0]:
        counter += 1
        url_temp = (
            base_url + str(url_parts[0]) +
              "&xobec=" + str(a) + "&xvyber=" + str(url_parts[1]))
        
        print("Progress {:2}/".format(counter),len(ID_city[0]), end="\r")
        dfl.append(download_data(url_temp))
        
    df2 = pd.DataFrame(np.array(dfl), columns=column)
    return (df2)

def _dframe(main_data, column2, column1):
    """Transpose the Info(ID and name) data, then merge 
    Info data together with dataframe. Output is dataframe."""
    df = main_data
    tt = df.transpose()
    df1 = pd.DataFrame(np.array(tt), columns = column1[0])

    
    df2 = _url_creator(d_loc_data, column2)
    
    result_frame = pd.concat([df1, df2], axis=1)
    
    return result_frame

def _find_titles_lvl_1(html):
    """Separate soup and find title on level-1 page and process it. 
    Then add informatin to output. Output is title-data."""
    soup = BeautifulSoup(html,features="html.parser")
    

    ingredience = soup.find_all(id="t1sb1", class_="fixed45")
    _title_1 = [data.text.strip() for data in ingredience]
    ingredience = soup.find_all(id="t1sb2", class_="fixed150")
    _title_2 = [data.text.strip() for data in ingredience]
    
    ingredience_title = _title_1 + _title_2
    
    return ingredience_title

def _title_url(ID_city):
    """For each ID is creating unique URL 
    and then call data_mining. Here is printing load sequence.
    Output is dataframe 2."""
    base_url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj="
    url_temp = (
        base_url + str(url_parts[0]) + "&xobec=" +
          ID_city + "&xvyber=" + str(url_parts[1]))
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
        ingre = soup.find_all(id=title_id)
        ingr_title_data.extend([data.text.strip() for data in ingre])

    for title_class, title_header in zip(title_classes, title_headers):
        ingre = soup.find_all(class_=title_class, headers=title_header)
        ingr_title_data.extend([data.text.strip() for data in ingre])

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

def dwn_main_webpage(www, output_file):
    """Raise for status www page and start up process 
    to find ID, name, titles and data. After collecting data 
    prepare lists to merge."""
    while True:
        task = requests.get(www)
        task.raise_for_status()
        # Assuming _strip_url is defined somewhere
        _strip_url(www)
        
        d_loc_data.append(_find_ID(task.text))      
        d_loc_data.append(_find_name(task.text))
        title_data.append(_find_titles_lvl_1(task.text))

        # Assuming _dframe and _title_url are defined somewhere
        d_f = (_dframe(pd.DataFrame(np.array(d_loc_data)), 
                _title_url(d_loc_data[0][0]), title_data))
        #print(d_f)
        
        # Create the directory if it doesn't exist
        # Get the directory of the script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Create the directory if it doesn't exist
        output_directory = os.path.join(script_directory, "Python-output")

        os.makedirs(output_directory, exist_ok=True)
        
        # Use os.path.join to construct the file path
        output_path = os.path.join(script_directory, str(output_file))

        
        # Use to_csv with the updated path
        d_f.to_csv(output_path, index=False)
        print("Thx for using, all is done and file", output_file, "is "\
               "prepared.")
        break

if __name__ == "__main__":
    # Ensure output_file is assigned the correct value
    #output_file = output_file
    
    # calling the function 
    concat(area_link, output_file)
    dwn_main_webpage(area_link, output_file)
