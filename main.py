import pandas as pd
from fastapi import FastAPI
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.get('/get_max_duration/{year}/{platforma}/{dtype}')
def get_max_duration(year: int, platforma: str, dtype: str):
    if not isinstance(year, int):
        raise ValueError("El valor de 'year' debe ser un número entero")
    if not isinstance(platform, str):
        raise ValueError("El valor de 'platform' debe ser una cadena de caracteres")
    if not isinstance(dtype, str):
        raise ValueError("El valor de 'duration_type' debe ser una cadena de caracteres")
    df = pd.read_csv("plataformas.csv")
    if platforma[0] in ["h", "n", "a", "d", "H", "N", "A", "D"]:
        platform = platforma.lower()[0]
        duration_type = dtype.lower()
        if duration_type == "min":
            resultado = df[(df['release_year']==year) & (df['id'].str.startswith(platform)) & (df['duration_type']== duration_type) & (df["type"] == "movie")]
            idx = resultado['duration_int'].idxmax()
            respuesta = resultado.loc[idx, 'title']
            return {'pelicula': respuesta}

        else:
            return {"Para saber cual fue la pelicula maxima trata de poner en duration_type min"}
    else: 
        return {"Intente usar una plataforma existente"}

@app.get('/get_score_count/{platforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: int, anio: int):
    df = pd.read_csv("plataformas.csv")
    if plataforma[0] in ["h", "n", "a", "d", "H", "N", "A", "D"]:
        plataform = plataforma.lower()[0]
        respuesta = df[(df['id'].str.startswith(plataform)) & (df["rating_y"]> scored) & (df["release_year"]== anio) & (df["type"]== "movie")]
        respuesta = respuesta.shape[0]
        return {
        'plataforma': plataforma,
        'cantidad': respuesta,
        'anio': anio,
        'score': scored}
    else: 
        return {"Intente usar una plataforma existente"}

@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):
    df = pd.read_csv("plataformas.csv")
    if plataforma in ["amazon", "netflix", "hulu", "disney"]:
        platform = plataforma.lower()[0]
        respuesta = df[(df["id"].str.startswith(platform)) & (df["type"]== "movie")]
        respuesta = respuesta.shape[0]
        return {'plataforma': plataforma, 'peliculas': respuesta}
    else: 
        return {"Intente usar una plataforma existente"}

@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
    if not isinstance(plataforma, str):
        raise ValueError("El valor de 'platform' debe ser de caracteres")
    if not isinstance(anio, int):
        raise ValueError("El valor de 'year' debe ser un entero")
    df = pd.read_csv("plataformas.csv")
    if plataforma[0] in ["h", "n", "a", "d", "H", "N", "A", "D"]:
        plataform = plataforma.lower()[0]
        df = df[(df['id'].str.startswith(plataform)) & (df['release_year'] == anio)]
        actores_por_fila = df['cast'].dropna().apply(lambda x: [i.strip() for i in x.split(',') if i.strip() and not i.strip().isdigit()])
        contador_actores = Counter()
        for actores in actores_por_fila:
            contador_actores.update(actores)
        respuesta = contador_actores.most_common(1)[0][0]
        respuesta1 = contador_actores[respuesta]
        return {
        'plataforma': plataforma,
        'anio': anio,
        'actor': respuesta,
        'apariciones': respuesta1}
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
                    'contenido': respuesta}
        else:
            return {f"Intenta poner un pais correcto"}
    else:
        return {f"Intenta poner tv show o movie en lugar de {tipo}"}

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    df = pd.read_csv("plataformas.csv")
    res = df[df["rating_x"]== rating]
    respuesta = res.shape[0]
    return {'rating': rating, 'contenido': respuesta}

@app.get('/get_recomendation/{title}')
def get_recommendationB(title: str):
    df= pd.read_csv("Modelo-MC.csv")
    title = title.lower()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    idx = df.index[df['title'] == title.lower()].tolist()[0]
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [i for i in sim_scores if i[0] != idx]
    sim_scores = sorted(sim_scores, key=lambda x: df['score'].iloc[x[0]], reverse=True)[:5]
    respuesta = df.iloc[[i[0] for i in sim_scores]]['title'].tolist()
    return {'recomendacion': respuesta}