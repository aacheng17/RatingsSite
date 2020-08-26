import React from "react";
import "./App.css";
import MovieTable from "./components/MovieTable.js";

function App() {
  return (
    <div className="pagecolor">
      <div className="jumbotron text-center bg-info p-3 mb-3 text-white">
        <h1>Ratings Site</h1>
        <p>
          Ratings Aggregator getting the top user scores from IMDb,
          Metacritic,and Rotten Tomatoes
        </p>
      </div>
      <div className="mx-3">
        <MovieTable />
      </div>
    </div>
  );
}

export default App;
