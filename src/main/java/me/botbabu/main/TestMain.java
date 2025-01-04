package me.botbabu.main;

import me.botbabu.controller.MovieController;

public class TestMain {
	
	public static void main(String[] args) {
		
		MovieController movieController = new MovieController();
		
		movieController.fetchMovieRatings("Haider");
	}

}
