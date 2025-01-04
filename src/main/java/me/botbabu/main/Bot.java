package me.botbabu.main;

import java.awt.Color;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import me.botbabu.controller.MovieController;
import me.botbabu.dto.Movie;
import me.botbabu.dto.Rating;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.requests.GatewayIntent;
import java.util.concurrent.CompletableFuture;

public class Bot extends ListenerAdapter {
    public static void main(String[] args) throws Exception {
        // Create JDABuilder and enable the MESSAGE_CONTENT intent
        JDABuilder builder = JDABuilder.createDefault("DISCORD_TOKEN")
            .enableIntents(GatewayIntent.MESSAGE_CONTENT)  // Enable the MESSAGE_CONTENT intent
            .addEventListeners(new Bot());  // Add your event listener (Bot)

        // Build the JDA instance
        JDA jda = builder.build();  // This creates and starts the bot

        // You can now interact with jda if necessary, but it will automatically be active
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        Message message = event.getMessage();
        String content = message.getContentRaw();
        StringBuffer director = new StringBuffer();
        StringBuffer genres = new StringBuffer();
        StringBuffer languages = new StringBuffer();
        StringBuffer country = new StringBuffer();

        if (content.startsWith("!f")) {
        	
            String movieName = content.replace("!f", "").trim();

            MovieController movieController = new MovieController();
            Movie movie = movieController.fetchMovieDetails(movieName);

            if (movie != null) {
                EmbedBuilder embed = new EmbedBuilder();
                embed.setTitle(movie.getTitle(), movie.getLbLink());
                String synopsis = movie.getSynopsis();
                if (synopsis.length() > 200) {
                    synopsis = synopsis.substring(0, 200) + "...";
                }
                embed.setDescription(synopsis);
                embed.setThumbnail(movie.getPosterURL());
                
                float rating = movie.getRating();
                String ratingText = "NA";
                
                int duration = movie.getDuration();
                String durationText = "NA";
                
                if (rating != 0) {
                	ratingText = String.valueOf(movie.getRating());
                }
                if (duration !=0) {
                	durationText = String.valueOf(duration);
                }
                
                embed.addField("Rating", ratingText + "/10", true);
                
                embed.addField("Director", String.valueOf(director.append("`").append(movie.getDirector()).append("`")), false);
                embed.addField("Genres", String.valueOf(genres.append("`").append(String.join(", ", movie.getGenres())).append("`")), true);
                embed.addField("Language(s)", String.valueOf(languages.append("`").append(String.join(", ", movie.getLanguage())).append("`")), true);
                embed.addField("Country", String.valueOf(country.append("`").append(String.join(", ", movie.getCountry())).append("`")), true);
                
                Date releaseDate = movie.getReleaseDate();
                
				if (releaseDate != null) {
					SimpleDateFormat sdf = new SimpleDateFormat("MMMM dd, yyyy"); // You can change the format as needed
					String formattedDate = "`" + sdf.format(releaseDate) + "`";
					
					String releaseDetail = movie.getReleaseDetail();

					if (releaseDetail == "New") {
						embed.addField(":star:New Release:star: ", formattedDate, false);
					}

					if (releaseDetail == "Upcoming") {
						embed.addField(":hourglass:Upcoming Release:hourglass: ", formattedDate, false);
					}
				}

                embed.setColor(Color.ORANGE);
                
                embed.setFooter(durationText  + " minutes", null);

                event.getChannel().sendMessageEmbeds(embed.build()).queue();
            } else {
                event.getChannel().sendMessage("Sorry, I couldn't find any details for that movie.").queue();
            }
        }
        
        else if (content.startsWith(".wk")) {
        	
            String movieName = content.replace("!f", "").trim();

            MovieController movieController = new MovieController();
            		
            // Run both calls concurrently
            CompletableFuture<Movie> movieFuture = CompletableFuture.supplyAsync(() -> movieController.fetchMovieDetails(movieName));
            CompletableFuture<List<Rating>> ratingsFuture = CompletableFuture.supplyAsync(() -> movieController.fetchMovieRatings(movieName));

            // Wait for both results
            Movie movie = movieFuture.join();
            List<Rating> ratings = ratingsFuture.join();

            if (ratings != null) {
                EmbedBuilder embed = new EmbedBuilder();
                embed.setTitle(movie.getTitle(), movie.getLbLink());
                embed.setThumbnail(movie.getPosterURL());
                embed.setColor(new Color(0, 128, 128));

                // Build the ratings display
                StringBuilder ratingBuilder = new StringBuilder();
                int totalRatings = 0;
                double ratingSum = 0;
                int watchedCount = 0;

                for (Rating rating : ratings) {
                    String heart = rating.isHeart() ? "<:dfds:1123838948611985418>" : ""; // heart emoji
                    if (rating.getRating() > 0) {
                        ratingBuilder.append(rating.getUsername())
                            .append(" **")
                            .append((int) rating.getRating())
                            .append("** ")
                            .append(heart)
                            .append("\n");
                        totalRatings++;
                        ratingSum += rating.getRating();
                    } else {
                        ratingBuilder.append(rating.getUsername()).append(" --\n");
                    }
                    watchedCount++;
                }

                double averageRating = totalRatings > 0 ? ratingSum / totalRatings : 0.0;
                
                System.out.println(ratingBuilder);

                //embed.addField("who knows", ratingBuilder.toString(), false);
                embed.setDescription(ratingBuilder.toString());
                embed.setFooter(String.format("%.1f from %d members, %d watched", averageRating, totalRatings, watchedCount), null);

                event.getChannel().sendMessageEmbeds(embed.build()).queue();
            } else {
                event.getChannel().sendMessage("Sorry, I couldn't find any details for that movie.").queue();
            }

        }
        
        
    }
}
