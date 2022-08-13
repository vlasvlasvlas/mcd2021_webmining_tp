import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import sys, os
import json

## diario ambito 
# h2 a href value

# request
url = 'https://www.ambito.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, headers=headers)
 
# page
page = BeautifulSoup(response.text, 'html.parser')

# extract 
page_titulos = page.select('h2 a[href]')

# dict
noticias_ambito = []

# append
for a in page_titulos:
  noticia = a.get_text().replace('"','').replace('“','').replace('”','').replace("'",'')
  noticias_ambito.append(noticia)

# json
diario_ambito = {
    'fecha':str(date.today()),
    'origen':url,
    'noticias':noticias_ambito
}




## diario pagina12
#https://www.pagina12.com.ar/
#class="article-title "

# request
url = 'https://www.pagina12.com.ar/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, headers=headers)

# page
page = BeautifulSoup(response.text, 'html.parser')

# extract
page_titulos = page.find_all('div', {"class": "article-title "})

# dict 
noticias_pagina12 = []

# append
for a in page_titulos:
  noticia = a.get_text().replace('"','').replace('“','').replace('”','').replace("'",'')
  noticias_pagina12.append(noticia)

# json 
diario_pagina12 = {
    'fecha':str(date.today()),
    'origen':url,
    'noticias':noticias_pagina12
}



## clarin
#https://www.clarin.com/

#class="link_article"

# request
url = 'https://www.clarin.com'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, headers=headers)

# page
page = BeautifulSoup(response.text, 'html.parser')

# extract
page_titulos = page.select('div.mt h2')


# dict 
noticias_clarin = []

# append
for a in page_titulos:
  noticia = a.get_text().replace('"','').replace('“','').replace('”','').replace("'",'')
  noticias_clarin.append(noticia)

# json 
diario_clarin = {
    'fecha':str(date.today()),
    'origen': url,
    'noticias':noticias_clarin
}



if not os.path.exists('data_noticias'):
    os.makedirs('data_noticias')

# clarin
filejson = str(date.today())+"_clarin.json"

with open('data_noticias/'+filejson, 'w') as f:
    json.dump(diario_clarin, f, ensure_ascii=False, indent=4)


# clarin
filejson = str(date.today())+"_pagina12.json"

with open('data_noticias/'+filejson, 'w') as f:
    json.dump(diario_pagina12, f, ensure_ascii=False, indent=4)    


# clarin
filejson = str(date.today())+"_ambito.json"

with open('data_noticias/'+filejson, 'w') as f:
    json.dump(diario_ambito, f, ensure_ascii=False, indent=4)        

print("executed:"+datetime.now().isoformat())