import azure.functions as func
import logging
import datetime
import movies_sql as ms
import movies_imdb_scraper
import movies_meta_scraper
import movies_rt_scraper

# MAIN


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    # Deletes all entries from table
    ms.sqlDelete()
    # runs the scrapers for each site and inserts them into the table
    ms.sqlInsert(movies_imdb_scraper.run(), "imdb")
    ms.sqlInsert(movies_meta_scraper.run(), "meta")
    ms.sqlInsert(movies_rt_scraper.run(), "rt")

    # gets the movies without a rating for each site,runs the scraper to get those ratings and updates  the table
    ratings = movies_imdb_scraper.scrapeRatings(ms.sqlGetMissing("imdb"))
    ms.sqlUpdate(ratings, "imdb")
    ratings = movies_meta_scraper.scrapeRatings(ms.sqlGetMissing("meta"))
    ms.sqlUpdate(ratings, "meta")
    ratings = movies_rt_scraper.scrapeRatings((ms.sqlGetMissing("rt")))
    ms.sqlUpdate(ratings, "rt")

    # finalizes the table's data
    ms.updateAverageRatings()
    ms.deleteDuplicateMovies()
    ms.copyUrls()
    ms.deleteBadEntries()
