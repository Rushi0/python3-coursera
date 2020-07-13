import requests
import json


def get_movies_from_tastedive(movie):
    url='https://tastedive.com/api/similar'
    resp=requests.get(url,params={'q':movie,'type':'movies','limit':5})
    return json.loads(resp.text)


def extract_movie_titles(response):
    similar_movies=[]
    for details in response['Similar']['Results']:
        similar_movies.append(details['Name'])
    return similar_movies

def get_related_titles(names_list):
    out=[]
    for name in names_list:
        out.extend(extract_movie_titles(get_movies_from_tastedive(name)))
    return list(set(out))

def get_movie_data(movie):
    url='http://www.omdbapi.com/'
    resp=requests.get(url,params={'t':movie,'r':'json'})
    return json.loads(resp.text)

def get_movie_rating(response):
    ratings=response['Ratings']
    for rating in ratings:
        #print(rating)
        if rating['Source']=='Rotten Tomatoes':
            return int(rating['Value'].replace('%','')) 
    return 0

def get_sorted_recommendations(movie_list):
    return sorted(get_related_titles(movie_list), key=lambda x:(get_movie_rating(get_movie_data(x)),x[0]), reverse=True)
    
