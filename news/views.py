from django.shortcuts import render
from django.conf import settings
try:
    from beautifulsoup4 import BeautifulSoup
except:
    from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import requests
import ssl
import socket
import re
import random
from .models import New
import requests_cache
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

def fetchNews(url):
    logger.info('news - fetching news for {}'.format(url))
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # Cache request
    requests_cache.install_cache(cache_name='newsapi_cache', backend='sqlite', expire_after=3600)
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    user_agent = random.choice(user_agent_list)
    logger.info('Use fake user agent : {}'.format(user_agent))
    headers = {'User-Agent': user_agent}
    return requests.get(url, headers=headers)

def processNewsapiResponse(httpResponse):
    articles = []
    if (httpResponse.status_code == 200):
        page = httpResponse.json()
        articles = page['articles']
    return articles

def saveNews(httpResponse, tag):
    news = []
    if (tag == 'nyt' or tag == 'bbc' or tag == 'th' or tag == 'twp'):
        articles = processNewsapiResponse(httpResponse)
        logger.info('news - Saving articles to database for tag {}'.format(tag))
        for article in articles:
            news.append(New(title=article['title'], tag=tag))
    if (tag == 'toi'):
        toi_soup = BeautifulSoup(httpResponse.content, 'html5lib')
        toi_headings = toi_soup.find_all('h2')
        toi_headings = toi_headings[0:-13] # removing footers
        for th in toi_headings:
            if len(th.text)<25:
                continue
            news.append(New(title=th.text, tag=tag))
    if (tag == 'ht'):
        ht_soup = BeautifulSoup(httpResponse.content, 'html5lib')
        ht_headings = ht_soup.findAll("div", {"class": "headingfour"})
        ht_headings = ht_headings[2:]
        ht_news = []

        for hth in ht_headings:
            if len(hth.text)<25:
                continue
            news.append(New(title=hth.text, tag=tag))
    logger.debug("news - Saving news to databases")
    New.objects.bulk_create(news)

def index(req):
    logger.error("news - Deleting old entries")
    New.objects.all().delete()
    logger.error("new - API KEY: {}".format(settings.NEWS_API_KEY))
    news = [
        {
            'url': 'https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal&apiKey={}'.format(settings.NEWS_API_KEY),
            'tag': 'nyt'
        },
        {
            'url': 'https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={}'.format(settings.NEWS_API_KEY),
            'tag': 'bbc'
        },
        {
            'url': 'https://timesofindia.indiatimes.com/briefs',
            'tag': 'toi'
        },
        {
            'url': 'https://www.hindustantimes.com/india-news/',
            'tag': 'ht'
        },
        {
            'url': 'https://newsapi.org/v1/articles?source=the-hindu&sortBy=top&apiKey={}'.format(settings.NEWS_API_KEY),
            'tag': 'th'
        },
        {
            'url': 'https://newsapi.org/v2/top-headlines?sources=the-washington-times&apiKey={}'.format(settings.NEWS_API_KEY),
            'tag': 'twp'
        }
    ]
    for new in news:
        response = fetchNews(new['url'])
        logger.debug("news - Status code of {} is {}".format(new['url'], response.status_code))
        saveNews(response, new['tag'])
    db_new = New.objects.all()
    toi_news = db_new.filter(tag='toi')
    ht_news = db_new.filter(tag='ht')
    twp_news = db_new.filter(tag='twp')
    nyt_news = db_new.filter(tag='nyt')
    th_news = db_new.filter(tag='th')
    bbc_news = db_new.filter(tag='bbc')
    return render(req, 'news/index.html', {'toi_news':toi_news,'ht_news': ht_news,'twp_news':twp_news,'nyt_news':nyt_news,'th_news':th_news,'bbc_news':bbc_news})
