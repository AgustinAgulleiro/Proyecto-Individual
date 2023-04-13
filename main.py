from fastapi import FastAPI
import pandas as pd
from collections import Counter

app = FastAPI()

@app.get('/get_max_duration/{year}/{platform}/{duration_type}')
def get_max_duration(year: int, platform: str, duration_type: str):
    if not isinstance(year, int):
        raise ValueError("El valor de 'year' debe ser un número entero")
    if not isinstance(platform, str):
        raise ValueError("El valor de 'platform' debe ser una cadena de caracteres")
    if not isinstance(duration_type, str):
        raise ValueError("El valor de 'duration_type' debe ser una cadena de caracteres")
    df = pd.read_csv("plataformas.csv")
    if platform[0] in ["h", "n", "a", "d", "H", "N", "A", "D"]:
        platform = platform.lower()[0]
        duration_type = duration_type.lower()
        if duration_type == "min":
            resultado = df[(df['release_year']==year) & (df['id'].str.startswith(platform)) & (df['duration_type']== duration_type) & (df["type"] == "movie")]
            idx = resultado['duration_int'].idxmax()
            return {resultado.loc[idx, 'title']}
        else:
            return {"Para saber cual fue la pelicula maxima trata de poner en duration_type min"}
    else: 
        return {"Intente usar una plataforma existente"}

@app.get('/get_score_count/{platform}/{scored}/{year}')
def get_score_count(platform: str, scored: int, year: int):
    df = pd.read_csv("plataformas.csv")
    if platform[0] in ["h", "n", "a", "d", "H", "N", "A", "D"]:
        platform = platform.lower()[0]
        respuesta = df[(df['id'].str.startswith(platform)) & (df["rating_y"]> scored) & (df["release_year"]== year) & (df["type"]== "movie")]
        cantidad = respuesta.shape[0]
        return {cantidad}
    else: 
        return {"Intente usar una plataforma existente"}

@app.get('/get_count_platform/{platform}')
def get_count_platform(platform: str):
    df = pd.read_csv("plataformas.csv")
    if platform in ["amazon", "netflix", "hulu", "disney"]:
        platform = platform.lower()[0]
        respuesta = df[(df["id"].str.startswith(platform)) & (df["type"]== "movie")]
        cantidad = respuesta.shape[0]
        return {cantidad}
    else: 
        return {"Intente usar una plataforma existente"}

@app.get('/get_actor/{platform}/{year}')
def get_actor(platform: str, year: int):
    df = pd.read_csv("plataformas.csv")
    if platform[0] in ["h", "n", "a", "d", "H", "N", "A", "D"]:
        platform1 = platform
        platform = platform.lower()[0]
        df = df[(df['id'].str.startswith(platform)) & (df['release_year'] == year)]
        actores_por_fila = df['cast'].dropna().apply(lambda x: [i.strip() for i in x.split(',') if i.strip() and not i.strip().isdigit()])
        contador_actores = Counter()
        for actores in actores_por_fila:
            contador_actores.update(actores)
        actor_mas_repetido = contador_actores.most_common(1)[0][0]
        cantidad_actor_mas_repetido = contador_actores[actor_mas_repetido]
        return f"El actor que aparece más veces es {actor_mas_repetido}, con {cantidad_actor_mas_repetido} apariciones, en el año {year} de la plataforma {platform1}"
    else:
        return f"Los valores ingresados son incorrectos intente nuevamente, recuerde que las plataformas son Netflix, Amazon, Disney o Hulu."

@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str,pais: str,anio: int):
    if not isinstance(tipo, str):
        raise ValueError("El valor de 'tipo' debe ser de caracteres")
    if not isinstance(pais, str):
        raise ValueError("El valor de 'platform' debe ser una cadena de caracteres")
    if not isinstance(anio, int):
        raise ValueError("El valor de 'duration_type' debe ser un entero")
    df = pd.read_csv("plataformas.csv")
    tipo = tipo.lower()
    pais = pais.lower()
    if tipo == "tv show" or tipo == "movie":
        if pais in df["country"].unique():
            respuesta = df[(df["type"]== tipo) & (df["country"]== pais) & (df["release_year"]== anio)].shape[0]
            return {'pais': pais,
                    'anio': anio,
                    'peliculas': respuesta}
        else:
            return {f"Intenta poner un pais correcto"}
    else:
        return {f"Intenta poner tv show o movie en lugar de {tipo}"}
