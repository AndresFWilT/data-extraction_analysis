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

## Endpoint for Facebook extraction
@app.route('/facebookData')
def get_data_FaceBook():
    data = Data(FacebookExtraction())
    data.execute_extraction()
    return render_template('index.html')

## Endpoint for SparQl extraction
@app.route('/sparQLData')
def get_data_SparQL():
    data = Data(SparQLExtraction())
    data.execute_extraction()
    return render_template('index.html')

## Endpoint for Twitter extraction
@app.route('/twitterData')
def get_data_Twitter():
    data = Data(TwitterExtraction())
    data.execute_extraction()
    return render_template('index.html')

## App init
if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.run(debug=True)