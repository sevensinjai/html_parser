

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import datetime
import re
import os
from shutil import copyfile



class RaceMetaParser():

    def parseRaceData(self, filepath):
        '''
        This function is dedicated to parse the race data in the result page and return the dataset
        Param: filepath of the HTML
        Return: transformed dataset
        '''    
        try:
            html = open(filepath, 'r').read()
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', attrs={'class':'tableBorder0'})
            rows = table.find_all('tr')   
            data = []  
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values
            classDistanceGoing = data[0]
            course = data[1][2]
            raceClass = classDistanceGoing[0].split('-')[0].strip()
            distance = classDistanceGoing[0].split('-')[1].strip()
            going = classDistanceGoing[2]
            fileSource = filepath.split("/")[-1].split(".")[0]
            col = ['file_source','class', 'distance', 'going', 'course']
            data = [[fileSource,raceClass, distance, going, course]]
            df = pd.DataFrame(data=data)
            df.columns = col
            return df
        except:
            print ("exception raised. Maybe hidden sys file")
            return "error"