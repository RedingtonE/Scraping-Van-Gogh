# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a webscraper designed to save a repository of Van Gogh's paintings
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import urllib.request
import os.path
from os import path

#Pull out the HTML of the main page of a repository of Van Gogh's paintings
url = 'http://www.vggallery.com/'
page = requests.get(url)
soupG = BeautifulSoup(page.text, 'html.parser')

#Initialize variables to track the images path in the website, name, when and where it was painted, its current location, and informtion in F and JH about when it was painted in relation to other works
imgP = [];
imgName = [];
Origin = []; 
CL = [];
F = [];
JH = [];
#Since I am only interested in the painings the webscraper specifically looks for the hyperlinks that list paintings by the period they were painted in. Each of these pages is setup as a table with the same basic format, so we can iterate through the pages and tables to generate a list of all the paintings. We will include a delay in the scraper to be polite. 
for link in soupG.findAll('a', attrs={'href': re.compile("by_period")}):
    newPage = 'http://www.vggallery.com/' + link.get('href')
    bpPage = requests.get(newPage)
    soupBG = BeautifulSoup(bpPage.text, 'html.parser')
    allrow = soupBG.find_all("tr")
    updatedrow = soupBG.findAll("tr")
    for row in updatedrow:
        if row.get_text().find('Painting Name') == -1:
            rowinfo = row.findAll('td')
            if len(rowinfo) == 5:
                imgurl = rowinfo[0].find('a').get('href')
                imgP.append('http://www.vggallery.com/painting' + imgurl.replace('..', ''))
                imgName.append(rowinfo[0].find('b').contents)
                Origin.append(rowinfo[1].contents[0].strip())
                CL.append(rowinfo[2].contents[0].strip())
                F.append(rowinfo[3].contents[0].strip())
                JH.append(rowinfo[4].contents[0].strip())
    time.sleep(5)
#Convert to a pandas dataframe that can easily be saved as a csv and used for further analysis of the paintings
df = pd.DataFrame({'Image Path': imgP, 'Image Name': imgName, 'Origin': Origin, 'CL': CL, 'F': F, 'JH': JH})
#Unfortunately hardcoded, could be improved by concatenating a string with the current working directory    
df.to_csv(r'C:\Users\Emmy\Documents\Scrapetest\Vangogh.csv')
direc = r'C:\Users\Emmy\Documents\Scrapetest\savedPaintings' 

#Use the image paths we previously saved to locate the url where each painting is stored and then download it to a directory. Since we will be opening far more web pages in this for loop I have opted to include a delay that is related to the response delay of the server. This way if we start to overlaod it the scraper will back off. Also included conditions to prevent accessing the same painting if it's already been saved and the scraper needs to be run again. 
for index, row in df.iterrows():
    t0 = time.time()
    imUrl = row['Image Path']
    undInd = imUrl.find('_')+1
    pInd = imUrl.find('.htm')
    chStr = imUrl[undInd:pInd]
    saveName = direc + '\\' + chStr + '.png'
    if path.exists(saveName):
        print('skipping:' + saveName)
    else: 
        imgPage = requests.get(imUrl)
        soupIP = BeautifulSoup(imgPage.text, 'html.parser')
        response_delay = time.time() - t0;
        print(response_delay)
        time.sleep(response_delay)
        dlstr = soupIP.find('img', attrs={'src': re.compile(chStr)}).get('src')
        dlURL = 'http://www.vggallery.com/painting/' + dlstr
        if len(dlURL) > 0:
            
            urllib.request.urlretrieve(dlURL, saveName)
            time.sleep(1)





    
    
