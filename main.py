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
from nltk.tokenize  import word_tokenize #se usa para dividir un texto en palabras individuales
from nltk.corpus import wordnet #nos ayuda a encontrar sinonimos de palabra

# indicamos la ruta donde NLTK buscará los datos descargados en nuestro computador 
nltk.data.path.append()

#descargamos las herramientas necesarias de NLTK para el analisi de palabras

nltk.download('punit') #paquete para dividir frases en palabras
nltk.download('wordnet') # paquete para encontrar sinonimos de palabras en ingles

#funcion para cargar las peliculas desde un archivo CSV

def load_movies():
    