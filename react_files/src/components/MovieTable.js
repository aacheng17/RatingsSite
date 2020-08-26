import React from "react";
import { Component } from "react";
import Movie from "./Movie.js";
import "../App.css";
import RangeSlider from "./RangeSlider.js";
import TextField from "@material-ui/core/TextField";
import IconButton from "@material-ui/core/IconButton";
import InputAdornment from "@material-ui/core/InputAdornment";
import ClearIcon from "@material-ui/icons/Clear";

export default class MovieTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      movieList: [],
      initList: [],
      page: 1,
      searchString: "",
      sortBy: "averageRating",
      sortAscending: false,
      yearFullRange: [0, 10000],
      yearRange: [0, 10000],
      averageRatingFullRange: [0, 10],
      averageRatingRange: [0, 10],
    };
  }

  // START FETCHING FUNCTIONS
  getYearFullRange(movieList) {
    if (movieList.length === 0) {
      return [0, 10000];
    }
    var minYear = movieList[0].year,
      maxYear = movieList[0].year;
    movieList.forEach((movie) => {
      if (movie.year < minYear) {
        minYear = movie.year;
      }
      if (movie.year > maxYear) {
        maxYear = movie.year;
      }
    });
    return [minYear, maxYear];
  }
  //fetches the data from the server
  componentDidMount() {
    //Get the link and check to see what sorting the user wants
    fetch("https://ratingsspring.azurewebsites.net/movies/getDefault")
      .then((response) => response.json())
      .then((data) => {
        var tempYearFullRange = this.getYearFullRange(data);
        this.setState({
          movieList: data,
          initList: data,
          yearFullRange: tempYearFullRange,
          yearRange: tempYearFullRange,
        });
      });
  }
  // END FETCHING FUNCTIONS

  // START RENDER FUNCTIONS
  getPageActiveState(num) {
    if (this.state.page === num) {
      return "page-item active";
    } else {
      return "page-item";
    }
  }
  setSortBy(header) {
    var newSortAscending = false;
    if (this.state.sortBy === header) {
      newSortAscending = !this.state.sortAscending;
    }
    this.setState({
      sortBy: header,
      sortAscending: newSortAscending,
    });
  }
  sliderRangeHandler(event, newValue, rangeParam) {
    this.setState({
      page: 1,
      [rangeParam + "Range"]: newValue,
    });
  }
  filterRange(movie, rangeParam) {
    return (
      movie[rangeParam] >= this.state[rangeParam + "Range"][0] &&
      movie[rangeParam] <= this.state[rangeParam + "Range"][1]
    );
  }
  render() {
    // Filter and sort
    var movieListShow = this.state.movieList;
    movieListShow = movieListShow.filter(
      (movie) =>
        this.filterRange(movie, "year") &&
        this.filterRange(movie, "averageRating")
    );
    movieListShow.sort((a, b) => {
      if (a[this.state.sortBy] < b[this.state.sortBy]) {
        return -1;
      }
      if (a[this.state.sortBy] > b[this.state.sortBy]) {
        return 1;
      }
      return 0;
    });
    // Reverse if sort by descending, and also reverse if sorting by name (since it's a string)
    if (!this.state.sortAscending !== (this.state.sortBy === "title")) {
      movieListShow.reverse();
    }

    // Search
    movieListShow = movieListShow.filter(
      (movie) =>
        movie.title.toLowerCase().includes(this.state.searchString) ||
        movie.genre.toLowerCase().includes(this.state.searchString)
    );

    const pageList = movieListShow.slice(
      100 * (this.state.page - 1),
      100 * this.state.page
    );

    //Start building elements

    // Search field
    const searchField = (
      <TextField
        id="outlined-full-width"
        label="Search movies"
        variant="outlined"
        value={this.state.searchString}
        fullWidth
        onChange={(event) =>
          this.setState({ searchString: event.target.value.toLowerCase() })
        }
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                class="btn btn-sm btn-danger"
                onClick={() => this.setState({ searchString: "" })}
              >
                <ClearIcon fontSize="small" />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    );
    //sort Icon
    const sortIcon = (
      <svg
        width="1.2em"
        height="1.2em"
        viewBox="0 0 16 16"
        class="bi bi-chevron-expand"
        fill="currentColor"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          d="M3.646 9.146a.5.5 0 0 1 .708 0L8 12.793l3.646-3.647a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 0-.708zm0-2.292a.5.5 0 0 0 .708 0L8 3.207l3.646 3.647a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 0 0 0 .708z"
        />
      </svg>
    );

    // Sliders
    var sliders = <div></div>;
    // Make sure that the info has loaded before building sliders
    if (this.state.yearFullRange[0] !== 0) {
      sliders = (
        <div>
          <span className="my-2"> Filter by Year </span>
          {/* <button
            className="btn btn-outline-dark"
            onClick={() => {
              var tempYearRange = this.getYearFullRange(this.state.initList);
              this.setState({
                page: 1,
                yearRange: tempYearRange,
                yearFullRange: tempYearRange,
                averageRatingFullRange: [0, 10],
                averageRatingRange: [0, 10],
              });
              //document.getElementById("yearSlider").value = tempYearRange;
            }}
          >
            Clear
          </button> */}
          <RangeSlider
            id="yearSlider"
            key={0}
            type="year"
            minValue={this.state.yearFullRange[0]}
            maxValue={this.state.yearFullRange[1]}
            handler={(event, newValue) =>
              this.sliderRangeHandler(event, newValue, "year")
            }
          />
          <span className="my-2"> Filter by Average Rating </span>
          <RangeSlider
            key={1}
            type="ratings"
            minValue={this.state.averageRatingFullRange[0]}
            maxValue={this.state.averageRatingFullRange[1]}
            handler={(event, newValue) =>
              this.sliderRangeHandler(event, newValue, "averageRating")
            }
          />
        </div>
      );
    }

    // Page buttons
    var pages = [];
    for (let i = 1; i <= movieListShow.length / 100 + 1; i++) {
      pages.push(
        <li className={this.getPageActiveState(i)} key={i}>
          <button
            className="page-link border border-dark"
            onClick={() => this.setState({ page: i })}
          >
            {i}
          </button>
        </li>
      );
    }

    // Table
    var table;
    if (pageList.length > 0) {
      table = (
        <div>
          <table className="table table-striped table-bordered">
            <thead className="thead-dark">
              <tr>
                <th>Rank</th>
                <th
                  className="Clickable rowWidth2"
                  onClick={() => this.setSortBy("title")}
                >
                  <span className="mr-1">Name</span>
                  {sortIcon}
                </th>
                <th
                  className="Clickable"
                  onClick={() => this.setSortBy("year")}
                >
                  <span className="mr-1">Year</span>
                  {sortIcon}
                </th>
                <th
                  className="Clickable genre"
                  onClick={() => this.setSortBy("averageRating")}
                >
                  <span className="mr-1">Average Rating</span>
                  {sortIcon}
                </th>
                <th
                  className="Clickable"
                  onClick={() => this.setSortBy("imdbRating")}
                >
                  <span className="mr-1">IMDb Rating</span>
                  {sortIcon}
                </th>
                <th
                  className="Clickable"
                  onClick={() => this.setSortBy("metacriticRating")}
                >
                  <span className="mr-1">Metacritic Rating</span>
                  {sortIcon}
                </th>
                <th
                  className="Clickable"
                  onClick={() => this.setSortBy("rtRating")}
                >
                  <span className="mr-1">Rotten Tomatoes Rating</span>
                  {sortIcon}
                </th>
                <th className="rowWidth">Genre</th>
                <th>MPAA Certification</th>
              </tr>
            </thead>
            <tbody>
              {pageList.map((item, count) => (
                //maps each item in the list to a Movie object
                <Movie
                  key={100 * (this.state.page - 1) + count + 1}
                  item={item}
                  rank={100 * (this.state.page - 1) + count + 1}
                />
              ))}
            </tbody>
          </table>
        </div>
      );
    } else {
      table = <h4>No results match your search parameters</h4>;
    }

    return (
      <div>
        <div className="mx-3">{searchField}</div>
        <div className="mx-4 my-2">{sliders}</div>
        <div className="mx-3">{table}</div>
        <nav>
          <ul className="mt-3 pagination justify-content-center">{pages}</ul>
        </nav>
      </div>
    );
  }
  // END RENDER FUNCTIONS
}
