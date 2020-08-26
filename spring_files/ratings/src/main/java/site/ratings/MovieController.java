package site.ratings;
import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/movies")
@CrossOrigin(origins="http://localhost:3000")
public class MovieController {
    private MovieRepository movieRepo;
    public MovieController(MovieRepository movieRepo) {
        this.movieRepo=movieRepo;
    }
    
    @GetMapping("/getDefault")
    public List<Movie> getInitialList(){
        return movieRepo.getInitialList();
    }
}
