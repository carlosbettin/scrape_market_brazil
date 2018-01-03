# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 10:56:14 2018

@author: carlos.bettin
"""
import requests
import datetime
from bs4 import BeautifulSoup

def get_imas():
   
    ref = {'IMA-B':5,'IMA-B 5':4,'IMA-B 5+':6, 'IRF-M':7,'IRF-M 1':436, 'IRF-M 1+':438, 'IMA-C':439}
    
    url = 'http://www.anbima.com.br/ima/arqs/ima_completo.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')

    lst_xml = soup.find_all('FAMILIA')
    lst = []

    for i in lst_xml:
        INDICE = i['INDICE']
        DT_REF = datetime.datetime.strptime(i.find_all('TOTAIS')[0]['DT_REF'], '%d/%m/%Y').strftime('%Y-%m-%d')
       
        try:
            YLD = float(i.find_all('TOTAL')[0]['T_Yield'].replace(',','.'))/100
        except: continue
        try:
            DUR = int(i.find_all('TOTAL')[0]['T_Duration'])
        except: continue
        try:
            CLS = float(i.find_all('TOTAL')[0]['T_Num_Indice'].replace(',','.'))
        except: continue    

        yld_tup = (YLD, ref[INDICE], 'YLD', DT_REF)
        dur_tup = (DUR, ref[INDICE], 'DUR', DT_REF)
        niv_tup = (CLS, ref[INDICE], 'COT', DT_REF)
        lst.append(yld_tup)
        lst.append(dur_tup)
        lst.append(niv_tup)
        
    return lst
