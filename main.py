"""
Imagina que esta API es una biblioteca de pelicular:
La función load_movies() es como un bibliotecario que carga el catalogo de 
libros (peliculas) cuando se abre la biblioteca
la función get_movies() muestra todo el catalogo cuando alguien lo pide.
la función get_movies(id) es como si alguien preguntara por un libro especifico po su codigo de identificación.
la función chatbot 8query es un asistente que busca libros segun palabras claves y sinonimos
la funcion get_movies_by_category (cagory) ayuda a encontrar peliculas segun su genero (acción, comedia, etc).
"""
#importamos las herramientas necesarias para construir nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse # HTTPResponse para paginas web, JSCNesponse para respuestas en formato JSCN
import pandas as pd # pandas nosayuda a manejar datos en tablas como si fuera un excel
import nltk #NLTK es una libreria para procesar texto y analizar palabras
from nltk.tokenize import word_tokenize #se usa para dividir un texto en palabras individuales
from nltk.corpus import wordnet #nos ayuda a encontrar sinonimos de palabra

# indicamos la ruta donde NLTK buscará los datos descargados en nuestro computador 
nltk.data.path.append('C:\Users\Usuario\AppData\Roaming\nltk_data')
#nltk.download('punkt') para descargar la carpeta de ntlk-data
#descargamos las herramientas necesarias de NLTK para el analisi de palabras

nltk.download('punit') #paquete para dividir frases en palabras
nltk.download('wordnet') # paquete para encontrar sinonimos de palabras en ingles

#funcion para cargar las peliculas desde un archivo CSV

def load_movies():
    #leemos el archivo que contiene información de la peliculas y seleccionaremos las columnas mas importantes.
    df = pd.read_csv('Dataset/netflix_titles.csv')[['show_id','title','realease_year','listed_in', 'rating',
                                                    'description']]
    
    #renombramos las columnas para que sean mas faciles de encontrar
    df.columns = ['id','title','year','category','rating','overview']
    
    #llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# cargamos las peliculas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ella.
movies_list =load_movies()

#Función para encontrar sinónimos de una palabra

def get_synonyms(word):
    # Usamos wirdnet para obtener distintas palabras que significan lo mismo.
    return{lema.name().lower() for Syn in wordnet.synsets(word) for lema in Syn.lemas()}