import requests

def wget(url):
    r = requests.get(url, allow_redirects=True)
    with open(url[url.rfind('/') + 1::], 'wb') as f:
        f.write(r.content)

wget("https://covid.ourworldindata.org/data/ecdc/full_data.csv")

! wget "https://covid.ourworldindata.org/data/ecdc/full_data.csv"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("full_data.csv")


def get_cases(selected_country, start_date, end_date):
  country = df[(df["date"].between(start_date, end_date))&(df["location"] == selected_country)]
  dates = list(country["date"])
  cases = list(country["total_cases"])
  plt.plot(dates,cases, linestyle="solid", label=selected_country)
    

def get_deaths(selected_country, start_date, end_date):
  country = df[(df["date"].between(start_date, end_date))&(df["location"] == selected_country)]
  dates = list(country["date"])
  deaths = list(country["total_deaths"])
  plt.plot_date(dates,deaths, linestyle="solid")
    
    
def crearCruces(x_dias1, y_datos1, x_dias2, y_datos2):
  dict01 = {}
  dict02 = {}
  x_fechas  = []
  y_valores = []
  fechas = []

  for x in range(len(y_datos1)):
    dict01[x_dias1[x]] = y_datos1[x]

  for x in range(len(y_datos2)):
    dict02[x_dias2[x]] = y_datos2[x]

  fechas = [value for value in x_dias1 if value in x_dias2] 

  for x in range(len(fechas)):
    valor01 = dict01[fechas[x]]
    valor02 = dict02[fechas[x]]
    if ((valor01 >= valor02) and (dict01[fechas[x-1]] < dict02[fechas[x-1]])):
      x_fechas.append(fechas[x])
      y_valores.append((valor01 + valor02) // 2)
    elif valor01 <= valor02 and dict01[fechas[x-1]] > dict02[fechas[x-1]]:
      x_fechas.append(fechas[x])
      y_valores.append((valor01 + valor02) // 2)
  return x_fechas, y_valores


def programa():
  another_country = "si"
  deaths_or_cases = input("Qué dato queres saber? Ingresá 'casos' para ver los casos totales o 'fallecimientos' para ver las muertes")
  start_date= input("Desde qué fecha querés ver los casos? Ingresar la fecha en formato aaaa-mm-dd")
  end_date = input("Hasta qué fecha querés ver los casos? Ingresar la fecha en formato aaaa-mm-dd")
  countries = []

  while another_country=="si":
    country = input("Ingresá el país (en inglés)").capitalize()
    countries.push(country)
    another_country=input("Querés ver otro país? Responde 'si' o 'no'")

  for country in countries:
    if deaths_or_cases=="casos":
      get_cases(country,start_date,end_date)
    elif deaths_or_cases=="fallecimientos":
      get_deaths(country,start_date,end_date)
  
  plt.legend()
  plt.show()

programa()
