package me.botbabu.dto;

import java.util.Date;
import java.util.List;
import java.util.Set;

public class Movie {

	private String title;
	private String director;
	private Date releaseDate;
	private int releaseYear;
	private String[] genres;
	private float rating;
	private String[] cast;
	private String writer;
	private int duration;
	private Set<String> language;
	private String synopsis;
	private String posterURL;
	private String lbLink;
	private List<String> country;
	private String releaseDetails;
	private List<Rating> ratings;

	@Override
	public String toString() {
		return "Movie [title=" + title + "\n Release Details Details=" + releaseDetails + "\n LB link=" + lbLink
				+ "\n director=" + director + "\n genre(s)=" + genres[0] + "\n language=" + language + "\n country="
				+ country + "\n rating=" + rating + "\n duration=" + duration + "\n synopsis=" + synopsis
				+ "\n posterURL=" + posterURL + "]";
	}

	public List<Rating> getRatings() {
		return ratings;
	}

	public void setRatings(List<Rating> ratings) {
		this.ratings = ratings;
	}

	public String getReleaseDetails() {
		return releaseDetails;
	}

	public String getReleaseDetail() {
		return releaseDetails;
	}

	public void setReleaseDetails(String releaseDetails) {
		this.releaseDetails = releaseDetails;
	}

	public Date getReleaseDate() {
		return releaseDate;
	}

	public void setReleaseDate(Date releaseDate) {
		this.releaseDate = releaseDate;
	}

	public List<String> getCountry() {
		return country;
	}

	public void setCountry(List<String> country) {
		this.country = country;
	}

	public String getLbLink() {
		return lbLink;
	}

	public void setLbLink(String movieLink) {
		this.lbLink = movieLink;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getDirector() {
		return director;
	}

	public void setDirector(String director) {
		this.director = director;
	}

	public int getReleaseYear() {
		return releaseYear;
	}

	public void setReleaseYear(int releaseYear) {
		this.releaseYear = releaseYear;
	}

	public String[] getGenres() {
		return genres;
	}

	public void setGenres(String[] genres) {
		this.genres = genres;
	}

	public float getRating() {
		return rating;
	}

	public void setRating(float rating) {
		this.rating = rating;
	}

	public String[] getCast() {
		return cast;
	}

	public void setCast(String[] cast) {
		this.cast = cast;
	}

	public String getWriter() {
		return writer;
	}

	public void setWriter(String writer) {
		this.writer = writer;
	}

	public int getDuration() {
		return duration;
	}

	public void setDuration(int duration) {
		this.duration = duration;
	}

	public Set<String> getLanguage() {
		return language;
	}

	public void setLanguage(Set<String> language) {
		this.language = language;
	}

	public String getSynopsis() {
		return synopsis;
	}

	public void setSynopsis(String synopsis) {
		this.synopsis = synopsis;
	}

	public String getPosterURL() {
		return posterURL;
	}

	public void setPosterURL(String posterURL) {
		this.posterURL = posterURL;
	}

}
