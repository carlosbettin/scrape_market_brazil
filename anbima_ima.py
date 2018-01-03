def get_anbima():
    
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
        
        yld_tup = (INDICE,'YLD',DT_REF,YLD)
        dur_tup = (INDICE,'DUR',DT_REF,DUR)
        niv_tup = (INDICE,'CLS',DT_REF,CLS)
        lst.append(yld_tup)
        lst.append(dur_tup)
        lst.append(niv_tup)
        
    return lst
