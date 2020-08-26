# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 05:58:34 2020

@author: JTR
"""
#Libraries
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import re
import shutil
pd.options.display.max_columns = 10

#%% Generations
url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
page = requests.get(url)
bs = BeautifulSoup(page.content,features="lxml")
html = str(bs)
end = html.split('id="See_also"')
interest = end[0]
l = interest.split('Pokémon\n</th>')[1:]
#%%
df = pd.DataFrame()
#One loop per generation
for en,i in enumerate(l):
    regionalDex= re.findall('<tr style="background:#FFF">\n<td style="font-family:monospace">([^<]+)\n</td>',i)
    regionalDex = np.array(regionalDex)
    nationalDex = re.findall('<td style="font-family:monospace">([^<]+)\n</td>\n<th>',i)
    nationalDex = np.array(nationalDex)
    link = re.findall('<th> <a href="([^<]+)" title="',i)
    name = [j.split('/')[2].split('_')[0] for j in link]
    if(en==0):
        aux = np.ones(regionalDex.shape,dtype=bool)
        aux[[-6,-8,-10]] = 0
        regionalDex = regionalDex[aux].copy()
        nationalDex = nationalDex[aux].copy()
    if(en==1):
        aux = np.ones(regionalDex.shape,dtype=bool)
        aux[48] = 0
        regionalDex = regionalDex[aux].copy()
        nationalDex = nationalDex[aux].copy()
    link = ['https://bulbapedia.bulbagarden.net'+j for j in link]
    df = pd.concat([df,pd.DataFrame({'regionalDex':regionalDex,'nationalDex':nationalDex,'link':link,'name':name})])
    
print(df)

#%%    
    
    
    
    
    
    
    
