import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import datetime
import re
import os
from shutil import copyfile
import logging
import numpy as np
import sys

class RaceCardParser():

    def __init__(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('RaceResultParser.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)

        self.__logger__ = logger

    def parseRaceCard(self, filepath):
        try:
            html = open(filepath, 'r',encoding="utf-8" ).read()
            soup = BeautifulSoup(html, 'html.parser')
           
            table = soup.find('table', attrs={'class':'draggable hiddenable'})
            table_header_thead = table.find('thead')
            header_rows = table_header_thead.find_all('tr') 
            header = []
            for row in header_rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                header.append([ele for ele in cols ]) # Get rid of empty values
            header = header[0]

            table_body = table.find('tbody')
            rows = table_body.find_all('tr')  
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols ]) # Get rid of empty values
            
            data = np.array(data).T.tolist()
            df = pd.DataFrame(columns= header)
            for i,j in enumerate(header):
                df[j] = data[i]

            df['file_source'] = filepath.split('\\')[-1].split('.')[0]
            return df

        except Exception as e:
            print ("exception raised. Maybe hidden sys file")  
            self.__logger__.error(e, exc_info=True)
            return None


    def parseCurrentRaceCard(self, filepath):
        try:   
            html = open(filepath, 'r',encoding="utf-8" ).read()
            soup = BeautifulSoup(html, 'html.parser')
           
            table = soup.find('table', attrs={'class':'draggable hiddenable'})


            table_header_thead = table.find('tr', attrs={'class':'trBg01 boldFont13'})
            header_rows = table_header_thead.find_all('td')
            cols = [ele.text.strip() for ele in header_rows]
            header = cols
            
            table_body = table.find_all('tr')
            table_body = table_body[1:]
            data = []
            for row in table_body:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols ]) # Get rid of empty values
            data = np.array(data).T.tolist()
            df = pd.DataFrame(columns= header)
            for i,j in enumerate(header):
                df[j] = data[i]

            

            df['file_source'] = filepath.split('/')[-1].split('.')[0]


            table = soup.find('table', attrs={'class':'font13 lineH20 tdAlignL'})
            table_body = table.find('tr')
           
            table_content = table.find('td').get_text()

            found_class = re.search('Class \d', table_content)
            if found_class:
                found_class = found_class.group()
            else:
                found_class = "UNKNOWN"
                
            found_distance = re.search('\d\d\d\dM', table_content).group()
            

            isTurf = re.search('Tur', table_content)
            if isTurf:
                turfType = re.search(',.*Course,', table_content).group()
                turfType = turfType.replace(", ","")
                turfType = turfType.replace(",","")
                turfType = turfType.replace("Course","COURSE")
                found_course = "TURF - " + turfType
            else:
                found_course = "ALL WEATHER TRACK"


            table_content = str (table.find('td')      )          
            list_of_content = table_content.split("<br/>")
            list_of_content = list_of_content[-2].split(",")


            found_going = list_of_content[-1].strip().upper()


            df['class'] = found_class
            df['distance'] = found_distance
            df['going'] = found_going
            df['course'] = found_course
            return df

        except Exception as e:
            print ("exception raised. Please see the log.")  
            self.__logger__.error(e, exc_info=True)
            return None


if __name__ == "__main__":
    rcp = RaceCardParser()
    df = rcp.parseCurrentRaceCard("/Users/felixleung/airflow/datafile/html/20190220-HV-5.html")
    print (df)
    