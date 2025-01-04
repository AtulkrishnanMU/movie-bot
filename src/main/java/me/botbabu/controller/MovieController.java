package me.botbabu.controller;

import java.util.List;

import me.botbabu.dto.Movie;
import me.botbabu.dto.Rating;
import me.botbabu.service.MovieService;

public class MovieController {
	
	private MovieService movieService = new MovieService();
	
	public Movie fetchMovieDetails(String movieName) {
		return movieService.fetchMovieDetails(movieName);
	}

	public List<Rating> fetchMovieRatings(String movieName) {
		return movieService.fetchMovieRatings(movieName);
	}
}
