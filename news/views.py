from django.shortcuts import render
import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import requests
import ssl
import socket
import re


#Getting news from New York Times
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Getting news from the-wall-street-journal
main_url = "https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal&apiKey=98cb343e477940f181f5b38bdb9e3f9d"
# fetching data in json format
open_nyt_page = requests.get(main_url).json()

    # getting all articles in a string article
article = open_nyt_page["articles"]

    # empty list which will
    # contain all trending news
nyt_news=[]

for ar in article:
    nyt_news.append(ar["title"])



# FROM BBC

main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=98cb343e477940f181f5b38bdb9e3f9d"
# fetching data in json format
open_bbc_page = requests.get(main_url).json()

    # getting all articles in a string article
article = open_bbc_page["articles"]

    # empty list which will
    # contain all trending news
bbc_news = []

for ar in article:
    bbc_news.append(ar["title"])













# GEtting news from Times of India

toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[0:-13] # removing footers

toi_news = []

for th in toi_headings:
    if len(th.text)<25:
        continue
    toi_news.append(th.text)



#Getting news from Hindustan times

ht_r = requests.get("https://www.hindustantimes.com/india-news/")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll("div", {"class": "headingfour"})
ht_headings = ht_headings[2:]
ht_news = []

for hth in ht_headings:
    if len(hth.text)<25:
        continue
    ht_news.append(hth.text)


#getting news From The Hindu

main_url = " https://newsapi.org/v1/articles?source=the-hindu&sortBy=top&apiKey=98cb343e477940f181f5b38bdb9e3f9d"
# fetching data in json format
open_th_page = requests.get(main_url).json()

    # getting all articles in a string article
article = open_th_page["articles"]

    # empty list which will
    # contain all trending news
th_news = []

for ar in article:
    th_news.append(ar["title"])


# FROM THE WASHINGTON POST
main_url = "https://newsapi.org/v2/top-headlines?sources=the-washington-times&apiKey=98cb343e477940f181f5b38bdb9e3f9d"
# fetching data in json format
open_twp_page = requests.get(main_url).json()

    # getting all articles in a string article
article = open_twp_page["articles"]

    # empty list which will
    # contain all trending news
twp_news = []

for ar in article:
    twp_news.append(ar["title"])





def index(req):
    return render(req, 'news/index.html', {'toi_news':toi_news,'ht_news': ht_news,'twp_news':twp_news,'nyt_news':nyt_news,'th_news':th_news,'bbc_news':bbc_news})
