# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 09:06:24 2021

@author: Alogon
"""
from gmg import gmg
import requests
from bs4 import BeautifulSoup
import time

def main():
    def get_dict_ayuntamientos_cdp():
        global lista_ayuntamientos
        lista_ayuntamientos = ['Ferrol','Santiago de Compostela','Vilaboa','Lugo','Ourense','Oleiros','Viveiro','Pontevedra','Vigo','Arteixo']
        URL_ayuntamiento = 'https://irdgcdinfo.data.blog/ayuntamientos/'
        url_ayuntamiento = requests.get(URL_ayuntamiento)
        html = BeautifulSoup(url_ayuntamiento.text,'html.parser')
        #print(html)
        columnas_html = html.find_all('th')
        lcp = []
        lnom = []
        for td in columnas_html:
            x = td.text
            
            if x.isdecimal() == True:
                lcp.append(x)
                
            else:
                if x == 'Nome do concello' or x == 'Identificador':
                    pass
                else:
                    lnom.append(x)
                    
        return dict(zip(lcp, lnom))
    #print(d.get('36058'))
    d = get_dict_ayuntamientos_cdp()
    def get_clave(d,i):
        for clave, valor in d.items(): 
            if valor == i:
                return clave
    
    def get_lista_cdp(d):
        lista_cp_ayuntamientos = []
        for i in lista_ayuntamientos:
            lista_cp_ayuntamientos.append(get_clave(d,i))
        return lista_cp_ayuntamientos
    
    lista_cp_ayuntamientos = get_lista_cdp(d)
    
    lista_datos = []
    for k in lista_cp_ayuntamientos:
        meteog_url = requests.get("http://servizos.meteogalicia.gal/rss/predicion/jsonPredConcellos.action?idConc={}".format(k))
        meteo_json = meteog_url.json()
        cielo = meteo_json["predConcello"]["listaPredDiaConcello"][0]['ceo']['manha']
    
        URL_codigos = 'https://irdgcdinfo.data.blog/codigos/'
        url_codigos = requests.get(URL_codigos)
        htmlcodigos = BeautifulSoup(url_codigos.text,'html.parser')
        columnascodigo_html = htmlcodigos.find_all('th')
        lcm = []
        lci = []
        
        for td in columnascodigo_html:
            x = td.text
            
            if x.isdecimal() == True:
                lcm.append(x)
                
            else:
                if x == 'Valor numérico' or x == 'Descrición do estado do ceo':
                    pass
                else:
                    lci.append(x)
                    
        c = dict(zip(lcm, lci))
        estado = (c.get('{}'.format(cielo)))
        
        #print('En {} con código {} o día é {}'.format(d.get(k),k,estado))
        
        localizacion = requests.get('https://eu1.locationiq.com/v1/search.php?key=pk.791b519936c75085e5967c97a617ec98&q=Spain,Galicia,{}&format=xml'.format(d.get(k)))
        location = BeautifulSoup(localizacion.content,'lxml')
        cord_loc = location.select('place')
        #print(cord_loc)
        f = []
        
        def get_max_index(cord_loc):
            for i in range(len(cord_loc)):
                cord_loc1 = location.select('place')[i]
                c = cord_loc1.get('importance')
                f.append(c)
            return f.index(max(f))
            
        cord_loc3 = location.select('place')[get_max_index(cord_loc)]
        latitud = cord_loc3.get('lat')
        longitud = cord_loc3.get('lon')
        importancia = cord_loc3.get('importance')
        print('En {} con código {} e coordenadas {}, {} o día é {}'.format(d.get(k),k,latitud, longitud, estado))
        #time.sleep(1) No se considera necesario 
        lista_datos1 = (cielo,(longitud, latitud))
        lista_datos.append(lista_datos1)

        
    gmg.plotMap(points = lista_datos)


if __name__=='__main__':
    main()

















