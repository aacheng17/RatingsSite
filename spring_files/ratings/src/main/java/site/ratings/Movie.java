package site.ratings;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;

@Entity
@IdClass(MovieId.class)
public class Movie {
    @Id
    private String title;

    @Id
    private Integer year;

    @Column(name = "imdb_rating")
    private Float imdbRating;

    @Column(name= "imdbUrl")
    private String imdbUrl;

    @Column(name = "meta_rating")
    private Float metacriticRating;

    @Column(name="metaUrl")
    private String metaUrl;

    @Column(name = "rt_rating")
    private Float rtRating;

    @Column(name="rtUrl")
    private String rtUrl;

    @Column(name = "average_rating")
    private Float averageRating;

    private String genre;
  
    private String mpaa;
    
    public Movie() {
    }

    public Movie( String title, Integer year, Float imdbRating, String imdbUrl, Float metacriticRating, String metaUrl,
                  Float rtRating, String rtUrl, Float averageRating, String genre,String mpaa ) {
        this.title = title;
        this.year = year;
        this.imdbRating = imdbRating;
        this.imdbUrl = imdbUrl;
        this.metacriticRating = metacriticRating;
        this.metaUrl = metaUrl;
        this.rtRating = rtRating;
        this.rtUrl = rtUrl;
        this.averageRating = averageRating;
        this.genre = genre;
        this.mpaa = mpaa;
    }

    public String getTitle () {
        return title;
    }

    public void setTitle ( String title ) {
        this.title = title;
    }

    public Integer getYear () {
        return year;
    }

    public void setYear ( Integer year ) {
        this.year = year;
    }

    public Float getImdbRating () {
        return imdbRating;
    }

    public void setImdbRating ( Float imdbRating ) {
        this.imdbRating = imdbRating;
    }

    public String getImdbUrl () {
        return imdbUrl;
    }

    public void setImdbUrl ( String imdbUrl ) {
        this.imdbUrl = imdbUrl;
    }

    public Float getMetacriticRating () {
        return metacriticRating;
    }

    public void setMetacriticRating ( Float metacriticRating ) {
        this.metacriticRating = metacriticRating;
    }

    public String getMetaUrl () {
        return metaUrl;
    }

    public void setMetaUrl ( String metaUrl ) {
        this.metaUrl = metaUrl;
    }

    public Float getRtRating () {
        return rtRating;
    }

    public void setRtRating ( Float rtRating ) {
        this.rtRating = rtRating;
    }

    public String getRtUrl () {
        return rtUrl;
    }

    public void setRtUrl ( String rtUrl ) {
        this.rtUrl = rtUrl;
    }

    public Float getAverageRating () {
        return averageRating;
    }

    public void setAverageRating ( Float averageRating ) {
        this.averageRating = averageRating;
    }

    public String getGenre () {
        return genre;
    }

    public void setGenre ( String genre ) {
        this.genre = genre;
    }

    public String getMpaa () {
        return mpaa;
    }

    public void setMpaa ( String mpaa ) {
        this.mpaa = mpaa;
    }

    @Override
    public String toString () {
        return "Movie [title=" + title + ", year=" + year + ", imdbRating="
                + imdbRating + ", imdbUrl=" + imdbUrl + ", metacriticRating="
                + metacriticRating + ", metaUrl=" + metaUrl + ", rtRating="
                + rtRating + ", rtUrl=" + rtUrl + ", averageRating="
                + averageRating + ", genre=" + genre + ", mpaa=" + mpaa + "]";
    }

}
