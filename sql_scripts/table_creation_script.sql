create table movie(
	title varchar(100),
    year int,
    imdb_rating float,
    metacritic_rating float,
    rt_rating float,
    average_rating float,
    genre varchar(30),
    mpaa varchar(10), 
	Primary Key(title,year)
);
delete from movie where average_rating is null;
UPDATE movie SET imdb_url = imdbUrl WHERE imdbUrl IS NOT NULL;
    UPDATE movie SET meta_url = metaUrl WHERE metaUrl IS NOT NULL;
    UPDATE movie SET rt_url = rtUrl WHERE rtUrl IS NOT null;
select * from movie order by average_rating desc;
delete from movie where rt_rating=0;