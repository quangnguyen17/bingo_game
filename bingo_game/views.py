from django.shortcuts import render, redirect, HttpResponse
from .models import *
from bs4 import BeautifulSoup
import requests
import random
import re


def index(request):
    context = {
        'rows': None
    }

    if 'keyword' in request.GET:
        if request.GET['keyword'] is not None:
            keyword = request.GET['keyword']
            trimmed_keyword = " ".join(keyword.split())

            if len(trimmed_keyword) > 0:
                keyword_obj = try_keyword(keyword)
                two_d_array = get_2d_array(keyword_obj)

                total_stats = get_total_stats()
                '''
                total_stats = [
                    total_played,
                    total_wins,
                    ['word','word','word','word','word']
                ]
                '''
                
                # TODO
                # UPDATE STATS FOR WHEN / GAME PLAYS

                context['rows'] = two_d_array

    return render(request, 'index.html', context)


# GIVEN A STRING, RETURNS KEYWORD OBJECT


def try_keyword(keyword):
    if len(Keyword.objects.filter(word=keyword)) != 0:
        keyword_to_play = Keyword.objects.get(word=keyword.upper())
    else:
        # 50 WORDS
        list_of_words = get_words(keyword)
        keyword_to_play = Keyword.objects.create(word=keyword.upper())

        for word in list_of_words:
            subword_to_add = Subword.objects.create(word=word)
            subword_to_add.keywords.add(keyword_to_play)

    return keyword_to_play

# GIVEN KEYWORD OBJECT, RETURNS 2D-ARRAY WITH 24 RANDOM SUBWORDS


def get_2d_array(keyword_obj):
    subwords_array = keyword_obj.subwords.all()
    # keyword.subwords looks like QuerySet['a','b',...'h']
    # Pick 24 indexes to grab
    indexes_to_grab = []
    while len(indexes_to_grab) <= 24:
        index_to_try = random.randint(0, len(subwords_array) - 1)
        if index_to_try not in indexes_to_grab:
            indexes_to_grab.append(index_to_try)
    # indexes_to_grab looks like Array[1,2,3,....24]
    # Grabs the 24 indexes from subwords list
    grabbed_words_list = []
    for idx in indexes_to_grab:
        grabbed_words_list.append(subwords_array[idx])
    # grabbed_words_list looks like Array['a','b',...'h']
    # Add keyword_obj to the middle of subwords list
    grabbed_words_list.insert(12, keyword_obj)
    # grabbed_words_list looks like Array['a','b',..'keyword',...'h']
    # Converts to 2D Array
    two_d_array = [[], [], [], [], []]

    idx_counter = 0
    while idx_counter <= 24:
        # 0 to 4
        if idx_counter <= 4:
            two_d_array[0].append(grabbed_words_list[idx_counter])
        # 5 to 9
        elif idx_counter > 4 and idx_counter <= 9:
            two_d_array[1].append(grabbed_words_list[idx_counter])
        # 10 to 14
        elif idx_counter > 9 and idx_counter <= 14:
            two_d_array[2].append(grabbed_words_list[idx_counter])
        # 15 to 19
        elif idx_counter > 14 and idx_counter <= 19:
            two_d_array[3].append(grabbed_words_list[idx_counter])
        # 20 to 24
        elif idx_counter > 19 and idx_counter <= 24:
            two_d_array[4].append(grabbed_words_list[idx_counter])
        idx_counter += 1
    # two_d_array looks like Array[['a',...'b'],['a',...'b'],['a',...'b'],['a',...'b'],['a',...'b']]
    # add 2d array to session
    return two_d_array


def get_words(keyword):
    words = []
    url = f'https://en.wikipedia.org/wiki/{keyword}'

    REGEX = re.compile(r'^[A-Za-z]+$')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()
    words_list = " ".join(text.split()).split(' ')

    def word_valid(word):
        word_length = len(word)
        return word_length >= len(keyword) and word_length < (word_length * 2) and REGEX.match(word)

    filtered_list = filter(word_valid, words_list)

    filtered_words = []
    for word in filtered_list:
        filtered_words.append(word)

    final_list = list(dict.fromkeys(filtered_words))

    print(filtered_list)

    for i in range(50):
        random_word = final_list[random.randint(0, len(final_list) - 1)]
        words.append(random_word.upper())

    return words

# Returns [Total Games Played, Total Games Won, Top 5 words] in DB
def get_total_stats():
    total_played = 0
    total_wins = 0
    #top_five_words = [{"none":0},{"none":0},{"none":0},{"none":0},{"none":0}]
    one={"word":"none", "count":0} 
    two={"word":"none", "count":0}
    three={"word":"none", "count":0}
    four={"word":"none", "count":0}
    five={"word":"none", "count":0}
    
    all_keywords_sorted_by_played = Keyword.objects.all().order_by('games_used')
    for keyword in all_keywords_sorted_by_played:
        # Increment total played and won
        total_played += keyword.games_used
        total_wins += keyword.games_won
        # Check Against Top 5, replace if larger
        if one['count'] < keyword.games_used:
            one = {"word":keyword.word, "count":keyword.games_used}
        elif two['count'] < keyword.games_used:
            two = {"word":keyword.word, "count":keyword.games_used}
        elif three['count'] < keyword.games_used:
            three = {"word":keyword.word, "count":keyword.games_used}
        elif four['count'] < keyword.games_used:
            four = {"word":keyword.word, "count":keyword.games_used}
        elif five['count'] < keyword.games_used:
            five = {"word":keyword.word, "count":keyword.games_used}
    
    return [total_played,total_wins,[one['word'],two['word'],three['word'],four['word'],five['word']]]