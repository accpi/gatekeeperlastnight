from flask import Flask
from flask_restful import Api, Resource, reqparse

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)


class Quote(Resource):
    def get(self):
        url = "http://www.textsfromlastnight.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        random_url = url + soup.find_all('a')[len(soup.find_all('a')) - 6]['href']
        response = requests.get(random_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        texts_list = soup.find_all(id='texts-list')
        texts = None

        for _li in texts_list:
            texts = _li.find_all('p')

        quote_link = None
        quote_text = None

        for _text in texts[0]:
            quote_link = _text['href']
            quote_text = _text.text

        quote = {
            "quote_link": quote_link,
            "quote_text": quote_text
        }

        return quote, 200

api.add_resource(Quote, '/quote/')