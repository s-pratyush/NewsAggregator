from django.test import TestCase
from django.conf import settings
from .models import New
from .views import FetchNews, saveNews
from unittest.mock import patch, Mock

# Create your tests here.

class NewTestCase(TestCase):
    """
    New test case
    """
    def setUp(self):
        New.objects.create(title="Hello world", tag="nyt")

    def test_new_return_title(self):
        new = New.objects.get(title="Hello world")
        self.assertEquals(new.title, "Hello world")

    def test_new_return_tag(self):
        new = New.objects.get(title="Hello world")
        self.assertEquals(new.tag, "nyt")

    def test_id_return_hello_world(self):
        new = New.objects.get(id=1)
        self.assertEquals(new.title, "Hello world")

    def teardown(self):
        New.objects.all.delete()

class FetchNewsTestCase(TestCase):
    """
    Fetch News test case
    """
    def setUp(self):
        self.key = settings.NEWS_API_KEY

    @patch('requests.get')
    def test_fetch_news_return_a_200_response_for_nyt(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal&apiKey={}"
        response = FetchNews(url.format(self.key))
        self.assertEquals(response.status_code, 200)

    @patch('requests.get')
    def test_fetch_news_return_a_200_response_for_bbc(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={}"
        response = FetchNews(url.format(self.key))
        self.assertEquals(response.status_code, 200)
    
    @patch('requests.get')
    def test_fetch_news_return_a_200_response_for_toi(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "https://timesofindia.indiatimes.com/briefs"
        response = FetchNews(url)
        self.assertEquals(response.status_code, 200)

    @patch('requests.get')
    def test_fetch_news_return_a_200_response_for_ht(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "https://www.hindustantimes.com/india-news/"
        response = FetchNews(url)
        self.assertEquals(response.status_code, 200)

    @patch('requests.get')
    def test_fetch_news_return_a_200_response_for_th(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "https://newsapi.org/v1/articles?source=the-hindu&sortBy=top&apiKey={}"
        response = FetchNews(url.format(self.key))
        self.assertEquals(response.status_code, 200)

    @patch('requests.get')
    def test_fetch_news_return_a_200_response_for_twt(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "https://newsapi.org/v2/top-headlines?sources=the-washington-times&apiKey={}"
        response = FetchNews(url.format(self.key))
        self.assertEquals(response.status_code, 200)

class StoreNewsTestCase(TestCase):
    """
    Store news test case
    """
    def setUp(self):
        self.key = settings.NEWS_API_KEY 

    @patch('requests.get')
    def test_store_nyt_news(self, mock_get):
        mock_get.return_value = Mock(status_code = 200)
        mock_get.return_value.json.return_value = {"articles": [{"title": "hello world"}]}
        url = "https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal&apiKey={}"
        response = FetchNews(url.format(self.key))
        saveNews(response, tag="nyt")
        new = New.objects.get(id=1)
        self.assertEquals(new.tag, "nyt")
        self.assertEquals(new.title, 'hello world')

    @patch('requests.get')
    def test_store_bbc_news(self, mock_get):
        mock_get.return_value = Mock(status_code = 200)
        mock_get.return_value.json.return_value = {"articles": [{"title": "hello world"}]}
        url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={}"
        response = FetchNews(url.format(self.key))
        saveNews(response, tag="bbc")
        new = New.objects.get(id=1)
        self.assertEquals(new.tag, "bbc")
        self.assertEquals(new.title, 'hello world')

    @patch('requests.get')
    def test_store_th_news(self, mock_get):
        mock_get.return_value  = Mock(status_code = 200)
        mock_get.return_value.json.return_value = {"articles": [{"title": "hello world"}]}
        url = "https://newsapi.org/v1/articles?source=the-hindu&sortBy=top&apiKey={}"
        response = FetchNews(url.format(self.key))
        saveNews(response, tag="th")
        new = New.objects.get(id=1)
        self.assertEquals(new.tag, "th")
        self.assertNotEquals(new.title, '')

    def test_store_toi_news(self):
        url = "https://timesofindia.indiatimes.com/briefs"
        response = FetchNews(url)
        saveNews(response, tag="toi")
        new = New.objects.get(id=1)
        self.assertEquals(new.tag, "toi")
        self.assertNotEquals(new.title, '')

    def test_store_ht_news(self):
        url = "https://www.hindustantimes.com/india-news/"
        response = FetchNews(url)
        saveNews(response, tag="ht")
        new = New.objects.get(id=1)
        self.assertEquals(new.tag, "ht")
        self.assertNotEquals(new.title, '')

    def teardown(self):
        New.objects.all().delete()

