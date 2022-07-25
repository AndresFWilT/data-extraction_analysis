# imports
from flask import Flask, render_template, request, session, redirect
from config import DevelopmentConfig
from jinja2 import Environment, FileSystemLoader
import os
import json

## Logic imports (Strategy pattern)
from logic.context.Data import Data
from logic.strategy.FacebookExtraction import FacebookExtraction
from logic.strategy.SparQLExtraction import SparQLExtraction
from logic.strategy.TwitterExtraction import TwitterExtraction

app = Flask(__name__)

## Default server endpoint
@app.route('/')
def init():
    return index()

## Another endpoint for index
@app.route('/index')
def index():
    return render_template('index.html')

## Endpoint for module data
@app.route('/data')
def data():
    return render_template('dataIndex.html')

## Endpoint for Facebook extraction
@app.route('/facebookData')
def get_data_FaceBook():
    data = Data(FacebookExtraction())
    data.execute_extraction()
    message = "Datos de Facebook extraidos y guardados con exito"
    return render_template('dataIndex.html', message=message)

## Endpoint for SparQl extraction
@app.route('/sparQLData')
def get_data_SparQL():
    data = Data(SparQLExtraction())
    data.execute_extraction()
    message = "Datos de SparQL extraidos y guardados con exito"
    return render_template('dataIndex.html', message = message)

## Endpoint for Twitter extraction
@app.route('/twitterData')
def get_data_Twitter():
    data = Data(TwitterExtraction())
    data.execute_extraction()
    message = "Datos de Twitter extraidos y guardados con exito"
    return render_template('dataIndex.html', message = message)

## Endpoint to view FacebookData 
@app.route('/viewFacebookData')
def view_fb_data():
    data = Data(FacebookExtraction())
    facebook_data = data.get_extraction()
    return render_template('viewFacebookData.html', facebook_data = facebook_data)

## Endpoint to view SparQLData 
@app.route('/viewSparQLData')
def view_sparql_data():
    data = Data(SparQLExtraction())
    sparql_data = data.get_extraction()
    return render_template('viewSparQLData.html', sparql_data = sparql_data)

## Endpoint to view TwitterData 
@app.route('/viewTwitterData')
def view_twitter_data():
    data = Data(TwitterExtraction())
    twitter_data = data.get_extraction()
    return render_template('viewTwitterData.html', twitter_data = twitter_data)

## Endpoint to go to dashBoard
@app.route('/dashboard')
def dashboard():
    data_t = Data(TwitterExtraction())
    twitter_data = data_t.get_extraction()
    data_f = Data(FacebookExtraction())
    facebook_data = data_f.get_extraction()
    # facebook data
    likes_fb = facebook_data['likes']
    date_fb = facebook_data['date']
    # twitter data
    date_tw = twitter_data['date']
    likes_tw = twitter_data['likes']
    retweets = twitter_data['retweets']
    replies = twitter_data['replies']
    # twitter analysis
    tw_numbers = __calculate_semicircle(likes_tw,retweets,replies)
    # social media comparison
    social_media = __calculate_pie(tw_numbers, likes_fb)
    # important data
    important_data = __get_important_data(facebook_data,twitter_data)
    important_data.append(round(tw_numbers[5],2))
    return render_template('dashboard.html', likes_fb = likes_fb, date_fb = date_fb, date_tw = date_tw, likes_tw = likes_tw, retweets = retweets, replies = replies, tw_numbers = tw_numbers, social_media = social_media, important_data = important_data)

## Method that gets the important data (max iterations, date, text.. etc)
def __get_important_data(fb, tw):
    data = []
    # for facebook
    fb_likes = fb['likes']
    max_likes_fb = max(fb_likes)
    index_fb = fb_likes.index(max_likes_fb)
    fb_id = fb['id']
    fb_text = fb['text']
    fb_date = fb['date']
    fb_id = fb_id[index_fb]
    fb_text = fb_text[index_fb]
    fb_date = fb_date[index_fb]
    # saving
    data.append(fb_id)
    data.append(max_likes_fb)
    data.append(fb_text)
    data.append(fb_date)
    # for twitter
    # Likes
    tw_likes = tw['likes']
    tw_likes_max = max(tw_likes)
    index_tw = tw_likes.index(tw_likes_max)
    tw_id = tw['id']
    tw_text = tw['tweet']
    tw_date = tw['date']
    tw_id = tw_id[index_fb]
    tw_text = tw_text[index_tw]
    tw_date = tw_date[index_tw]
    # saving
    data.append(tw_id)
    data.append(tw_likes_max)
    data.append(tw_text)
    data.append(tw_date)
    # retweets
    tw_retweets = tw['retweets']
    tw_retweets_max = max(tw_retweets)
    index_tw = tw_retweets.index(tw_retweets_max)
    tw_id = tw['id']
    tw_text = tw['tweet']
    tw_date = tw['date']
    tw_id = tw_id[index_fb]
    tw_text = tw_text[index_tw]
    tw_date = tw_date[index_tw]
    # saving
    data.append(tw_id)
    data.append(tw_retweets_max)
    data.append(tw_text)
    data.append(tw_date)
    # replies
    tw_replies = tw['replies']
    tw_replies_max = max(tw_replies)
    index_tw = tw_replies.index(tw_replies_max)
    tw_id = tw['id']
    tw_text = tw['tweet']
    tw_date = tw['date']
    tw_id = tw_id[index_fb]
    tw_text = tw_text[index_tw]
    tw_date = tw_date[index_tw]
    # saving
    data.append(tw_id)
    data.append(tw_replies_max)
    data.append(tw_text)
    data.append(tw_date)
    return data


## Method that calculate the numbers of pie
def __calculate_pie(twitter, facebook):
    # defining
    data = []
    # facebook data
    f_sum = 0
    for i in range(len(facebook)):
        f_sum = f_sum + facebook[i]
    # total sum of the pie
    total = twitter[0] + twitter[1] + twitter[2] + f_sum
    # percentages
    tw_per = ((twitter[0] + twitter[1] + twitter[2])/total)*100
    f_per = ((f_sum)/total)*100
    # saving data
    data.append(f_sum)
    data.append((twitter[0] + twitter[1] + twitter[2]))
    data.append(f_per)
    data.append(tw_per)
    return data

## Method that calculate the numbers of semicircle
def __calculate_semicircle(likes,retweets,replies):
    # defining
    data = []
    l_sum = 0
    rt_sum = 0
    rp_sum = 0
    # iteration
    for i in range(len(likes)):
        l_sum = l_sum + likes[i]
        rt_sum = rt_sum + retweets[i]
        rp_sum = rp_sum + replies[i]
    # percentages
    l_per = (l_sum/(l_sum+rt_sum+rp_sum))*100
    rt_per = (rt_sum/(l_sum+rt_sum+rp_sum))*100
    rp_per = (rp_sum/(l_sum+rt_sum+rp_sum))*100
    # saving sumatories
    data.append(l_sum)
    data.append(rt_sum)
    data.append(rp_sum)
    # saving percentages
    data.append(l_per)
    data.append(rt_per)
    data.append(rp_per)
    return data
    
## App init
if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.run(debug=True)