# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import urllib.request
import os.path
from os import path

url = 'http://www.vggallery.com/'
page = requests.get(url)
soupG = BeautifulSoup(page.text, 'html.parser')

imgP = [];
imgName = [];
Origin = []; 
CL = [];
F = [];
JH = [];
for link in soupG.findAll('a', attrs={'href': re.compile("by_period")}):
    newPage = 'http://www.vggallery.com/' + link.get('href')
    bpPage = requests.get(newPage)
    soupBG = BeautifulSoup(bpPage.text, 'html.parser')
    allrow = soupBG.find_all("tr")
    a.decompose()
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
    
df = pd.DataFrame({'Image Path': imgP, 'Image Name': imgName, 'Origin': Origin, 'CL': CL, 'F': F, 'JH': JH})
    
df.to_csv(r'C:\Users\Emmy\Documents\Scrapetest\Vangogh.csv')
direc = r'C:\Users\Emmy\Documents\Scrapetest\savedPaintings' 

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





    
    
