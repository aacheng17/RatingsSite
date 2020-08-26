import os
import mysql.connector
from mysql.connector import Error
import norm

from dotenv import load_dotenv
load_dotenv()

# AZURE
AZURE_DB_USER = os.getenv("AZURE_DB_USER")
AZURE_DB_PASS = os.getenv("AZURE_DB_PASS")
AZURE_DB_HOST = os.getenv("AZURE_DB_HOST")

# SQL
DB_NAME = "project_schema"
TABLE_NAME = "movie"
connection = None
cursor = None

# SQL FUNCTIONS


def sqlConnect():
    global connection, cursor
    connection = mysql.connector.connect(
        user=AZURE_DB_USER, password=AZURE_DB_PASS, host=AZURE_DB_HOST, port=3306, database=DB_NAME)
    cursor = connection.cursor(buffered=True)


def sqlDelete():
    global connection, cursor
    sqlConnect()
    print("Deleting movies from table {}".format(TABLE_NAME))
    query = "delete from {}".format(TABLE_NAME)
    cursor.execute(query)
    print("Successfully deleted all movies from table\n")
    sqlCommit()

# IMDB -> year, genre, mpaa, imdb_rating, title
# meta -> year, meta_rating, title,metaUrl
# rt -> year, rt_rating, title,rtUrl


def sqlInsert(movies, site):
    sqlConnect()
    print("Inserting movies into table {}".format(TABLE_NAME))
    insertions = 0
    for m in movies:
        if site == "imdb":
            query = 'insert into {} (year,genre,mpaa,imdb_rating,title,imdbUrl) values ({},"{}","{}",{},"{}","{}")'.format(
                TABLE_NAME, *m)
        elif site == "meta":
            norm_name = norm.normName(m[2])
            select_query = 'select * from {} where year={} and lower(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}"'.format(
                TABLE_NAME, m[0], norm_name)
            cursor.execute(select_query)
            movList = cursor.fetchall()
            if not movList:
                query = 'insert into {} (year,meta_rating,title,metaUrl) values ("{}","{}","{}","{}")'.format(
                    TABLE_NAME, *m)
            else:
                query = 'update {} set meta_rating = "{}", metaUrl="{}" where year = "{}" and LOWER(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}"'.format(
                    TABLE_NAME, m[1], m[3], m[0], norm_name)
        elif site == "rt":
            norm_name = norm.normName(m[2])
            select_query = 'select * from {} where year={} and lower(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}"'.format(
                TABLE_NAME, m[0], norm_name)
            cursor.execute(select_query)
            movList = cursor.fetchall()
            if not movList:
                query = 'insert into {} (year,rt_rating,title,rtUrl) values ("{}","{}","{}","{}")'.format(
                    TABLE_NAME, *m)
            else:
                query = 'update {} set rt_rating = "{}", rtUrl="{}" where year = "{}" and lower(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}"'.format(
                    TABLE_NAME, m[1], m[3], m[0], norm_name)
        print(query)
        try:
            cursor.execute(query)
        except Error as e:
            print("Failed to insert: {}".format(e))
        insertions += 1
    sqlCommit()
    print("Successfully inserted {} out of {} attempted movies\n".format(
        insertions, len(movies)))


def sqlGetMissing(site):
    sqlConnect()
    cursor.execute(
        "select title, year from {} where {}_rating is null".format(TABLE_NAME, site))
    titles = list(cursor)
    sqlCommit()
    return [(x[0], str(x[1])) for x in titles]


def sqlUpdate(movies, site):
    sqlConnect()
    print("Inserting movies into table {}".format(TABLE_NAME))
    insertions = 0
    for m in movies:
        print(m)
        if site == "imdb":
            norm_name = norm.normName(m[3])
            query = 'update {} set genre="{}",mpaa="{}",imdb_rating="{}",imdbUrl="{}" where lower(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}" and abs(year-{} < 2)'.format(
                TABLE_NAME, m[0], m[1], m[2], m[5], norm_name, m[4])
        elif site == "meta":
            norm_name = norm.normName(m[2])
            query = 'update {} set meta_rating="{}",metaUrl="{}" where year = "{}" and lower(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}"'.format(
                TABLE_NAME, m[0], m[3], m[1], norm_name)
        elif site == "rt":
            norm_name = norm.normName(m[2])
            query = 'update {} set rt_rating="{}",rtUrl="{}" where year = "{}" and lower(replace(replace(replace(title, "- ", ""), ",", ""), ":", "")) like "{}"'.format(
                TABLE_NAME, m[0], m[3], m[1], norm_name)
        try:
            print(query)
            cursor.execute(query)
        except Error as e:
            print("Failed to insert: {}".format(e))
        insertions += 1
    print("Successfully updated {} out of {} attempted movies\n".format(
        insertions, len(movies)))
    sqlCommit()


def sqlCommit():
    connection.commit()
    cursor.close()
    connection.close()


def sqlQueries(movies):
    try:
        sqlConnect()
        sqlDelete()
        sqlInsert(movies)
        sqlCommit()
    except mysql.connector.Error as error:
        raise Error("SQL Error")


def updateAverageRatings():
    average_rating_query = """update movie set average_rating=(ROUND(((imdb_rating+meta_rating+rt_rating)/3),2)) where not isnull(imdb_rating) and not isnull(meta_rating) and not isnull(rt_rating)"""
    try:
        sqlConnect()
        cursor.execute(average_rating_query)
        sqlCommit()
    except mysql.connector.Error as error:
        raise Error("SQL Error")


def deleteDuplicateMovies():
    delete_query = """delete from movie where (title,year) in (select * from (select a.title,a.year from movie as a, movie as b where a.title=b.title and a.year=b.year+1) as t);"""
    try:
        sqlConnect()
        cursor.execute(delete_query)
        print(delete_query)
        sqlCommit()
    except mysql.connector.Error as error:
        raise Error("SQL Error")


def copyUrls():
    query = """UPDATE movie SET imdb_url = imdbUrl WHERE imdbUrl IS NOT NULL;
    UPDATE movie SET meta_url = metaUrl WHERE metaUrl IS NOT NULL;
    UPDATE movie SET rt_url = rtUrl WHERE rtUrl IS NOT NULL;"""
    try:
        sqlConnect()
        cursor.execute(query, multi=True)
        print(query)
        sqlCommit()
    except mysql.connector.Error as error:
        raise Error("SQL Error")


def deleteBadEntries():
    delete_query = """delete from movie where average_rating is null;"""
    try:
        sqlConnect()
        cursor.execute(delete_query)
        print(delete_query)
        sqlCommit()
    except mysql.connector.Error as error:
        raise Error("SQL Error")
