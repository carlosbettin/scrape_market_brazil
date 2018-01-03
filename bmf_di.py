# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 09:37:46 2017

@author: carlos.bettin
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import mssql_python as mp
import datetime
import pandas as pd

def bmf_values():
    
    date = yesterday()
    id_tup = bmf_sel(date)
    
    yields = [((100000/i[3])**(252/i[2])-1,i[0],'YLD',date.strftime('%Y-%m-%d')) for i in id_tup if i[2]!=0]
    dc = [(i[2],i[0],'DC',date.strftime('%Y-%m-%d')) for i in id_tup if i[2]!=0]
    lst = yields+dc
    
    return lst

def yesterday():
    
    df = pd.read_excel('feriados_nacionais.xls')
    df = df.iloc[:936,0].values
    
    dates, i = [], 1
    while len(dates) <= 0: 
        tmp = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=i)
        if tmp.weekday() == 6: i+=2
        elif tmp.weekday() == 5: i+=1
        elif tmp in df: i+=1
        else: 
            dates.append(tmp)
            i+=1
    yesterday = dates[0] 
    return yesterday


def bmf_sel(date):
    
    df = pd.read_excel('feriados_nacionais.xls')
    df = df.iloc[:936,0].values
    
    lista = [date]
    i = 1
    while len(lista) <5000 :
        tmp = date + datetime.timedelta(days=i)
        if tmp.weekday() == 5: i+=2
        elif tmp.weekday() == 6: i+=1
        elif tmp in df: i+=1
        else: 
            lista.append(tmp)
            i+=1      
        
    bmf_date = date.strftime('%m/%d/%Y') 
    query = mp.read_di1()
        
    browser = webdriver.PhantomJS()
    url = "http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-sistema-pregao-enUS.asp?Data="+ bmf_date +"&Mercadoria=DI1"
    browser.get(url) #navigate to the page
    soup = BeautifulSoup(browser.page_source, 'lxml')
    
    index = ['DI1'+i.text[0:-1] for i in soup.td.find_all('td')]

    set_price = []  
    for i in soup.find(id='MercadoFut2').find_all('tr')[1:]:
        set_price.append(i.find_all('td')[7].text.replace(',',''))
    
    bmf_dic = {k : float(v) for k, v in zip(index, set_price)}
    
    id_tup = [(i[1],i[0],lista.index(datetime.datetime.strptime(i[2], '%Y-%m-%d')),bmf_dic[i[0]]) for i in query]
    
    return id_tup
