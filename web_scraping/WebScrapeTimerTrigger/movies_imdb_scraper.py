import requests
import re
import urllib.request
import json
from bs4 import BeautifulSoup
import norm

movies = []


def run():
    global movies
    url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&count=250'
    response = requests.get(
        url, headers={"Accept-Language": "en-US", "encoding": "utf-8"})
    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = html_soup.find_all(
        'div', class_='lister-item mode-advanced')

    for i in range(len(movie_containers)):
        movie_title = movie_containers[i].h3.a.text
        idable_movie_title = norm.normImdbId(movie_title)
        movie_year = re.search(r"\d{4}", movie_containers[i].find(
            'span', class_='lister-item-year text-muted unbold').text).group()
        movie_id = omdbGetData(idable_movie_title)['imdbID']
        try:
            movie_certificate = movie_containers[i].find(
                'span', class_='certificate').text
        except AttributeError:
            movie_certificate = "N/A"
        movie_genre = movie_containers[i].find('span', class_='genre').text
        movie_genre = re.split(r"\s\s", movie_genre)[0][1:]
        movie_rating = movie_containers[i].find('strong').text
        movie_url = "www.imdb.com/title/"+movie_id
        movies.append((movie_year, movie_genre,
                       movie_certificate, movie_rating, movie_title, movie_url))
    return movies


def scrapeRatings(titles):
    movies = []
    for title in titles:
        print(title[0])
        movie = scrapeRating(title[0])
        if movie != None:
            movies.append(movie)
    return movies


def scrapeRating(title):
    if title == "101 Dalmations":
        idableTitle = "One Hundred and One Dalmations"
    else:
        idableTitle = norm.normImdbId(title)
    data = omdbGetData(idableTitle)
    print(data)
    try:
        Id = data['imdbID']
        year = data['Year']
        genres = data['Genre']
        mpaa = data['Rated']
        rating = data['imdbRating']
        imdbTitle = data['Title']
        url = "www.imdb.com/title/"+Id
    except KeyError:
        return None
    return (genres, mpaa, rating, imdbTitle, year, url)


def omdbGetData(title):
    print(title)
    url = "http://www.omdbapi.com/?t="
    title = title.split(" ")
    for i in range(len(title)-1):
        url += title[i] + "+"
    url += title[len(title)-1]
    url += "&apikey=232f04b4"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data
