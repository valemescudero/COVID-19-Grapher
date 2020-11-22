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



def get_countries(countries):
  next = '0'

  while next != '3':
    print("1. Ingresar país")
    print("2. Resetear países")
    print("3. Volver al menú principal")
    next = input("")
    if next == '1':
      country = input("Ingresá el nombre del país (en inglés)").capitalize()
      countries.append(country)
    elif next == '2':
      countries = []
    elif next == '3':
      return
    else:
      print("Opción inválida")

def get_time_frame(dates):
    print("1. Modificar rango de tiempo")
    print("2. Volver al menú principal")
    next = input("")
    if next == '1':
      dates[0] = input("Ingresá fecha de inicio en formato aaaa-mm-dd")
      dates[1] = input("Ingresá fecha de límite en formato aaaa-mm-dd")
    elif next == '2':
        return
    else:
      print("Opción inválida")



def get_cases(selected_country, dates):
  country = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == selected_country)]
  dates = list(country["date"])
  cases = list(country["total_cases"])
  plt.plot(dates,cases, linestyle="solid", label=selected_country)
    

def get_deaths(selected_country, dates):
  country = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == selected_country)]
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
  option = '0'
  countries = []
  dates = ['start', 'end']

  while option != '5':
    print("GRAFICADOR COVID-19\n")
    print("Ingrese una opción para continuar:")
    print("1. Modificar países de consulta")
    print("2. Modificar rango de tiempo")
    print("3. Consultar casos totales")
    print("4. Consultar muertes totales")
    print("5. Salir")
    option = input("")

    if option == '1':
      get_countries(countries)
    elif option == '2':
      get_time_frame(dates)
    elif option == '3':
      for country in countries:
        get_cases(country, dates)
      plt.legend()
      plt.show()
    elif option == '4':
      for country in countries:
        get_deaths(country, dates)
      plt.legend()
      plt.show()
    elif option == '5':
      break
    else:
      print("Opción inválida")
      break


programa()
