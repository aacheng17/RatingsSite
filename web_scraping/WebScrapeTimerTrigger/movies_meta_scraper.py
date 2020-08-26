import requests
from bs4 import BeautifulSoup
import norm


def isFloat(s):
    if s == None:
        return False
    for x in s:
        if x not in "0,1,2,3,4,5,6,7,8,9,.".split(","):
            return False
    return True


# SCRAPING
NUM_MOVIES = 250
URL = "https://www.metacritic.com/browse/movies/score/userscore/all/filtered?view=condensed&page="
USER_AGENT = {'User-agent': 'Mozilla/5.0'}
BASE_URL = "https://www.metacritic.com"
movies = []

# SQL
TABLE_NAME = "movies_meta"

# SCRAPING FUNCTIONS


def scrapeAll():
    i = 0
    while len(movies) < NUM_MOVIES:
        page = scrape(URL+str(i), USER_AGENT)
        parseHTML(page)
        i += 1


def scrape(url, userAgent):
    return requests.get(url, headers=userAgent)

# PARSING FUNCTIONS


def parseHTML(page):
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("div", class_="title_bump")
    # Each movie's information is in a <tr> element in the HTML
    trs = table.find_all("tr", class_="expand_collapse")
    for tr in trs:
        movie = parseMovie(tr)
        movies.append(movie)
        if len(movies) >= NUM_MOVIES:
            break


def parseMovie(tr):
    rating = tr.find("td", class_="score").find("div").get_text()

    td = tr.find("td", class_="details")
    title = td.find("h3").get_text()
    href = td.find("a", class_="title").get("href")
    movie_url = BASE_URL + href
    genres = scrapeGenres(movie_url)

    justGotDate = 0
    for child in td.children:
        child = str(child)
        if justGotDate == 1:
            justGotDate = 2
        elif justGotDate == 2:
            pipeIndex = child.find("|")
            if pipeIndex == -1:
                mpaa = "Rating Unlisted"
            else:
                mpaa = child[pipeIndex+2:-7]
            break
        if child[:6] == "<span>":
            year = child[-11:-7]
            justGotDate = 1

    if title == None:
        title = "N/A"
    if genres == None:
        genres = "N/A"
    if year == None:
        year = "N/A"
    if rating == None:
        rating = "N/A"
    if mpaa == None:
        mpaa = "N/A"

    # If title includes year at the end, use this as the year and remove from title
    if len(title) > 7:
        if title[-6] == "(" and title[-1] == ")" and title[-5:-1].isdigit():
            year = title[-5:-1]
            title = title[:-7]

    return (year, rating, title, movie_url)


def scrapeGenres(url):
    page = scrape(url, USER_AGENT)
    soup = BeautifulSoup(page.content, "html.parser")
    return ", ".join([x.get_text() for x in soup.find("div", class_="genres").contents[3].findAll("span")])


def scrapeRatings(titles):
    movies = []
    for title in titles:
        try:
            rating, url = scrapeRating(title[0], title[1])
            print(rating)
            if rating != None:
                movies.append((rating, title[1], title[0], url))
        except:
            print("temporary error")
    return movies


def scrapeRating(title, year):
    urlTitle = norm.normUrl(title)
    baseUrl = BASE_URL + "/movie/"
    if title.lower() == "star wars: episode iv - a new hope":
        thisUrl = "https://www.metacritic.com/movie/star-wars-episode-iv---a-new-hope"
    elif title.lower() == "star wars: episode v - the empire strikes back":
        thisUrl = "https://www.metacritic.com/movie/star-wars-episode-v---the-empire-strikes-back"
    elif title.lower() == "star wars: episode vi - return of the jedi":
        thisUrl = "https://www.metacritic.com/movie/star-wars-episode-vi---return-of-the-jedi"
    elif title.lower() == "moonlight" and year == 2016:
        thisUrl = "https://www.metacritic.com/movie/moonlight-2016"
    elif title.lower() == "hamilton" and year == 2020:
        thisUrl = "https://www.metacritic.com/movie/hamilton-2020"
    else:
        thisUrl = baseUrl + "-".join(urlTitle.split())
    print("metaUrl=", thisUrl)
    page = scrape(thisUrl, USER_AGENT)
    # if error message like 403 or 404, return nothing
    if str(page).split()[1][1] == "4":
        thisUrl += "-" + year
        page = scrape(thisUrl, USER_AGENT)
        if str(page).split()[1][1] == "4":
            return None
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        rating = soup.find("div", class_="us_wrapper").find(
            "a", class_="metascore_anchor").find("span").get_text()
    except AttributeError as e:
        print("Error scraping: {}".format(e))
        return None
    if not isFloat(rating):
        return None
    return (rating, thisUrl)


def run():
    scrapeAll()
    return movies
