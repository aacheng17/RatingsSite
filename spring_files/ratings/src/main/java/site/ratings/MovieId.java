package site.ratings;

import java.io.Serializable;

public class MovieId implements Serializable {
    private String title;
    private Integer year;
    
    public MovieId() {
        
    }
    public MovieId(String title,int year) {
        this.title=title;
        this.year=year;
    }
    @Override
    public int hashCode () {
        final int prime = 31;
        int result = 1;
        result = prime * result
                + ( ( title == null ) ? 0 : title.hashCode() );
        result = prime * result + year;
        return result;
    }
    @Override
    public boolean equals ( Object obj ) {
        if ( this == obj )
            return true;
        if ( obj == null )
            return false;
        if ( getClass() != obj.getClass() )
            return false;
        MovieId other = ( MovieId ) obj;
        if ( title == null ) {
            if ( other.title != null )
                return false;
        } else if ( ! title.equals(other.title) )
            return false;
        if ( year != other.year )
            return false;
        return true;
    }
}   
