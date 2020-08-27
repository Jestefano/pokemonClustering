# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:36:30 2020

@author: JTR
"""
#%% Ruta y librerias
my_folder = r'C:\Users\JTR\Desktop\pokemon'

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import re
import shutil

#%% Exploring html and defining generations
url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'

page = requests.get(url)
print(page)

bs = BeautifulSoup(page.content)
html = str(bs)

#We can get to this exploring the web page
l = html.split('Pokémon\n</th>')
print(len(l))
for j,i in enumerate(l):
    print(j)
    print(i[:500])
    print('---')
#%% See where we end
end = l=html.split('id="See_also"')
print(len(end))

for i in end:
    print(i[:100])
    print('---')
    
interest = end[0]
#%% Separacion de generaciones

generations = interest.split('Pokémon\n</th>')
print(len(generations))

for i in generations:
    print(i[:500])
    print('---')
# La primera se debe dropear, los demas funcionan
generations = generations[1:]


#%% Exploratorio por generacion
aux1 = re.findall('<tr style="background:#FFF">\n<td style="font-family:monospace">([^<]+)\n</td>',generations[0])
print('kdex number:')
print(aux1[-10:])
print(len(aux1))
aux2 = re.findall('<td style="font-family:monospace">([^<]+)\n</td>\n<th>',generations[0])
print('Ndex number:')
print(aux2[-10:])
print(len(aux2))
aux3 = re.findall('<th> <a href="([^<]+)" title="',generations[0])
print('link:')
print(aux3[-10:])
print(len(aux3))
print('nombre:')
aux4 = [i.split('/')[2].split('_')[0] for i in aux3]
print(aux4[-10:])
print(len(aux4))
#Type and stats can be downloaded from their respective links
"""
Observations
1. There is a problem in the length of the first generation: Moltres, Zapdos and Articuno
2. There is a problem with Slowking in the 2nd
This will be considered in the code for web scrapping
"""

#%% For a single pokemon

def f (url):
    page = requests.get(url)
    bs = BeautifulSoup(page.content,features="lxml")
    html = str(bs)
    
    #We can get to this exploring the web page
    l = html.split('<a href="/wiki/Type" title="Type"><span style="color:#000;">Types</span></a>')
    
    end = (l[1]).split('Abilities')[0]
    
    aux = re.findall('<small>([^<]+)?</small>',end)
    aux = [i for i in aux if i!='']
    print(len(aux))
    print(aux)
    tipos = end.split('<small>')[:len(aux)]
    aux = [re.findall('<b>([^<]+)?</b>',i) for i in tipos]
    print(aux)
    
(f('http://bulbapedia.bulbagarden.net/wiki/Corsola_(Pokémon)'))
f('https://bulbapedia.bulbagarden.net/wiki/Dugtrio_(Pok%C3%A9mon)')
#%% For only one pkmn 

def f (url):
    page = requests.get(url)
    bs = BeautifulSoup(page.content,features="lxml")
    html = str(bs)
    
    #We can get to this exploring the web page
    l = html.split('<a href="/wiki/Type" title="Type"><span style="color:#000;">Type</span></a>')
    
    end = (l[1]).split('Abilities')[0]
    
    aux = re.findall('<small>([^<]+)?</small>',end)
    aux = [i for i in aux if i!='']
    print(len(aux))
    print(aux)
    tipos = end.split('<small>')[:len(aux)]
    aux = [re.findall('<b>([^<]+)?</b>',i) for i in tipos]
    print(aux)


f('https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)')

