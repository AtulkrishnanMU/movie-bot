package me.botbabu.dto;

public class Rating {
	
	private String username;
	private float rating;
	private boolean heart;
	
	public boolean isHeart() {
		return heart;
	}
	public void setHeart(boolean heart) {
		this.heart = heart;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	
	public float getRating() {
		return rating;
	}
	public void setRating(float rating) {
		this.rating = rating;
	}
	public Rating(String username, float rating, boolean heart) {
		super();
		this.username = username;
		this.rating = rating;
		this.heart = heart;
	}
	@Override
	public String toString() {
		return "Rating [username=" + username + ", rating=" + rating + ", heart=" + heart + "]";
	}
}
