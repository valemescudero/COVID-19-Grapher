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



def get_countries(countries, countries_data):
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
      countries_data = []
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



def get_cases(selected_country, dates, countries_data):
  country = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == selected_country)]
  countries_data.append(country)
  cases_dates = list(country["date"])
  cases = list(country["total_cases"])
  plt.plot(cases_dates,cases, linestyle="solid", label=selected_country)
    

def get_deaths(selected_country, dates, countries_data):
  country = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == selected_country)]
  countries_data.append(country)
  deaths_dates = list(country["date"])
  deaths = list(country["total_deaths"])
  plt.plot_date(deaths_dates,deaths, linestyle="solid")
    

  
    
    
def crear_cruces(first_country, second_country, option):
  print(first_country)

  x_first_country = [first_country["Date"][0]]
  x_second_country = [second_country["Date"][0]]
  if option == 3:
    y_first_country = [first_country["total_cases"][0]]
    y_second_country = [first_country["total_cases"][0]]
  else:
    y_first_country = [first_country["total_deaths"][0]]
    y_second_country = [first_country["total_deaths"][0]]
  crucex = []
  crucey = []
  
  for i in range(1, len(first_country["Date"])):
    x_first_country.append(first_country["Date"][i])
    x_second_country.append(first_country["Date"][i])
    if option == 3:
      x_first_country.append(first_country["total_cases"][i])
      x_second_country.append(first_country["total_cases"][i])
    else:
      x_first_country.append(first_country["total_deaths"][i])
      x_second_country.append(first_country["total_deaths"][i])
        
  if (y_first_country[i] == y_second_country[i]) or (y_first_country[i] > y_second_country[i] and y_first_country[i-1] < y_second_country[i-1]) or (y_first_country[i] < y_second_country[i] and y_first_country[i-1] > y_second_country[i-1]):
    crucex.append(x_second_country[i])
    crucey.append(y_second_country[i])

  plt.plot(x_second_country,y_second_country)
  plt.plot(x_first_country,y_first_country)
  plt.plot(crucex,crucey, 'k.')
  plt.xticks(x_second_country[::100], rotation=60)
    

def programa():
  option = '0'
  countries = []
  countries_data = []
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
      get_countries(countries, countries_data)
    elif option == '2':
      get_time_frame(dates)
    elif option == '3':
      for country in countries:
        get_cases(country, dates, countries_data)
      for i in range(len(countries)-1):
        for j in range(len(countries)):
            crear_cruces(countries_data[i], countries_data[j], option)
      plt.legend()
      plt.show()
    elif option == '4':
      for country in countries:
        get_deaths(country, dates, countries_data)
      for i in range(len(countries)-1):
        for j in range(len(countries)):
            crear_cruces(countries_data[i], countries_data[j], option)
      plt.legend()
      plt.show()
    elif option == '5':
      break
    else:
      print("Opción inválida")
      break


programa()
