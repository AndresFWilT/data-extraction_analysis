# imports
from facebook_scraper import get_posts
import pandas as pd
import os
import matplotlib.pyplot as plt
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

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

# plot
plt.plot(_fecha, _likes)
plt.title('Likes en el tiempo - Mercadolibre Col')

# saving plot
plt.savefig("likes_tiempo_MeliFb.png")

# saving dataset into .xlx
fb_posts.to_excel('mercadolibreFbPostsInfo.xlsx',index=False)
print("End of Fb data extraction")
#-------------------------------- For SparQL ------------------------------------------------------------------
# global
_name = []
_info = []
_image = []

# methods
def execute_sparQl_Query():
    # we want to bring the most iconic videogame creators from SparQL
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    values = ['Microsoft','Xbox_Series_X_and_Series_S','Xbox_One','Sony_Interactive_Entertainment','PlayStation_5','PlayStation_4','Nintendo','Nintendo_Switch'] 
    # iterations to bring the info
    for value in values:
        sparql.setQuery(f'''
        SELECT ?name ?comment ?image
        WHERE {{ dbr:{value} rdfs:label ?name.
                dbr:{value} rdfs:comment ?comment.
                dbr:{value} dbo:thumbnail ?image.
            FILTER (lang(?name) = 'en')
            FILTER (lang(?comment) = 'en')
        }}''')
        sparql.setReturnFormat(JSON)
        qres = sparql.query().convert()
        result = qres['results']['bindings'][0]
        name, comment, image_url = result['name']['value'],result['comment']['value'],result['image']['value']
        _name.append(name)
        _info.append(comment)
        _image.append(image_url)
    # end of cycle
    data_frame = {
            'name': _name,
            'info': _info,
            'image': _image
        }
    return pd.DataFrame(data_frame)

sparQL_dataFrame = execute_sparQl_Query()

# saving dataset into .xlx
sparQL_dataFrame.to_excel('ConsolasTendenciaInfoSparQl.xlsx',index=False)
print("End of SparQl data extraction")