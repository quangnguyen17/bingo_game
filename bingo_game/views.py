from django.shortcuts import render, redirect, HttpResponse
import requests
from bs4 import BeautifulSoup
# Create your views here.


def index(request):
    url = 'https://en.wikipedia.org/wiki/javascript'
    keyword = None
    word_length = None

    if 'word_length' in request.GET:
        if request.GET['word_length'] != None:
            word_length = request.GET['word_length']

    if 'keyword' in request.GET:
        if request.GET['keyword'] != None:
            keyword = request.GET['keyword']
            url = f'https://en.wikipedia.org/wiki/{keyword}'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    context = {
        'url': url,
        'keyword': keyword,
        'word_length': word_length,
        'text': soup.get_text()
    }

    return render(request, 'index.html', context)
