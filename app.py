# imports
from facebook_scraper import get_posts
import pandas as pd
import os
import matplotlib.pyplot as plt
from SPARQLWrapper import SPARQLWrapper, JSON

os.chdir(r'D:/Andres Wilches/Estudios/Ing Sistemas/Tendencias avanzadas de ingenieria de software/Corte 1/Extraccion_datos')

# Para Facebook

likes = []
fecha = []
posts = []

for post in get_posts('mercadolibrecol',pages =7):
    likes.append(post['likes'])
    fecha.append(post['time'])
    posts.append(post)

fb_posts = pd.DataFrame(posts)
plt.plot(fecha, likes)
plt.title('Likes en el tiempo - Mercadolibre Col')
plt.savefig("likes_tiempo_MeliFb.png")

fb_posts.to_excel('mercadolibrePostsInfo.xlsx',index=False)

# Por SparQL ------------------------------------------------------------------

sparql = SPARQLWrapper(
    "http://vocabs.ardc.edu.au/repository/api/sparql/"
    "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020"
)
sparql.setReturnFormat(JSON)

sparql.setQuery("""
    SELECT ?item ?itemLabel ?publication_date (group_concat(distinct ?platform;separator=", ") as ?platforms) (group_concat(distinct ?genre;separator=", ") as ?genres)  with {
    SELECT ?item WHERE 
        {
        ?item wdt:P31 wd:Q7889 .
        }limit 20} as %i
    WHERE
        { 
        include %i
        ?item wdt:P400 ?value . ?value rdfs:label ?platform . filter(lang(?platform)="en")
        ?item wdt:P136 ?value2 . ?value2 rdfs:label ?genre . filter(lang(?genre)="en")
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en,en". }
    } group by ?item ?itemLabel ?publication_date
""")

try:
    ret = sparql.queryAndConvert()
    for r in ret["results"]["bindings"]:
        print(r)
except Exception as e:
    print(e)