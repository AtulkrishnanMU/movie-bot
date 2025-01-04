package me.botbabu.util;

import java.io.IOException;
import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;

import me.botbabu.dto.Movie;
import me.botbabu.dto.Rating;

public class MovieUtil {

	public void fetchRatings(String url, List<Rating> ratingsList) {
		try {
			Document document = Jsoup.connect(url).get();
			Elements rows = document.select("tr");

			for (Element row : rows) {
				String name = cleanText(row.selectFirst("a.name"));
				String ratingStars = cleanText(row.selectFirst("span"));
				Element likesElement = row.selectFirst("span.has-icon.icon-16.icon-liked");

				if (name != null && !name.isEmpty()) {
					int rating = parseRating(ratingStars);
					boolean liked = likesElement != null;

					// Shorten long names and format ratings
					if (name.length() > 19) {
						name = name.replace(" (aka Pardesi)", "") + "...";
					}

					// Add the rating to the list
					if (liked) { ratingsList.add(new Rating(name, rating, true));}
					else {
						ratingsList.add(new Rating(name, rating, false));
					}
				}
			}
		} catch (Exception e) {
			System.out.println("Error fetching data from: " + url + " - " + e.getMessage());
		}
	}

	public int parseRating(String ratingStars) {
		if (ratingStars == null) {
			return 0;
		}

		int rating = 0;
		for (char c : ratingStars.toCharArray()) {
			if (c == '★') {
				rating += 2;
			} else if (c == '½') {
				rating += 1;
			}
		}
		return rating; // Convert to a scale of 10
	}

	public String cleanText(Element element) {
		if (element == null) {
			return "";
		}
		return element.text().replaceAll("\\<.*?\\>", "").trim();
	}

	public String getMovieLbLink(String movieName) {

		StringBuffer lbSearchLink = new StringBuffer();
		String movieLbLink = null;

		lbSearchLink.append("https://www.google.com/search?q=").append(movieName).append("+movie+letterboxd");

		try {
			Document lbDocument = Jsoup.connect(String.valueOf(lbSearchLink)).get();

			Elements links = lbDocument.select("a[href^=https://letterboxd.com/film]");

			if (!links.isEmpty()) {
				Element firsLbLink = links.first();
				movieLbLink = firsLbLink.attr("href");
				movieLbLink = movieLbLink.replace("/releases", "").replace("/details", "").replace("/watch", "")
						.replace("/genres", "").replace("/reviews", "");

			} else {
				System.out.println("No matching links found.");
			}

		} catch (IOException e) {
			e.printStackTrace();
		}

		return movieLbLink;
	}

	public Movie getLbDetails(String movieLbLink) {

		Movie movie = null;

		try {

			// Connect to the movie link page
			Document document = Jsoup.connect(movieLbLink).get();

			// Extract meta information
			String title = document.select("meta[property=og:title]").attr("content");
			String description = document.select("meta[name=description]").attr("content");
			String imageUrl = getPosterUrl(movieLbLink);
			String director = document.select("meta[name=twitter:data1]").attr("content");

			int duration = 0;
			try {
				duration = Integer.parseInt(document.selectFirst("p.text-link.text-footer").text().split(" ")[0]);
			} catch (Exception e) {
			}

			float rating = 0;
			try {
				rating = Float.parseFloat(document.select("meta[name=twitter:data2]").attr("content").split(" ")[0])
						* 2;
			} catch (Exception e) {
				e.printStackTrace();
				System.out.println("failed to calculated rating");
			}
			String[] genres = (document.select("#tab-genres h3:contains(Genre) + .text-sluglist p a.text-slug").text()
					.split(" "));

			Set<String> language = new HashSet<String>();

			for (Element element : document.select("h3:contains(Language) + .text-sluglist p a.text-slug")) {
				language.add(element.text());
			}

			List<String> country = new ArrayList<String>();

			for (Element element : document.select("h3:contains(Countr) + .text-sluglist p a.text-slug")) {
				country.add(element.text());
			}

			Date releaseDate = null;

			SimpleDateFormat dateFormat = new SimpleDateFormat("dd MMM yyyy", Locale.ENGLISH);
			try {
				releaseDate = dateFormat.parse(document.selectFirst(".release-table .listitem .cell h5.date").text());
			} catch (Exception e) {
			}

			movie = new Movie();
			movie.setTitle(title);
			movie.setSynopsis(description);
			movie.setPosterURL(imageUrl);
			movie.setRating(rating);
			movie.setDirector(director);
			movie.setDuration(duration);
			movie.setLbLink(movieLbLink);
			movie.setGenres(genres);
			movie.setLanguage(language);
			movie.setCountry(country);
			movie.setReleaseDate(releaseDate);

		} catch (IOException e) {
			e.printStackTrace();
		}

		return movie;
	}

	public String getReleaseDetails(Movie movie) {

		Date releaseDate = movie.getReleaseDate();

		if (releaseDate != null) {
			Date currentDate = new Date();

			// Check if the release date is in the future
			if (releaseDate.after(currentDate)) {
				return "Upcoming";
			}

			// Get the current time and subtract 1 month
			Calendar calendar = Calendar.getInstance();
			calendar.setTime(currentDate);
			calendar.add(Calendar.MONTH, -1);
			Date oneMonthAgo = calendar.getTime();

			// Check if the release date is within the last 1 month
			if (!releaseDate.before(oneMonthAgo)) {
				return "New";
			}
		}
		// If it's neither upcoming nor a new movie, it's an old movie
		return null;
	}

	private static String getPosterUrl(String url) {
		try {
			// Fetch the HTML content of the page
			Document document = Jsoup.connect(url).get();

			// Select the script tag containing JSON-LD data
			Element scriptElement = document.selectFirst("script[type=application/ld+json]");
			if (scriptElement != null) {
				// Extract the JSON data
				String scriptContent = scriptElement.html();

				// Clean and parse the JSON using JsonReader for lenient parsing
				String jsonData = scriptContent.split(" \\*/")[1].split("/\\* \\[\\[>")[0].trim();
				JsonReader reader = new JsonReader(new StringReader(jsonData));
				reader.setLenient(true); // Allow lenient parsing

				JsonObject jsonObject = JsonParser.parseReader(reader).getAsJsonObject();

				// Get the image URL
				return jsonObject.get("image").getAsString();
			} else {
				System.out.println("JSON-LD script not found!");
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Error parsing JSON: " + e.getMessage());
		}
		return null;
	}

	// Utility method to extract year from Date
//	private static int getYear(Date date) {
//		Calendar calendar = Calendar.getInstance();
//		calendar.setTime(date);
//		return calendar.get(Calendar.YEAR);
//	}

}
