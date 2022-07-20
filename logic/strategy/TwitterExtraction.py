from logic.strategy.Extraction import Extraction
import twint
import pandas as pd
import os
import matplotlib.pyplot as plt

class TwitterExtraction(Extraction):
    ## Global
    __data = pd.DataFrame()
    __likes = []
    __date = []
    __retweets = []
    __replies = []
    __curr_dir = ""
    __c = twint.Config()
    
    """
    Concrete strategy that implements the algorithm to extract the data
    from Twitter using twitter Scrapper, following the base Strategy Extraction interface
    """
    def do_extraction(self):
        """
        method that first, collects the data, use
        pandas dataset to eliminate some useless columns
        """
        print("Twitter")
        self.data = self.__delete_useless_columns_twitter(self.__get_dataFrame_from_twitter())

        return "Datos extraidos"

    def save_data(self):
        """
        method that saves all the collected data
        into images or .xlx files
        """
        # setting current directory (changes on your pc)
        self.curr_dir = r'D:/Andres Wilches/Estudios/Ing Sistemas/Tendencias avanzadas de ingenieria de software/Extraccion_datos'
        os.chdir(self.curr_dir)
        # plotting date vs rt, rp, likes
        plt.figure(figsize=(10, 6), dpi=80)
        plt.plot(self.date,self.likes,color="blue",label="likes")
        plt.plot(self.date,self.retweets,color="red",label="retweets")
        plt.plot(self.date,self.replies,color="green",label="replies")
        plt.legend(loc='upper left')
        plt.title('Mercadolibre Twitter')
        # saving plot
        plt.savefig("static/data/twitter_meli.png")
        # saving dataset to .xlx format
        self.data.to_excel('static/data/mercadolibreTwitterInfo.xlsx')
        return "Datos guardados"

    # get dataFrame from facebook (Mercado Libre col)
    def __get_dataFrame_from_twitter(self):
        self.c.Username = "mercadolibre"
        self.c.Limit = 55
        self.c.Store_csv = True
        self.c.Output = "static/data/mercadolibreTweets.csv"
        twint.run.Search(self.c)
        return pd.read_csv('static/data/mercadolibreTweets.csv')

    # deleting the 'useless' data from the dataFrame
    def __delete_useless_columns_twitter(self,data_set):
        new_data_frame = {
            'post_id': data_set['id'],
            'text': data_set['tweet'],
            'date': data_set['date'],
            'time': data_set['time'],
            'replies': data_set['replies_count'],
            'retweets': data_set['retweets_count'],
            'likes': data_set['likes_count']
        }
        new_data_frame = pd.DataFrame(new_data_frame)
        os.remove('static/data/mercadolibreTweets.csv')
        self.likes = data_set['likes_count']
        self.date = data_set['date']
        self.replies = data_set['replies_count']
        self.retweets = data_set['retweets_count']
        return new_data_frame

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

    # getter of retweets
    @property
    def retweets(self):
        return self.__retweets

    # setter of retweets
    @retweets.setter
    def retweets(self,retweets):
        self.__retweets = retweets

    # getter of replies
    @property
    def replies(self):
        return self.__replies

    # setter of replies
    @replies.setter
    def replies(self,replies):
        self.__replies = replies

    # getter of c
    @property
    def c(self):
        return self.__c

    # setter of c
    @c.setter
    def c(self,c):
        self.__c = c
    
    # getter of current directory (change)
    @property
    def curr_dir(self):
        return self.__curr_dir

    # setter of current directory
    @curr_dir.setter
    def curr_dir(self,curr_dir):
        self.__curr_dir = curr_dir