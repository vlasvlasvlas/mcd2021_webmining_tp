# -*- coding: utf-8 -*-
"""Analizar_noticias_diarios.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GCvCBj4YcVjaqcHqAPQRSUNQVBcMwT2z

# Importación datos de diarios

última actualización: 24/9/2022

- se actualizó para que trabje con los últimos 7 días
- se acomodó el datafram final, se sumo tanto noticiaes_es como noticias_en

- Importación de librerías
"""

# para poder traer las noticias del repo
from base64 import encode
import json
import os, sys

# para poder usar regex
import re

# pandas
import pandas as pd

# fechas
from datetime import datetime, timedelta

"""- instalación de translators"""

# traductor
# from googletrans import Translator
# translator = Translator(service_urls=['translate.googleapis.com'])
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="es", target="en")


# from google_trans_new import google_translator
# translator = google_translator()

# nlp: nltk
import nltk

nltk.download("vader_lexicon")
nltk.download("punkt")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize

analizador = SentimentIntensityAnalyzer()

"""- Import de datos de diarios JSON recolectados con Github Actions"""

user = "vlasvlasvlas"
repo = "mcd2021_webmining_tp"

# remove local directory if it already exists
"""- se trabaja con los últimos diarios """

# nos quedamos con las fechas de los archivos json para seleccionar los más recientes
directory = "data_noticias"
dates = []
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        dates.append(filename[:10])
print("dates:", len(dates))

# busco la fecha más reciente
cantdias = 30
date_to = max(dates, key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
date_from = datetime.today() - timedelta(days=cantdias)
date_from = date_from.date()

# última semana
rangofecha = pd.date_range(start=date_from, end=date_to)

# me quedo con los archivos de la última fecha más reciente
diarios_ultimasemana = []

for date in rangofecha:
    iterafecha = date.date()
    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename.startswith(str(iterafecha)):
            diarios_ultimasemana.append(filename)

diarios_ultimasemana

"""- se prepara el dataframe de los diarios"""

# defino los regex para asegurarme que me se estan guardan las noticias correctas
p_a = re.compile(".*ambito.*")
p_c = re.compile(".*clarin.*")
p_p = re.compile(".*pagina12.*")


# cargando los json por diario al dataframe
prefixfolder = "data_noticias/"

datos_ambito = []
datos_clarin = []
datos_pagina = []

for s in diarios_ultimasemana:
    folderfile = prefixfolder + s

    # ambito
    if p_a.match(folderfile):
        f = open(folderfile, encoding="utf8")
        datos_ambito.append(json.load(f))

    # clarin
    if p_c.match(folderfile):
        f = open(folderfile, encoding="utf8")
        datos_clarin.append(json.load(f))

    # pagina12
    if p_p.match(folderfile):
        f = open(folderfile, encoding="utf8")
        datos_pagina.append(json.load(f))


def analizar(dic_noticias, fuente_nombre):

    global df_noticias

    print("\n -----> fuente ", fuente_nombre, " - fecha ", dic_noticias["fecha"])
    nombre_diario = dic_noticias["origen"]
    lista_noticias = dic_noticias["noticias"]

    lista_noticias_en = []

    # traduce noticias al ingles
    for noticia in lista_noticias:
        # texto_temp = translator.translate(noticia, dest='en').text
        # texto_temp = translator.translate(noticia, lang_src='es', lang_tgt='en')
        texto_temp = translator.translate(noticia)
        print(texto_temp)
        lista_noticias_en.append(texto_temp)

    scores_lista = []

    # analiza noticias ingles
    for noticia in lista_noticias_en:
        scores = analizador.polarity_scores(noticia)
        scores_lista.append(scores["compound"])

    df_temp = pd.DataFrame()

    df_temp["noticia_es"] = lista_noticias
    df_temp["noticia_en"] = lista_noticias_en
    df_temp["puntaje"] = pd.to_numeric(scores_lista)

    df_temp = df_temp.assign(fecha=dic_noticias["fecha"])
    df_temp = df_temp.assign(fuente_nombre=fuente_nombre)
    df_temp = df_temp.assign(fuente_url=nombre_diario)

    df_noticias = df_noticias.append(df_temp, ignore_index=True)


# defino el dataframe para guardar las noticias
df_noticias = pd.DataFrame()
df_noticias["fecha"] = None
df_noticias["fuente_nombre"] = None
df_noticias["fuente_url"] = None
df_noticias["noticia_es"] = None
df_noticias["noticia_en"] = None
df_noticias["puntaje"] = None

# cargo datos y resultados del análisis a dataframe
for datadia in datos_ambito:
    analizar(datadia, "ambito")

for datadia in datos_clarin:
    analizar(datadia, "clarin")

for datadia in datos_pagina:
    analizar(datadia, "pagina")

df_noticias.fuente_nombre.value_counts()
df_noticias.to_csv("analisis_30dias.csv", encoding="utf8", mode="w+", index=False)
print(df_noticias)