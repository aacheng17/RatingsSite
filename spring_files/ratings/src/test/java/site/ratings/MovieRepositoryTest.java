package site.ratings;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import site.ratings.MovieRepository;
import site.ratings.Movie;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.test.context.junit4.SpringRunner;
import org.junit.runner.RunWith;

@RunWith(SpringRunner.class)
@DataJpaTest
@AutoConfigureTestDatabase(replace=Replace.NONE)
class MovieRepositoryTest {
    
    @Autowired
    private MovieRepository movieRepo;
    
    @Test
    void testGetInitialListDesc () {
       // fail("Not yet implemented");
        List<Movie> list=this.movieRepo.getInitialList();
        Movie m=list.get(0);
        System.out.println(m.toString());
    }

}
