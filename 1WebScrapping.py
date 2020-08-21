# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:36:30 2020

@author: JTR
"""
#%% Ruta y librerias
my_folder = r'C:\Users\LENOVO\Desktop\pokemon'

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

generations = interest.split('title="Generation')
print(len(generations))

for i in generations:
    print(i[:100])
    print('---')
# La primera se debe dropear, los demas funcionan
generations = generations[1:]

#%%Crear entorno para guardar los datos:
dataset = my_folder +'/dataset'
if not os.path.exists(dataset):
    os.mkdir(dataset)


#%% Exploratorio por generacion

aux = re.findall('<img alt=(.+)>',generations[0])
print(len(aux))

for i in range(100):
    print(aux[i])

names = re.findall('"(.+)" height',aux[0])
print(names)

url = re.findall('src="//(.+)" width',aux[0])
print(url)

#%% Generalizando para las demas generaciones y probando para los demas pokemon
def separarPokemon(gen):
    return re.findall('<img alt=(.+)',gen)

def extraerNombresPokemon(pokemon):
    return re.findall('"(.+)" height',pokemon)[0]

def extraerUrlPokemon(pokemon):
    return re.findall('src="//(.+)" width',pokemon)[0]
         
#%% Testeo de las funciones en gen1
pokemonGen1 = separarPokemon(generations[0])
pokemons = []
urls = []
for j,i in enumerate(pokemonGen1):
    nombre = extraerNombresPokemon(i)
    url = extraerUrlPokemon(i)
    pokemons.append(nombre)
    urls.append(url)
    
for j,i in enumerate(pokemonGen1):
    nombre = pokemons[j]
    url = urls[j]
    dataset = my_folder +'/dataset/1'
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    filename = my_folder+'/dataset/1/'+nombre+'.png'
    image = requests.get('https://'+url,stream=True)
    if image.status_code == 200:
        image.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(image.raw, f)            
    else:
        print('Image Couldn\'t be retreived')
    
    if(j>10):
        break

#It works!
#%% 
"""
Mas exploracion de la pagina nos hace ver que hay forma Alola 
Y hay algunos que tienen una entrada extra 

en ambos casos se soluciona ignorando las entradas repetidas

Ademas hace falta randomizar para separar en train y test
"""
#%% Hacemos la generalizacion del codigo asegurandonos de unicidad:

def extraerPokemonLink(gen,generations):
    pokemonGen = separarPokemon(generations[gen-1])
    pokemons = []
    urls = []
    for i in (pokemonGen):
        nombre = extraerNombresPokemon(i)
        url = extraerUrlPokemon(i)
        if(nombre in pokemons): continue
        pokemons.append(nombre)
        urls.append(url)
    gens = [gen]*len(urls)
    return pd.DataFrame({'pokemon':pokemons, 'url':urls,'gen':gens})
    

def descargaPokemon(dfPokemon,gen,my_folder,trainTest):
    if not os.path.exists(my_folder):
        os.mkdir(my_folder)
    for index,row in dfPokemon.iterrows():
        nombre = row.pokemon
        url = row.url
        dataset = my_folder +'/dataset/'+trainTest+'/'+str(gen)
        if not os.path.exists(dataset):
            os.mkdir(dataset)
        filename = dataset+'/'+nombre+'.png'
        image = requests.get('https://'+url,stream=True)
        if image.status_code == 200:
            image.raw.decode_content = True
            with open(filename,'wb') as f:
                shutil.copyfileobj(image.raw, f)            
        else:
            print(nombre+' Couldn\'t be retreived')
    
#pok = extraerPokemonLink(1,generations)
#descargaPokemon(pok[0],pok[1],1,range(len(pok[0])),my_folder,'train')


#%% Hacemos la permutacion con tamano train/test
def descargaTrainTest(my_folder):
    from sklearn.model_selection import train_test_split
    l = []
    for i in range(1,9):
        l.append(extraerPokemonLink(i,generations))
    dfPokemon = pd.concat(l,axis=0)
    dfPokemon.reset_index(drop=True,inplace=True)
    #dfPokemon.drop([-1,-2,-3],axis=0,inplace=True)
    train,test = train_test_split(dfPokemon,train_size=0.8,stratify=dfPokemon['gen'])
    for i in range(1,9):
        descargaPokemon(train[train.gen==i].copy(),i,my_folder,'train')
        descargaPokemon(test[test.gen==i].copy(),i,my_folder,'test')
    
    

#%% Eliminamos descargas previas y creamos todos los folders


#%% Finalmente, hacemos todas las descargas

descargaTrainTest(r'C:\Users\JTR\Desktop\python\projects\pokemon')

#%%
from sklearn.model_selection import train_test_split
train,test = train_test_split(aux,train_size=0.8,stratify=aux.gen)
print(train.shape)
print(test.shape)



