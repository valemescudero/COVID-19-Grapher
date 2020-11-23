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
from datetime import date


df = pd.read_csv("full_data.csv")


def get_countries():
  next = '0'
  newcountries=[]

  while next != '3':
    print("1. Ingresar país")
    print("2. Resetear países")
    print("3. Volver al menú principal")
    next = input("")
    if next == '1':
      new_country = input("Ingresá el nombre del país (en inglés)").capitalize()
      full_country_list = list(df["location"])
      if new_country in full_country_list:
        print("Pais agregado:", new_country)
        newcountries.append(new_country)
      else:
        print("El país no se encuentra en la lista") 
    elif next == '2':
      newcountries = []
    elif next == '3':
      return newcountries
    else:
      print("Opción inválida")

def get_time_frame():
  dates=['start', 'end']
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
  return dates


def get_cases(selected_country):
  cases_dates = list(selected_country["data"]["date"])
  cases = list(selected_country["data"]["total_cases"])
  plt.plot_date(cases_dates,cases, linestyle="solid", label=selected_country["name"])

def get_deaths(selected_country):
  deaths_dates = list(selected_country["data"]["date"])
  deaths = list(selected_country["data"]["total_deaths"])
  plt.plot_date(deaths_dates,deaths, linestyle="solid", label=selected_country["name"])

def crear_cruces(first_country, second_country, option):  
  x_first_country = list(first_country["data"]["date"])
  x_second_country = list(second_country["data"]["date"])

  y_first_country = list(first_country["data"][f"total_{option}"])
  y_second_country = list(second_country["data"][f"total_{option}"])

  crucex = []
  crucey = []
  

  for i in range(1, len(x_first_country)):
    if (y_first_country[i] == y_second_country[i]) or (y_first_country[i] > y_second_country[i] and y_first_country[i-1] < y_second_country[i-1]) or (y_first_country[i] < y_second_country[i] and y_first_country[i-1] > y_second_country[i-1]):
      crucex.append(x_second_country[i])
      crucey.append(y_second_country[i])

  plt.plot(crucex,crucey, 'ro')

    

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
      countries = get_countries()
      print("Paises:", countries)
    elif option == '2':
      dates = get_time_frame() 
      for i in range(len(countries)): 
        countrydata = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == countries[i])]
        countries[i] = {"name": countries[i], "data": countrydata}
    elif option == '3':
      for country in countries:
        get_cases(country)
      for i in range(len(countries)-1):
        for j in range(1,len(countries)):
          crear_cruces(countries[i], countries[j], "cases")
      plt.legend()
      plt.show()
      break
    elif option == '4':
      for country in countries:
        get_deaths(country)
      for i in range(len(countries)-1):
        for j in range(1,len(countries)):
          crear_cruces(countries[i], countries[j], "deaths")
      
      plt.legend()
      plt.show()
      break
    elif option == '5':
      break
    else:
      print("Opción inválida")
      break


programa()
