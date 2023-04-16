
# Proyecto Plataformas

El Proyecto Plataformas incluye Machine Learning y Data Engineer.  
Este proyecto consiste en solucionar un problema de negocios. Crear un modelo de **`Machine Learning`** en base a un sistema de recomendaciones basado en  tipo item-item.

Y pasar por diferentes dificultades haciendo una limpieza en los archivos recibidos mediantes procesos de **`ETL`**  y definir diferentes parametros para llegar al lanzamiento del **`Modelo`**.

## Requisitos
Todas las librerias estan en el archivo requierements.txt y puede ejecutar el siguiente comando.

``` bash
pip install requierements.txt
```
## Contenidos del Repositorio:

+ En el notebook `Proyecto.ipynb` se encuentra el código comentado paso por paso, explicando las decisiones tomadas a la hora de encarar este proyecto;
Lo realice de esta manera para que estuviera ordenado, se entendienda el paso a paso de lo que fui aplicando y explicando.
Con esto espero documentar y demostrar el desarrollo del proyecto.

+ En el notebook `EDA y Modelado MC.ipynb` se encuentra un pequeño analisis del dataset generado previamente por el ETL, y tambien encuentra un pequeño ETL y EDA extra para poder configurar mi sistema de recomendacion de la manera mas optima.

+ En el archivo `main.py` se encuentran todas las funciones configuradas de la API listas para hacer que se instancien los decoradores de la API para luego hacer el deploy.
 
+ En los archivos CSV `plataformas.csv` y `Modelo-MC.csv` se encuentran los DataSet trabajados o Dataset finales que se usan para la implementacion de las funciones de la API.

+ El archivo `requirements.txt` en el cual se encuentra las librerias utilizadas para el deploy.

### ANALISIS EXPLORATORIO
--- 
- Actividades
    - La duracion maxima de cierta plataforma referente al año
    - Cantidad de peliculas referente a una mayor puntuacion dada dependiendo del año y la plataforma
    - Total de peliculas en cierta Plataforma
    - Actor que mas participacion tuvo en cierto año
    - Cantidad de peliculas lanzadas en cierto año referente a X pais

## Herramientas utilizadas:

+ VSC.

+ Python.

+ Render.

+ FastAPI.

## Librerias utilizadas:
- pandas - matplotlib - seaborn - uvicorn - scikit-learnuvicorn - scikit-learn
- collections (Counter) - TfidfVectorizer - cosine_similarity

## Autor
--- 
- [Agustin Agulleiro](https://www.linkedin.com/in/agustin-agulleiro/) (Data engineer)