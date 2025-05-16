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
nltk.download('punkt') #para descargar la carpeta de ntlk-data
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

#creamos la aplicación FastAPI, que sera el motor de nuestra API
# Esto inicializa la API con un nombre y una version 
app = FastAPI(title="Mi Aplicación de Peliculas", version="1.0.0")

#Ruta de inicio: cuando alguien entra a la API sin especificar nada, vera un mensaje de bienvenido

@app.get('/',tags=['Home'])
def home():
    return HTMLResponse('<h1>Bienvenido a la API de Peliculas</h1>')
#obteniendo la lista de peliculas
#creamos una ruta para obtener todas las peliculas

#Ruta para obtener todas las peliculas disponibles

@app.get('/movies', tags=['Movies'])
def get_movies():
    # si hay peliculas las enviamos, si no, mostramos un error
    return movies_list or HTTPException(status_code=500, detail="No hay datos de peliculas disponibles")
    
# Ruta para obtener una pelicula especifica segun su id

@app.get('/movies/{id}', tag= ['Movies'])
def get_movie(id: str):
    #Buscamos en la lista de peliculas la que tenga el mismo ID
    return next((m for m in movies_list if m ['id'] == id), {"detalle": "pelicula no encontrada"})

#Ruta del chatbot que responde con peliculas segun las palabras claves de la categoria

@app.get('/chatbot', tags=['chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intención del usuario
    query_words = word_tokenize(query.lower())
    
    #Buscamos sinonimos de las palabras clave para ampliar la busqueda
    synonyms ={word for q in query_words for word in get_synonyms(q)} | set(query_words)
    
    #Filtramos la lista de peliculas buscando coincidencias en la categoria
    results = [m for m in movies_list if any (s in m ['category'].lower() for s in synonyms)]
    
    # Si encontramos peliculas, enviamos la lista; si no, mostramos un mensaje de que no se encontro coincidencias

    return JSONResponse(content={
        "respuesta":"Aqui tienes algunas peliculas relacionadas." if results else "No encontré peliculas en esa categoria.",
        "peliculas": results
    })

# Ruta para buscar peliculas por categoria especifica

@app.get('/movies', tags=['Movies'])
def get_movies_by_category(category: str):
    #Filtramos la lista de peliculas según la categoria ingresada
    return [m for m in movies_list if category.lower() in m['categoy'].lower()uvicorn main:app --reload]
