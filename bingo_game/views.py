from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import wikipedia
import random
import re


def index(request):
    context = {
        'rows': None
    }

    if 'keyword' in request.GET:
        if request.GET['keyword'] is not None:
            keyword = request.GET['keyword']
            keyword_obj = try_keyword(request, keyword)
            two_d_array = get_2d_array(keyword_obj)

            # total_stats = get_total_stats()
            # '''
            # total_stats = [
            #     total_played,
            #     total_wins,
            #     ['word','word','word','word','word']
            # ]
            # '''

            # TODO
            # UPDATE STATS FOR WHEN / GAME PLAYS

            context['rows'] = two_d_array

    return render(request, 'index.html', context)


# GIVEN A STRING, RETURNS KEYWORD OBJECT

def try_keyword(request, keyword):
    # If word exists
    try:
        keyword_to_play = Keyword.objects.get(word=keyword.upper())
    # If keyword is a new word
    except:
        list_of_words = get_words(request, keyword)
        keyword_to_play = Keyword.objects.create(word=keyword.upper())

        for word in list_of_words:
            subword = Subword.objects.create(word=word)
            subword.keywords.add(keyword_to_play)

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


def get_words(request, keyword):
    try:
        summary = wikipedia.summary(keyword)
        summary = summary.replace('.', ' ').replace(',', ' ').replace(
            '/', ' ').replace('\n', ' ').replace('(', ' ').replace(')', ' ')
        summary = summary.split(' ')

        REGEX = re.compile(r'^[A-Za-z]+$')

        list = []

        # WILL EVENTUALLY BE REPLACED WITH ANY API
        dummy_words = ['WITH', 'ALSO', 'THAT', 'THIS', 'THERE', 'MOST',
                       'ALONG', 'FROM', 'BASED', 'OTHER', 'SOME', 'HAVE', 'DOING']

        for index in range(len(summary)):
            word = summary[index].upper()
            if len(word) > 3 and REGEX.match(word) and word != keyword.upper() and word not in dummy_words:
                list.append(word)
    except:
        messages.error(
            request, f'No results for "{keyword}", try another keyword! :(')
        return None

    return list
# Returns [Total Games Played, Total Games Won, Top 5 words] in DB


def get_total_stats():
    total_played = 0
    total_wins = 0
    # top_five_words = [{"none":0},{"none":0},{"none":0},{"none":0},{"none":0}]
    one = {"word": "none", "count": 0}
    two = {"word": "none", "count": 0}
    three = {"word": "none", "count": 0}
    four = {"word": "none", "count": 0}
    five = {"word": "none", "count": 0}

    all_keywords_sorted_by_played = Keyword.objects.all().order_by('games_used')
    for keyword in all_keywords_sorted_by_played:
        # Increment total played and won
        total_played += keyword.games_used
        total_wins += keyword.games_won
        # Check Against Top 5, replace if larger
        if one['count'] < keyword.games_used:
            one = {"word": keyword.word, "count": keyword.games_used}
        elif two['count'] < keyword.games_used:
            two = {"word": keyword.word, "count": keyword.games_used}
        elif three['count'] < keyword.games_used:
            three = {"word": keyword.word, "count": keyword.games_used}
        elif four['count'] < keyword.games_used:
            four = {"word": keyword.word, "count": keyword.games_used}
        elif five['count'] < keyword.games_used:
            five = {"word": keyword.word, "count": keyword.games_used}

    return [total_played, total_wins, [one['word'], two['word'], three['word'], four['word'], five['word']]]
