import React from "react";

//creates a row in the table for each movie
const Movie = ({ item, rank }) => (
  <tr>
    <td>{rank}</td>
    <td>{item.title}</td>
    <td>{item.year}</td>
    <td className="font-weight-bold">{item.averageRating}</td>
    <td>
      <a
        target="_blank"
        rel="noopener noreferrer"
        href={`https://${item.imdbUrl}`}
      >
        {item.imdbRating}
      </a>
    </td>
    <td>
      <a target="_blank" rel="noopener noreferrer" href={`${item.metaUrl}`}>
        {item.metacriticRating}
      </a>
    </td>
    <td>
      <a target="_blank" rel="noopener noreferrer" href={`${item.rtUrl}`}>
        {item.rtRating}
      </a>
    </td>
    <td>{item.genre}</td>
    <td>{item.mpaa}</td>
  </tr>
);
export default Movie;
