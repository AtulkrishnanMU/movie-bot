package me.botbabu.service;

import java.util.List;

import me.botbabu.dao.MovieDAO;
import me.botbabu.dto.Movie;
import me.botbabu.dto.Rating;
import me.botbabu.util.MovieUtil;

public class MovieService {
	
	private MovieDAO movieDAO = new MovieDAO();
	private MovieUtil movieUtil = new MovieUtil();
	
	public Movie fetchMovieDetails(String movieName) {
		
		String movieLbLink = movieUtil.getMovieLbLink(movieName);
    
        Movie movie = movieDAO.fetchMovieDetails(movieLbLink);
        return movie;
	}
	
	public static void main(String[] args) {
		MovieService movieService = new MovieService();
		movieService.fetchMovieDetails("tianic");
	}

	public List<Rating> fetchMovieRatings(String movieName) {
		
		String movieLbLink = movieUtil.getMovieLbLink(movieName);
		
		String movieRatingsLink = movieLbLink.replace("/film/", "/travis_pickle12/friends/film/");
		
		return movieDAO.fetchMovieRatings(movieRatingsLink); 

	}

}
