from ctypes import sizeof
from logic.strategy.Extraction import Extraction
from facebook_scraper import get_posts
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

class FacebookExtraction(Extraction):
    ## Global
    __data = pd.DataFrame()
    __likes = []
    __date = []
    __curr_dir = ""
    
    """
    Concrete strategy that implements the algorithm to extract the data
    from facebook using Fb Scrapper, following the base Strategy Extraction interface
    """
    def do_extraction(self):
        """
        method that first, collects the data, use
        pandas dataset to eliminate some useless columns
        """
        print("Facebook")
        self.data = self.__delete_useless_columns_fb(self.__get_dataFrame_from_fb())
        return "Datos extraidos"

    def save_data(self):
        """
        method that saves all the collected data
        into images or .xlx files
        """
        # setting current direcotory (changes on your pc)
        self.curr_dir = r'D:/Andres Wilches/Estudios/Ing Sistemas/Tendencias avanzadas de ingenieria de software/Extraccion_datos'
        os.chdir(self.curr_dir)
        # plotting date vs likes
        plt.plot(self.date,self.likes)
        plt.title('Likes en el tiempo Meli - Facebook')
        # saving plot
        plt.savefig("static/data/likes_tiempo_MeliFb.png")
        # saving dataset to .xlx format
        self.data.to_excel('static/data/mercadolibreFbPostsInfo.xlsx')
        return "Datos guardados"

    # get dataFrame from facebook (Mercado Libre col)
    def __get_dataFrame_from_fb(self):
        posts = []
        for post in get_posts('mercadolibrecol', pages = 7):
            self.likes.append(post['likes'])
            self.date.append(post['time'])
            posts.append(post)
        return pd.DataFrame(posts)

    # deleting the 'useless' data from the dataFrame
    def __delete_useless_columns_fb(self,data_set):
        new_data_frame = {
            'post_id': data_set['post_id'],
            'text': data_set['text'],
            'timestamp': data_set['timestamp'],
            'time': data_set['time'],
            'image': data_set['image'],
            'likes': data_set['likes'],
            'was_live': data_set['was_live']
        }
        new_data_frame = pd.DataFrame(new_data_frame)
        return new_data_frame

    def get_data(self):
        """
        method that gets the collected data
        """
        data = pd.read_excel('static/data/mercadolibreFbPostsInfo.xlsx', sheet_name=None)
        first = {
            "time": data['Sheet1']['time'].tolist()
        }
        time = first['time']
        time2 = []
        for i in range(len(time)):
            time2.append(time[i].strftime("%m/%d/%Y, %H:%M:%S"))
        data = {
            "id": data['Sheet1']['post_id'].tolist(),
            "text": data['Sheet1']['text'].tolist(),
            "date": time2,
            "image": data['Sheet1']['image'].tolist(),
            "likes": data['Sheet1']['likes'].tolist(),
            "live": data['Sheet1']['was_live'].tolist()
        }
        return data

    # getter of data
    @property
    def data(self):
        return self.__data

    # setter of data
    @data.setter
    def data(self,data):
        self.__data = data

    # getter of date
    @property
    def date(self):
        return self.__date

    # setter of date
    @date.setter
    def date(self,date):
        self.__date = date

    # getter of likes
    @property
    def likes(self):
        return self.__likes

    # setter of likes
    @likes.setter
    def likes(self,likes):
        self.__likes = likes
    
    # getter of current directory (change)
    @property
    def curr_dir(self):
        return self.__curr_dir

    # setter of current directory
    @curr_dir.setter
    def curr_dir(self,curr_dir):
        self.__curr_dir = curr_dir