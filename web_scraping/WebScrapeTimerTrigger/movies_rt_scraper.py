import requests
from bs4 import BeautifulSoup
import norm
from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome("ChromeDriver/chromedriver.exe", options=options)
movies = list()


def run():
    genrePagesList = []
    drama_page = requests.get(
        "https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/")
    genrePagesList.append((drama_page, 100))
    comedy_page = requests.get(
        "https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/")
    genrePagesList.append((comedy_page, 100))
    animation_page = requests.get(
        "https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/")
    genrePagesList.append((animation_page, 50))
    horror_page = requests.get(
        "https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/")
    genrePagesList.append((horror_page, 50))

    for page in genrePagesList:
        webscraper(page)

    movies.sort(reverse=True, key=getRating)
    return movies


def getRating(element):
    return element[1]


def scrapeRatings(titles):
    movies = []
    for title in titles:
        movie = scrapeRatingSearch(title[0], title[1])
        if movie != None:
            movies.append(movie)
    return movies


def scrapeRatingSearch(title, year):
    print(title)
    if title.lower() == "m":
        try:
            rt_url = "https://www.rottentomatoes.com/m/1012928-m"
            rating = scrapeRatingLink(rt_url)
        except:
            rating = 0
    elif title.lower() == "se7en":
        try:
            rt_url = "https://www.rottentomatoes.com/m/seven"
            rating = scrapeRatingLink(rt_url)
        except:
            rating = 0
    elif title.lower() == "in the mood for love":
        try:
            rt_url = "https://www.rottentomatoes.com/m/in_the_mood_for_love_2001"
            rating = scrapeRatingLink(rt_url)
        except:
            rating = 0
    elif title.lower() == "star wars: episode iv - a new hope":
        try:
            rt_url = "https://www.rottentomatoes.com/m/star_wars"
            rating = scrapeRatingLink(rt_url)
        except:
            rating = 0
    elif title.lower() == "star wars: episode v - the empire strikes back":
        try:
            rt_url = "https://www.rottentomatoes.com/m/empire_strikes_back"
            rating = scrapeRatingLink(rt_url)
        except:
            rating = 0
    elif title.lower() == "star wars: episode vi - return of the jedi":
        try:
            rt_url = "https://www.rottentomatoes.com/m/star_wars_episode_vi_return_of_the_jedi"
            rating = scrapeRatingLink(rt_url)
        except:
            rating = 0
    else:
        thisUrl = "https://www.rottentomatoes.com/search?search=" + \
            "%20".join(title.split())
        page = requests.get(thisUrl)
        soup = BeautifulSoup(page.content, "html.parser")
        json = soup.find("script", id="movies-json")
        movies = str(json).split('"name":')
        closestDate = 1000
        movie = ""
        for m in movies:
            thisTitle = m[1:m.find('","url":')]
            thisTitleNorm = norm.normUrlRt(thisTitle)
            titleNorm = norm.normUrlRt(title)
            if thisTitleNorm in titleNorm or titleNorm in thisTitleNorm:
                index = m.find('"releaseYear":')
                thisYear = m[index+15:index+19]
                if not thisYear.isdigit():
                    continue
                yearDiff = abs(int(thisYear)-int(year))
                if yearDiff < closestDate:
                    movie = m
                    closestDate = yearDiff
        if movie != "":
            url_index = movie.find('"url":')+7
            url_post_index = movie.find(',"tomatometerScore"')-1
            rt_url = movie[url_index:url_post_index]
            print(rt_url)
            try:
                rating = scrapeRatingLink(rt_url)
            except:
                rating = 0
        else:
            rt_url = norm.normUrlRt(title)
            try:
                rating = scrapeRating(rt_url)
            except:
                rating = None
            if rating == None:
                if rt_url[:4] == "the ":
                    try:
                        rating = scrapeRating(rt_url[4:])
                    except:
                        rating = 0
        print("rtUrl=", rt_url)
    return (rating, year, title, rt_url)


def scrapeRating(title):
    return scrapeRatingLink("https://www.rottentomatoes.com/m/"+"_".join(title.split()))


def scrapeRatingLink(url):
    # print(url)
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # firstFind = soup.find("div",class_="mop-ratings-wrap__half audience-score")
    # if firstFind == None:
    #     return None
    # secondFind = firstFind.find("span",class_="mop-ratings-wrap__percentage")
    # if secondFind == None:
    #     return None
    # text = secondFind.get_text()
    # rating = text.strip()[:2]
    # return str(int(rating)/10)
    # try:
    driver.get(url)
    button = driver.find_element_by_class_name(
        "mop-ratings-wrap__score-detail-text")
    button.click()
    new_page = driver.page_source

    movie_page = BeautifulSoup(new_page, "html.parser")
    r_section = movie_page.find(
        "section", class_="modal modal--animate-slide is-open")
    aud_score = r_section.find(
        "span", class_="js-audience-score-info").get_text()
    rating = ((float)(aud_score))*2.0
    rating = round(rating, 1)
    return rating
    # except:
    # print("temporary error")


def webscraper(movieTuple):

    page = movieTuple[0]
    movieLimit = movieTuple[1]
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="table")

    titles = table.find_all("tr", limit=movieLimit+1)
    for t in titles[1:]:
        try:
            a = t.find(
                "a", class_="unstyled articleLink")
            title = a.get_text().strip()[:-7]
            try:
                ind = title.index("(")
                title = title[:ind].strip()
            except:
                pass
            # title = title.replace(':', '')
            # title = title.replace(',', '')
            # title = title.replace("- ", '')
            year = (int)(a.get_text()[-5:-1])
            link = a['href']
            page_link = "https://www.rottentomatoes.com"+link
            rating = scrapeRatingLink(page_link)
            print(title)
            tup = (year, rating, title, page_link)
            if tup not in movies:
                movies.append(tup)
        except:
            print("temporary error")
