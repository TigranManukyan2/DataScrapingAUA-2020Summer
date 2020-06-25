import requests;
import pandas as pd
import time;
from scrapy.http import TextResponse;

URL = "http://quotes.toscrape.com/"
base_url = "http://quotes.toscrape.com"


class Quotes:

    def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")

    def get_quotes(self):
        quotes = self.response.css("span.text::text").extract()
        authors = self.response.css("small.author::text").extract() 
        tags = [i.css("a.tag::text").extract() for i in self.response.css("div.tags")]
        hyperlinks = [base_url+i for i in self.response.css("small.author ~ a::attr(href)").extract()]
        return quotes, authors, tags, hyperlinks

    def get_next_page(self):
        next_url = self.response.css("li.next a::attr(href)").extract()
        return next_url




quotes = []
thequotes = Quotes(URL)


while True:
    time.sleep(3)
    if(thequotes.get_next()==[]):
        quotes.append(thequotes.get_quotes())
        break
    else:
        quotes.append(thequotes.get_quotes())
        URL = base_url + thequotes.get_next()[0]
        thequotes = Quotes(URL)


Print(quotes)