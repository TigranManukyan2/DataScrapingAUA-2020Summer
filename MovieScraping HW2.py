import requests;
import pandas as pd
import time;
from scrapy.http import TextResponse;

URL = "https://www.imdb.com/chart/moviemeter/"
base_url = "https://www.imdb.com"

class Movies: 
     def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")

     def scrape_movies(self):
        title = self.response.css("td.titleColumn a::text").extract()
        year = [str(i).strip('()') for i in self.response.css(".secondaryInfo:nth-child(2)::text").extract()]
        rank = []
        [rank.append(i) for i in range(1,101)]
        rating = []
        for i in self.response.css(".imdbRating"):
            rating.append(str(i.css("strong::text").extract()).strip('[]'))
        hyperlink = [base_url+i for i in self.response.css("td.titleColumn a::attr(href)").extract()]
        return title, year, rank, rating, hyperlink

film = Movies(URL).scrape_movies()


for i in range(0,100):
    if(film[3][i] == ""):
        film[3][i]="No ranking"



film = list(map(list, zip(*film)))


df = pd.DataFrame(film, columns=['Title','Year','Rank','Rating','Hyperlink'])
print(df)










