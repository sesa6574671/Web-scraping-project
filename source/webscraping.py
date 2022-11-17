# Importar módulos
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from numpy import random

# Creamos listados vacíos para guardar los portátiles dependiendo de las características que tengan
elementos=[]
elementos_8=[]

contador=1

while(contador<18):
  # Para cada iteración creamos un enlace nuevo
  url = "https://www.elcorteingles.es/electronica/ordenadores/portatiles/"+ str(contador)+"/"
  # Ejecutar GET-Request
  response = requests.get(url)

  # Analizar sintácticamente el archivo HTML de BeautifulSoup del texto fuente
  html = BeautifulSoup(response.text, 'html.parser')

  # Creamos un listado de elementos
  lista= html.find_all('p', class_='product_preview-desc') 
  # Creamos un listado de precios
  lista_precios=html.find_all('span', class_="price _big _sale")

  # Para cada par portátil, precio lo añadimos alos listados vacíos
  for element, precio in zip(lista, lista_precios):
    element=element.get_text().split(", ")
    element.append(precio.get_text())
    if len(element)>7 and len(element)<9:
      elementos_8.append(element)
    elif len(element)<8:
      elementos.append(element)

  contador+=1

  # Detenemos el código de forma aleatoria para no saturar el servidor
  sleep(random.randint(2,5))

# Creación de los datasets finales
df=pd.DataFrame(elementos, columns=['Nombre', 'Procesador', 'RAM', 'Disco Duro', 'Pantalla', 'SO', 'Precio'])
df_8=pd.DataFrame(elementos_8, columns=['Nombre', 'Procesador', 'RAM', 'Disco Duro', 'Tarjeta Grafica', 'Pantalla', 'SO', 'Precio'])
df_final = pd.concat([df, df_8])
df_final.to_csv('dataframe.csv',index=False, encoding='iso8859-15')