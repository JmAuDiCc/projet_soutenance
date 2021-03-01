from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
from datetime import datetime,date,timedelta  
import time
import dateparser

headers = {'User-Agent': 'Mozilla/5.0'}

def scrap_monde(day):
    global headers
    numero_page=1
    e = False
    liste_titre = []
    while not e:
        try:
            
            day_str = day.strftime('%d-%m-%Y')
            url = "https://www.lemonde.fr/archives-du-monde/"+day_str+"/"+str(numero_page)+"/"
            req = Request(url , headers=headers)
            page = soup( urlopen(req).read() , "lxml")
            for titre in page.find('section').findAll('h3',{ 'class':"teaser__title"}):
                liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' '))
            numero_page +=1
            
        except Exception:
            e=True
            
    return liste_titre


def scrap_closer(day):
    global headers
    liste_titre = []
    day_str = day.strftime('%Y/%m/%d')
    url = "https://www.closermag.fr/archives/"+day_str
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    for titre in page.findAll('div',{ 'class':"inner"}):
        liste_titre.append(titre.find('h2',{ 'class':"title"}).getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' '))

        
    return liste_titre


def scrap_figaro(day):
    global headers 
    liste_titre = []
    day_str = day.strftime('%Y%m/%d')
    url = "https://articles.lefigaro.fr/"+day_str+"/"
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    for titre in page.find('ul',{ 'class':"list-group"}).findAll('li',{'class':'list-group-item'}):
        liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' ').replace("\n", ""))
        
    return liste_titre


def scrap_gorafi(day):
    global headers
    liste_titre = []
    day_str = day.strftime('%Y/%m/%d/')
    url = "http://www.legorafi.fr/"+day_str
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    for titre in page.find('div',{'class':'articles'}).findAll('h2'):
        liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' '))
    return liste_titre


def scrap_nord_presse(day):
    global headers
    liste_titre = []
    day_str = day.strftime('%Y/%m/%d/')
    url = "https://nordpresse.be/"+day_str
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    for titre in page.find('ul',{'class':'mvp-blog-story-list left relative infinite-content'}).findAll('h2'):
        liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' '))
    return liste_titre

def scrap_le_point(day):
    global headers
    liste_titre = []
    day_str = day.strftime('%m-%Y/%d')
    url = "https://www.lepoint.fr/archives/"+day_str+".php"
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    for titre in page.findAll('h2',{'class':'art-title'}):
        liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' ').strip())
    return liste_titre


def scrap_libe(day):
    global headers
    liste_titre = []
    day_str = day.strftime('%Y/%m/%d')

    url = "https://www.liberation.fr/archives/"+day_str
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    titres = page.find('div',{ 'class':"custom-card-list"}).findAll('h2',{ 'class':"font_tertiary font_xs font_normal"})
    for titre in titres:
        liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' ').replace(u'\u200a', u' ').strip())
    return liste_titre


def scrap_public(day) :
    global headers
    liste_titre = []
    day_str = day.strftime('%Y/%m/%d')
    url = "https://www.public.fr/Archives/liste/"+day_str
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    for titre in page.findAll('a',{'class':'News-title News-title--small-onlymobile'}):
        liste_titre.append(titre.get('title').strip())
    return liste_titre 


def scrap_sience_avenir(day):
    global headers
    liste_titre = []
    day_str = day.strftime('%Y/%m/%d')
    url = "https://www.sciencesetavenir.fr/index/"+day_str+"/"
    req = Request(url , headers=headers)
    page = soup( urlopen(req).read() , "lxml")
    liste_balise = page.find('div',{ 'class':"bottom"}).findAll('h2')
    if liste_balise:
        for titre in liste_balise:
            liste_titre.append(titre.getText().strip())
    return liste_titre  


def recup_listes_charlie(day):
    liste_titre = []
    liste_date = []
    liste_th = []
    
    liste_themes = ['politique','international','societe','ecologie','economie','sciences','culture','religions']
    for theme in liste_themes: 
        liste_pages = []
        numero_page=1
        global headers
        last_day = day + timedelta(days=1) 
        
        while day < last_day:
            url = "https://charliehebdo.fr/themes/"+theme+'/page/'+str(numero_page)+'/'
            req = Request(url , headers=headers)
            page = soup( urlopen(req).read() , "lxml")
            
            dates = page.find('ul',{"class":'d-flex flex-row flex-wrap p-0 m-0'}).findAll('span',{'class':'ch_post_date content-block__author'})
            last_day =  dateparser.parse(dates[-1].getText().strip()).date()
            titres = page.find('ul',{"class":'d-flex flex-row flex-wrap p-0 m-0'}).findAll('h3')
            
            for titre,date in zip (titres,dates):
                
                liste_titre.append(titre.getText().encode('utf-8').decode('utf-8').replace(u'\xa0', u' ').replace(u'\u2009', u' '))
                liste_date.append(dateparser.parse(date.getText().strip()).date())
                liste_th.append(theme)
            
            #liste_pages.append(page)
            
            numero_page+=1
        #dic_theme[theme] = liste_pages
    #return dic_theme
    return liste_titre,liste_date,liste_th


def scrap_charlie(day,tuple_listes):
    
    liste_titre = []
    liste_th = []
    for titre,date,th in zip (tuple_listes[0],tuple_listes[1],tuple_listes[2]):
        if date==day:
            liste_titre.append(titre)
            liste_th.append(th)
    return liste_titre,liste_th


