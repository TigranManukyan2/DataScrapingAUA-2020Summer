import requests
import pandas as pd
import time
from scrapy.http import TextResponse


URL = "http://books.toscrape.com/"

l_URL = "http://books.toscrape.com/"

class Book:

    def __init__(self,URL):
        self.URL = URL
        self.page = requests.get(self.URL)
        self.response = TextResponse(body=self.page.text,url=self.URL,encoding="utf-8")

    def scraping_book(self):
        title = self.response.css('article[class="product_pod"] h3 a::attr(title)').extract()
        rating = self.response.css('p[class*="star-rating"]::attr(class)').extract()
        rating = [i.replace('star-rating','').strip() for i in rating]
        price = self.response.css(".price_color::text").extract()
        price = [i.replace('Â£','') for i in price]
        book_url = [URL+i for i in self.response.css('article[class="product_pod"] h3 a::attr(href)').extract()]
        img_url = [URL+i for i in self.response.css('img::attr(src)').extract()]
        in_stock = self.response.css('.instock::text').extract()
        in_stock = [i.replace('\n','').strip() for i in in_stock]
        return title, rating, price, book_url, img_url, in_stock[1::2]

    def get_next_page(self):
        next_url = self.response.css("li.next a::attr(href)").extract()
        return next_url



bk_class = Book(URL)
books = []


while True:
    time.sleep(3)
    if(bk_class.get_next_page() == []):
        books.append(bk_class.scraping_book())
        break
    else:
        books.append(bk_class.scraping_book())
        edge = bk_class.get_next_page ()[0].replace('catalogue/','')
        URL = l_URL + 'catalogue/' + edge
        bk_class = Book(URL)


print(books)