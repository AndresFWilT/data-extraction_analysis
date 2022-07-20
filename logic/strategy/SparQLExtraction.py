from logic.strategy.Extraction import Extraction
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import os

class SparQLExtraction(Extraction):
    ## Global
    __sparQL = SPARQLWrapper("https://dbpedia.org/sparql")
    __values = []
    __name = []
    __info = []
    __image = []
    __sparQL_data_frame = pd.DataFrame()
    __curr_dir = ""
    
    """
    Concrete strategy that implements the algorithm to extract the data
    from WikiData using SparQL, following the base Strategy Extraction interface
    """
    def do_extraction(self):
        """
        method that first, collects the data, use
        pandas dataset to save all later
        """
        print("SPARQL from DBpedia")
        self.values.extend(['Xbox_Series_X_and_Series_S','Xbox_One','Xbox_360','PlayStation_5','PlayStation_4','PlayStation_3','PlayStation_2','Nintendo_Switch'])
        self.sparQL_data_frame = self.__execute_sparQL_query()
        return "data extracted"
    
    def save_data(self):
        """
        method that saves all the collected data
        into .xlx files
        """
        # setting current direcotory (changes on your pc)
        self.curr_dir = r'D:/Andres Wilches/Estudios/Ing Sistemas/Tendencias avanzadas de ingenieria de software/Extraccion_datos'
        os.chdir(self.curr_dir)
        # saving dataset to .xlx file
        self.sparQL_data_frame.to_excel('Static/data/ConsolasTendenciaInfoSparQl.xlsx',index=False)
        return "saved data"

    # method that executes the query
    def __execute_sparQL_query(self):
        # iterations to bring the info
        for value in self.values:
            self.sparQL.setQuery(f'''
            SELECT ?name ?comment ?image
            WHERE {{ dbr:{value} rdfs:label ?name.
                    dbr:{value} rdfs:comment ?comment.
                    dbr:{value} dbo:thumbnail ?image.
                FILTER (lang(?name) = 'en')
                FILTER (lang(?comment) = 'en')
            }}''')
            self.sparQL.setReturnFormat(JSON)
            qres = self.sparQL.query().convert()
            result = qres['results']['bindings'][0]
            name, comment, image_url = result['name']['value'],result['comment']['value'],result['image']['value']
            self.name.append(name)
            self.info.append(comment)
            self.image.append(image_url)
        # end of cycle
        data_frame = {
                'name': self.name,
                'info': self.info,
                'image': self.image
            }
        return pd.DataFrame(data_frame)

    # getter of sparql
    @property
    def sparQL(self):
        return self.__sparQL

    # setter of sparQL
    @sparQL.setter
    def data(self,sparQL):
        self.__sparQL = sparQL

    # getter of values
    @property
    def values(self):
        return self.__values

    # setter of values
    @values.setter
    def date(self,values):
        self.__values = values

    # getter of name
    @property
    def name(self):
        return self.__name

    # setter of name
    @name.setter
    def name(self,name):
        self.__name = name

    # getter of info
    @property
    def info(self):
        return self.__info

    # setter of info
    @info.setter
    def info(self,info):
        self.__info = info

    # getter of image
    @property
    def image(self):
        return self.__image

    # setter of image
    @image.setter
    def image(self,image):
        self.__image = image

    # getter of sparQL_data_frame
    @property
    def sparQL_data_frame(self):
        return self.__sparQL_data_frame

    # setter of sparQL_data_frame
    @sparQL_data_frame.setter
    def sparQL_data_frame(self,sparQL_data_frame):
        self.__sparQL_data_frame = sparQL_data_frame

    # getter of current directory (change)
    @property
    def curr_dir(self):
        return self.__curr_dir

    # setter of current directory
    @curr_dir.setter
    def curr_dir(self,curr_dir):
        self.__curr_dir = curr_dir