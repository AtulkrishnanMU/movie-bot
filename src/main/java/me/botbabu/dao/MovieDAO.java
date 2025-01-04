package me.botbabu.dao;

import java.util.ArrayList;
import java.util.List;

import me.botbabu.dto.Movie;
import me.botbabu.dto.Rating;
import me.botbabu.util.MovieUtil;

public class MovieDAO {
	
	private MovieUtil movieUtil = new MovieUtil();

	public Movie fetchMovieDetails(String movieLbLink) {

		Movie movie = movieUtil.getLbDetails(movieLbLink);

		String bookingDetails = movieUtil.getReleaseDetails(movie);
		
		movie.setReleaseDetails(bookingDetails);

		return movie;
	}

	public List<Rating> fetchMovieRatings(String movieRatingsLink) {
        List<Rating> ratingsList = new ArrayList<>();

        movieUtil.fetchRatings(movieRatingsLink, ratingsList);

        // Attempt to fetch ratings from page 2
        try {
        	movieUtil.fetchRatings(movieRatingsLink + "page/2/", ratingsList);
        } catch (Exception e) {
        	e.printStackTrace();
            System.out.println("Error fetching additional pages: " + e.getMessage());
        }

        // Sort the ratings in descending order
        ratingsList.sort((a, b) -> Float.compare(b.getRating(), a.getRating()));

        // Print the sorted ratings
        System.out.println("Movie Ratings:");

		return ratingsList;
	}

//	public static void main(String[] args) {
//		MovieDAO movieDAO = new MovieDAO();
//		movieDAO.fetchDetails("https://letterboxd.com/film/titanic-1997/");
//	}

}
