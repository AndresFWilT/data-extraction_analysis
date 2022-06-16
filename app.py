# imports
from facebook_scraper import get_posts
import pandas as pd
import os
import matplotlib.pyplot as plt
from SPARQLWrapper import SPARQLWrapper, JSON

os.chdir(r'D:/Andres Wilches/Estudios/Ing Sistemas/Tendencias avanzadas de ingenieria de software/Corte 1/Extraccion_datos')

### For facebook

# global var
_likes = []
_fecha = []

### methods

# get dataFrame from facebook (Mercado Libre col)
def get_dataFrame_from_fb():
    posts = []
    # we bring the info from the posts
    for post in get_posts('mercadolibrecol',pages =7):
        _likes.append(post['likes'])
        _fecha.append(post['time'])
        posts.append(post)
    return pd.DataFrame(posts)

# deleting the 'useless' data from the dataFrame
def delete_useless_columns_fb(data_set):
    new_data_frame = {
        'post_id': data_set['post_id'].head(),
        'text': data_set['text'].head(),
        'timestamp': data_set['timestamp'].head(),
        'time': data_set['time'].head(),
        'image': data_set['image'].head(),
        'likes': data_set['likes'].head(),
        'was_live': data_set['was_live'].head()
    }
    new_data_frame = pd.DataFrame(new_data_frame)
    return new_data_frame

# limitating the info deleting som useless columns from the dataframe creation
fb_posts = delete_useless_columns_fb(get_dataFrame_from_fb())
print(fb_posts.dtypes)

# plot
plt.plot(_fecha, _likes)
plt.title('Likes en el tiempo - Mercadolibre Col')

# saving plot
plt.savefig("likes_tiempo_MeliFb.png")

# saving dataset into .xlx
fb_posts.to_excel('mercadolibrePostsInfo.xlsx',index=False)

# Por SparQL ------------------------------------------------------------------
"""
sparql = SPARQLWrapper(
    "http://vocabs.ardc.edu.au/repository/api/sparql/"
    "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020"
)
sparql.setReturnFormat(JSON)

sparql.setQuery(
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
)

try:
    ret = sparql.queryAndConvert()
    for r in ret["results"]["bindings"]:
        print(r)
except Exception as e:
    print(e)

"""

