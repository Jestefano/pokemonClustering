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
    gen = [en+1 for i in link]
    df = pd.concat([df,pd.DataFrame({'regionalDex':regionalDex,'nationalDex':nationalDex,'link':link,'name':name,
                                     'gen':gen})])
    
print(df)

#%%  
"""
We can skim through the dataset to see how clean it is
Comments about the dataframe so far
1. There are some missing in regionalDex. But this is it because it is an alternative form or a new pokemon (the last three)
2. From regionalDex we need to clean characters 
3. nationalDex looks clean
4. Links look ok but some of them are repeated (for alternative forms of the pkmn)
5. Name: Nidoran, Farfetch, Mr. Mime, Flabebe(669), Sirfetch (865), Mr. Rime(866), Type: Null(772), Mime Jr. (439), Tapus (785)
6. Gen is ok
7. Alola and Galarian can be added carefully, as well as alternative forms based on the link provided
8. We still need stats and type

Since this is the code to scrape we will continue with 8 (and 7 if possible) and let the other points for a code in data cleaning
"""



    
