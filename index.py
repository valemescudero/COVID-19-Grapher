
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date


df = pd.read_csv("https://covid.ourworldindata.org/data/ecdc/full_data.csv")


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
      newcountries = "nochanges"
      return newcountries
    else:
      print("Opción inválida")

def get_time_frame():
  next = '0'
  dates = ["2020-03-21","2020-11-21"]
  while next != '2':
    print("1. Modificar rango de tiempo")
    print("2. Volver al menú principal")
    next = input("")
    if next == '1':
      dates[0] = input("Ingresá fecha de inicio en formato aaaa-mm-dd")
      dates[1] = input("Ingresá fecha de límite en formato aaaa-mm-dd")
    elif next == '2':
      return dates
    else:
      print("Opción inválida")


def get_cases(selected_country):
  cases_dates = list(selected_country["data"]["date"])
  cases = list(selected_country["data"]["total_cases"])
  
  plt.plot_date(cases_dates,cases, linestyle="solid", linewidth=1, label=selected_country["name"])
  plt.yticks([])
  plt.xticks([])

def get_deaths(selected_country):
  deaths_dates = list(selected_country["data"]["date"])
  deaths = list(selected_country["data"]["total_deaths"])

  
  plt.plot_date(deaths_dates, deaths, linestyle="solid", linewidth=1, label=selected_country["name"])
  plt.yticks([])
  plt.xticks([])

def crear_cruces(first_country, second_country, option):  
  if (option == '3'):
    deaths_or_cases = "cases"
  else:
    deaths_or_cases = "deaths"
  x_first_country = list(first_country["data"]["date"])
  x_second_country = list(second_country["data"]["date"])

  y_first_country = list(first_country["data"][f"total_{deaths_or_cases}"])
  y_second_country = list(second_country["data"][f"total_{deaths_or_cases}"])
  
  crucex = []
  crucey = []

  for i in range(1, len(x_first_country)):
    if (y_first_country[i] == y_second_country[i]) or (y_first_country[i-1] > y_second_country[i-1] and y_first_country[i] < y_second_country[i]) or (y_first_country[i-1] < y_second_country[i-1] and y_first_country[i] > y_second_country[i]):
      crucex.append(x_second_country[i])
      crucey.append(y_second_country[i])
  if crucex and crucey:
      plt.figure(figsize=(6,9))
      plt.plot(crucex,crucey, 'ko')
      plt.yticks([])
      plt.xticks([])

    

def programa():
  option = '0'
  countries = []
  countries_data = []
  dates = ["2020-06-21","2020-09-21"]

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
      countries_aux = get_countries()
      if not countries_aux:
        countries = []
      elif countries_aux == "nochanges":
        print("No se realizaron cambios")
      else:
        for country in countries_aux:
          countries.append(country)
      print("Países:", countries)
    elif option == '2':
      dates = get_time_frame() 
    elif option == '3':
      for i in range(len(countries)): 
        countrydata = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == countries[i])]
        countries_data.append({"name": countries[i], "data": countrydata})
      for country in countries_data:
        get_cases(country)
        
      for i in range(len(countries_data)-1):
        for j in range(1,len(countries_data)):
          crear_cruces(countries_data[i], countries_data[j], "cases")
          
      plt.yticks(list(countries_data[0]["data"]["total_cases"]))
      plt.xticks(list(countries_data[0]["data"]["date"]))
      plt.xticks(rotation=45)
      plt.legend()
      plt.show()
  
      break
    elif option == '4':
      for i in range(len(countries)): 
        countrydata = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == countries[i])]
        countries_data.append({"name": countries[i], "data": countrydata})
      for country in countries_data:
        get_deaths(country)
        
      for i in range(len(countries_data)-1):
        for j in range(1,len(countries_data)):
          crear_cruces(countries_data[i], countries_data[j], "cases")        
      
      plt.yticks(list(countries_data[0]["data"]["total_deaths"]))
      plt.xticks(list(countries_data[0]["data"]["date"]))
      plt.xticks(rotation=45)
      plt.legend()
      plt.show()
      break
    elif option == '5':
      break
    else:
      print("Opción inválida")
      break


programa()
