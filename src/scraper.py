from bs4 import BeautifulSoup as bs
from urllib import parse
import lxml
import pandas as pd
import calendar
from datetime import datetime as dt
import requests as r
from requests.models import PreparedRequest
import time
import re
import csv
import json
from classes import URL

class Crawler:
    def __init__(self):
        self.name = 'Bon Appetite Crawler'
        self.main_url = 'https://www.bonappetit.com/sitemap.xml?'
    
    def session(self,url):
        self.session = r.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15"}
        self.content = self.session.get(self.url,verify=False,headers=self.session.headers)
        self.status_code = self.content.status_code
        if self.status_code == 200:
            return self.session,self.content.content
        else:
            return None
    
    def parser(self):
        """
        Sitemap is organized by by year,month, and week. 
        The week is actually the week number of that month
        
        """
        timespan = pd.date_range(start='2/1/2021', end='3/1/2021', freq='M')
        urls = []
        for x in timespan:
            week = len(calendar.month(x.year,x.month).split('\n')) - 3
            for ii in range(1,week):
                params={'year':x.year,'month':x.month,'week':ii}
                req = PreparedRequest()
                req.prepare_url(self.main_url, params)
                urls.append(req.url)
        return urls

    def get_recipe_urls(self):
        self.object = []
        for x in self.parser():
           self.request = r.get(x)
           time.sleep(1)
           self.soup = bs(self.request.content, 'xml')
           self.posts = self.soup.findAll('url')
           for self.post in self.posts:
               self.link = self.post.find("loc").text
               if 'recipe/' in self.link:
                   self.object.append(self.link)
        return self.object  
    
    def write_urls(self):
        return 

def recipe_urls():
    data = [[x] for x in Crawler().get_recipe_urls()]
    file = open('recipe_urls.csv', 'w+', newline ='')
    with file:    
        write = csv.writer(file)
        write.writerows(data)


class Ingredients():
    def __init__(self):
        self.name = 'Bon Appetite Ingredients'
        self.data_location = 'recipe_urls.csv'
        self.data = self.text_parser(self.data_location)
    
    def text_parser(self,location):
        with open(location) as f:
            line = f.readlines() # list containing lines of file
        
        return [x.rstrip("\n") for x in line]
    
    def text(self):
        self.data
        return 
    

d = Ingredients().data[1:2]

class Data():
    def __init__(self,url):
        self.url = url
        self.url_data = r.get(self.url).content
        self.soup = bs(self.url_data,'html.parser')
        self.title = self.find(("h1",{"data-testid":"ContentHeaderHed"}))
        self.date = self.find(("time",{"data-testid":"ContentHeaderPublishDate"}))
        self.author = self.find(("span",{"data-testid":"BylineName"}))
        self.reviews = self.find(("li",{"p":"class"}))
        self.tags = self.find(("div",{"span":"class"}))
        self.ratings = self.find(("div",{"data-testid":"RatingWrapper"}))
        self.json = self.json_parser()

    def find(self,params):
        d = self.soup.findAll(params)
        data = [x.text for x in d]
        return data


    def json_parser(self):
        d = self.soup.find_all('script',type='text/javascript')[0].string
        a = str(d).split('=')[2].replace(';','')
        return json.loads(a)["keywords"]["tags"]
    


a = Data(d[0]).title

print (a)
        