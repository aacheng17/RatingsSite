package site.ratings;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface MovieRepository extends JpaRepository < Movie, MovieId > {
    @Query(value="select * from movie",nativeQuery=true)
    List<Movie> getInitialList();
}
