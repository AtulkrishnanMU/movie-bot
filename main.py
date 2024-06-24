import discord
import os
import imdb
from discord.ext import commands, tasks
from keep_alive import keep_alive
from discord import app_commands
import random
import random
import json
from bs4 import BeautifulSoup
from genres import data
from genres import url
from genres import users
import requests
import re
import sqlite3
from similar import get_similar_movies
from similar import get_bestsimilar_links

history = [""]

connection = sqlite3.connect('myfirst.db')
crs = connection.cursor()

#grr
#del db['897091711824703518']
#del db['749884100768432128']
#del db['797900903184859158']

gemini_movie = ""

ans = "fgdzfgasgsdg"
pllt = ""
nm = ""
imggg = ""
uarel = ""
dick = {}
count1 = 0

from google.generativeai import GenerativeModel

import pathlib
import textwrap

import google.generativeai as genai

# Add the API key to the secrets manager in Colab
GOOGLE_API_KEY = os.environ['gemini_key']

# Configure the genai with the API key
genai.configure(api_key=GOOGLE_API_KEY)

star = crs.execute("SELECT DISTINCT COUNT(*) FROM movies")

reply_list = ["ip address", "my honest reaction", "ur mom", "shut up", "kill yourself", "dimden", "your mother", "touch grass", "Get some bitches", "womp womp cry about it", "sad meme", "i have feelings", "die", "depressed"]

def get_insult(language='en', response_type='json'):
  url = 'https://evilinsult.com/generate_insult.php'
  params = {
      'lang': language,
      'type': response_type
  }
  try:
      response = requests.get(url, params=params)
      response.raise_for_status()  # Check for HTTP errors
      if response_type == 'json':
          data = response.json()
          return data.get('insult', 'No insult found.')
      else:
          return response.text
  except requests.exceptions.RequestException as e:
      return f"An error occurred: {e}"
    

for i in star:
  print(i)

connection.commit()
connection.close()

data = data
url = url
users = users

prefix = "!!"

list1 = []
list1.append(0)
dict122 = {}

s2 = ""
genres = []


async def get_random_gif(keyword):
  # Construct the search URL with the keyword
  url = f'https://tenor.com/search/{keyword}-gifs'

  # Send a GET request to the URL
  response = requests.get(url)

  # Parse the HTML content
  soup = BeautifulSoup(response.text, "html.parser")

  # Find all div elements with class "Gif"
  gif_divs = soup.find_all("div", class_="Gif")

  gifs = []

  # Iterate through each div to extract the GIF URL
  for div in gif_divs:
      # Find the img tag within the div
      img_tag = div.find("img")
      # Extract the src attribute which contains the GIF URL
      gif_url = img_tag["src"]
      gifs.append(gif_url)

  # Select a random gif URL from the list
  random_gif_url = random.choice(gifs)
  return random_gif_url

def searcho(o):
  s = ""
  try:
    l2 = str(o)
    st1 = l2.find('film/')
    name = l2[st1 + 5:]

    s = "https://letterboxd.com/travis_pickle12/friends/film/" + str(
      name).replace("releases/", "") + "/"
    s = s.replace("ratings", "")
    #s = "https://letterboxd.com/film/" + str(lname) + "/"

    page = requests.get(s)
    code = page.status_code
    #print(name)
    #print(page.status_code)

    #print(genres)
    if code == 404:
      s = "https://letterboxd.com/travis_pickle12/friends/film/" + str(
        name) + "/"
      page = requests.get(s)
      code = page.status_code
      #print(name)
      #print(page.status_code)
  except:
    print("error")
  return s


def searchf(movienm):
  source = requests.get('https://www.google.com/search?q=' + movienm +
                        '+movie+letterboxd')
  source.raise_for_status

  soup = BeautifulSoup(source.text, 'html.parser')

  a = soup.find_all('a')

  #print(a)
  for i in a:
    if 'https://letterboxd.com/' in str(i) and '/film' in str(i):
      l = str(i)
      st = l.find('https://letterboxd.com/')
      end = l.find('/&amp;')
      ##print(st, " ", end)
      s = (l[st:end])
      if st != -1 and end != -1:
        break

  #print('s = ', s)
  s = s.replace('ratings', '')
  #print('s = ', s)
  strt = s.find('/film')
  s = 'https://letterboxd.com' + s[strt:]
  #print('s = ', s)
  return s


client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix=prefix,
                   case_insensitive=True,
                   intents=discord.Intents.all())

c = 2
nlist = []

from datetime import date, timedelta

first_day_of_this_month = date.today().replace(day=1)
last_day_prev_month = first_day_of_this_month - timedelta(days=1)
prev_month_name = last_day_prev_month.strftime("%B")
month = (prev_month_name[:3])

import discord
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)


async def fetch_popular_movies():
  # URL of the Rotten Tomatoes popular movies page
  url = 'https://editorial.rottentomatoes.com/guide/popular-movies/'

  # Send a GET request to the website
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the movie items
    movie_items = soup.find_all(
      'div', class_='col-sm-18 col-full-xs countdown-item-content')

    # Extract and return the movie names, years, and scores
    popular_movies = []
    for idx, item in enumerate(movie_items[:10],
                               start=1):  # Limit to first 15 movies
      title = item.find('div', class_='article_movie_title').find('a').text
      year = item.find('span', class_='subtle start-year').text.strip('()')
      score_span = item.find('span', class_='tMeterScore')
      score_text = score_span.text.strip() if score_span else None

      # Convert score text to integer, removing percentage sign if present
      if score_text:
        score_text = score_text.rstrip('%')
        score = int(score_text) if score_text.isdigit() else None
      else:
        score = None

      # Determine circle color based on score
      if score is None:
        circle = '--'  # Black circle for no score available
      elif score >= 70:
        circle = ':green_circle:'  # Green circle
      elif 50 <= score < 70:
        circle = ':yellow_circle:'  # Yellow circle
      else:
        circle = ':red_circle:'  # Red circle

      popular_movies.append(
        f"{title} ({year})"
      )

    return popular_movies
  else:
    return []


ou = ""
summ = 0


def create_embed(movie_data, page_number, userr, avatar):
  color = discord.Color.from_rgb(random.randint(0,
                                                255), random.randint(0, 255),
                                 random.randint(0, 255))
  embed = discord.Embed(title="Month Diary", color=color)
  embed.set_author(name=userr, icon_url=avatar)
  for idx, movie in enumerate(movie_data, start=(page_number - 1) * 10 +
                              1):  # Start numbering from 1
    title = movie.split('](')[0]
    link = movie.split('](')[1].split(')')[0]
    date = movie.split(') ')[1].split(', ')[0]
    rating = movie.split(', ')[-1]
    if rating == '0/10':
      rating = ''
    embed.add_field(
      name=f"{idx}. {title}",  # Use the counter for the field's name
      value=f"[{date}, {rating}]({link})",
      inline=False)
  return embed


@client.event
async def on_ready():
  #await tree.sync(guild=discord.Object(id=562260964263591965))
  print('We have logged in as {0.user}'.format(client))
  #called_once_a_day.start()


@client.event
async def on_message(msg):

  global searchf

  global s2

  if msg.author == client.user:

    return

  if msg.content.startswith('$hello'):

    await msg.channel.send("hello")

  if msg.content.startswith('$hello'):
    await msg.channel.send("hello")

  # If the message starts with '!sim', find similar movies
  if msg.content.startswith('!sim'):

    try:
      # Get the movie name by removing '!sim' and any extra spaces
      movie_name = msg.content[4:].strip()
      #print(movie_name)

      # Get the movie link based on the movie name
      movie_link = get_bestsimilar_links(movie_name)
      #print(movie_link)

      # Get a list of similar movies using the movie link
      similar_movies = get_similar_movies(movie_link)
      #print(similar_movies)

      # Create an embed to display the list of similar movies
      embed = discord.Embed(title=f"Movies similar to {similar_movies[0]}")

      # Make a single string with each movie name on a new line
      movie_list_text = "\n".join(similar_movies)

      # Set the description of the embed to this list of movie names
      embed.description = movie_list_text

      # Send the embed to the Discord channel
      await msg.reply(embed=embed)
    except:
      # Create an embed to display the list of similar movies
      embed = discord.Embed(title="OOPS!")
      embed.description = "The movie you entered is not in our database. Please try again."
      await msg.reply(embed=embed)

  if msg.content == "!roast" and msg.reference:

    # Check if the message is a reply to another message
    replied_message = await msg.channel.fetch_message(msg.reference.message_id)

    try:
      if replied_message:
        if replied_message.embeds:
          embed = replied_message.embeds[0]
          replied_content = (embed.title or "") + " " + (embed.description or "")
        else:
          # Extract the content of the replied message
          replied_content = replied_message.content
      for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
          print(m.name)
  
      # Generate text from text inputs
      model = genai.GenerativeModel('gemini-pro')
      response = model.generate_content('"' + replied_content +
                                        '" roast the guy who send this message')
  
      # Display the response text
      resp = str(response.text)
  
      resp = resp.replace("Gemini", "Tintin Quarantino")
      resp = resp.replace(" developed by Google", "").replace("Sure, here is a response in not more than 20 words:", "").replace("**", "").lstrip()

      substring = "in 20 words"

      # Split the string into sentences
      sentences = resp.split('.')

      # Filter out sentences containing the substring
      filtered_sentences = [sentence for sentence in sentences if substring not in sentence]

      # Join the remaining sentences back into a single string
      resp = '.'.join(filtered_sentences).strip() + '.'

      if len(resp) > 2000:
        resp1, resp2 = resp[:2000], resp[2000:]
        await replied_message.reply(resp1)
        await msg.channel.send(resp2)
      else:
        await replied_message.reply(resp)

    except:
      # Define the probabilities
      choices = ["gif", "insult"]

      # Randomly select an item based on the defined probabilities
      selection = random.choices(choices)
      #print(selection)

      if selection == ['insult']:
        #print('yes')
        insult = get_insult()
        await msg.reply(insult)
      else:
        # Get a random string from the list
        reply = random.choice(reply_list)

        gif_url = await get_random_gif(reply)

        if gif_url == '/assets/img/gif-maker-entrypoints/search-entrypoint-optimized.gif':
          gif_url = random.choices(['https://media1.tenor.com/m/qzaJRkZ2EskAAAAC/tww-the-wild-west.gif','https://media.tenor.com/KJVlOt5r1pkAAAAi/discord-discordgifemoji.gif'])

        await replied_message.reply(gif_url)

  elif msg.reference and msg.reference.resolved.embeds and client.user.mentioned_in(
      msg):
    replied_embed = msg.reference.resolved.embeds[0]

    try:
      title = replied_embed.title
      description = replied_embed.description
      print(description)
      #description = description.replace(":dfds:", "gave heart")
    except:
      title = ""
      description = ""
  
    mssg = msg.content
    mssg = mssg.replace("<@1095747091185270874>", "Hi")
    mssg = mssg.replace("Tintin Quarantino", "Gemini")

    for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        print(m.name)

    # Generate text from text inputs
    model = genai.GenerativeModel('gemini-pro')

    try:
      offens = model.generate_content('A said to B " ' + mssg + '.". is A calling bad words at B?')
      off = offens.text
    except:
      off = "i love you"

    if str(off).lower().startswith("yes"):

      # Define the probabilities
      choices = ["gif", "insult"]

      # Randomly select an item based on the defined probabilities
      selection = random.choices(choices)

      if selection == ['insult']:
        insult = get_insult()
        await msg.reply(insult)
      else:
        # Get a random string from the list
        reply = random.choice(reply_list)
  
        gif_url = await get_random_gif(reply)

        if gif_url == '/assets/img/gif-maker-entrypoints/search-entrypoint-optimized.gif':
          gif_url = random.choices(['https://media1.tenor.com/m/qzaJRkZ2EskAAAAC/tww-the-wild-west.gif','https://media.tenor.com/KJVlOt5r1pkAAAAi/discord-discordgifemoji.gif'])
  
        # Send the gif in the channel where the original message was sent
        await msg.reply(gif_url)
    else:  
      try:
        response = model.generate_content(title + description + " " + mssg + ". Respond in not more than a 20 words")
    
        # Display the response text
        resp = str(response.text).replace("<center>","*").replace("</center>","*")
    
        resp = resp.replace("Gemini", "Tintin Quarantino")
        resp = resp.replace(" developed by Google", "").replace("Sure, here's a response in not more than 20 words:", "").replace("**", "").lstrip()

        substring = "in 20 words"

        # Split the string into sentences
        sentences = resp.split('.')

        # Filter out sentences containing the substring
        filtered_sentences = [sentence for sentence in sentences if substring not in sentence]

        # Join the remaining sentences back into a single string
        resp = '.'.join(filtered_sentences).strip() + '.'
    
        #print("response = ", resp)
    
        if len(resp) > 2000:
          resp1, resp2 = resp[:2000], resp[2000:]
          await msg.reply(resp1)
          await msg.channel.send(resp2)
        else:
          await msg.reply(resp)
      except:
        # Search for a random gif based on the title
        gif_url = await get_random_gif(msg.content)

        if gif_url == '/assets/img/gif-maker-entrypoints/search-entrypoint-optimized.gif':
          gif_url = random.choices(['https://media1.tenor.com/m/qzaJRkZ2EskAAAAC/tww-the-wild-west.gif','https://media.tenor.com/KJVlOt5r1pkAAAAi/discord-discordgifemoji.gif'])
  
        # Send the gif in the channel where the original message was sent
        await msg.reply(gif_url)
  
  elif client.user.mentioned_in(msg) or (
      msg.reference and msg.reference.resolved.author == client.user):

    try:
      mssg = msg.content
      mssg = mssg.replace("<@1095747091185270874>", "")
  
      for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
          print(m.name)
  
      # Generate text from text inputs
      model = genai.GenerativeModel('gemini-pro')

      try:
        offens = model.generate_content('A said to B " ' + mssg + '.". is A calling bad words at B?')
        off = offens.text
      except:
        off = "i love you"

      if str(offens.text).lower().startswith("yes"):

        # Define the probabilities
        choices = ["gif", "insult"]

        # Randomly select an item based on the defined probabilities
        selection = random.choices(choices)
        #print(selection)

        if selection == ['insult']:
          #print('yes')
          insult = get_insult()
          await msg.reply(insult)
        else:
          # Get a random string from the list
          reply = random.choice(reply_list)
  
          gif_url = await get_random_gif(reply)

          if gif_url == '/assets/img/gif-maker-entrypoints/search-entrypoint-optimized.gif':
            gif_url = random.choices(['https://media1.tenor.com/m/qzaJRkZ2EskAAAAC/tww-the-wild-west.gif','https://media.tenor.com/KJVlOt5r1pkAAAAi/discord-discordgifemoji.gif'])
  
          # Send the gif in the channel where the original message was sent
          await msg.reply(gif_url)
      else:  
    
        if msg.reference and msg.reference.resolved:
          # Get the referenced message
          referenced_message = msg.reference.resolved
          # Get the content of the referenced message
          referenced_content = referenced_message.content

          greet = model.generate_content('Is this message a greeting - " ' + mssg + '."')
          gr = greet.text

          if str(gr).lower().startswith("yes"):
            response = model.generate_content(str(mssg))
            
          else:
            response = model.generate_content(str('In your previous response, you said : "' + referenced_content + '". Now, the I have replied with : ' + mssg + ". Respond to my reply in not more than 20 words."))
    
        else:
          greet = model.generate_content('Is this message a greeting - " ' + mssg + '."')
          gr = greet.text

          if str(gr).lower().startswith("yes"):
            response = model.generate_content(str(mssg))
          else:
            response = model.generate_content(str(mssg) + ". Reply in not more than 20 words.")
        # Display the response text
        resp = str(response.text).replace("<center>","*").replace("</center>","*")
    
        resp = resp.replace("Gemini, a large multi-modal model, trained by Google", "Tintin Quarantino").replace("Gemini, a multi-modal AI language model developed by Google", "").replace("Gemini, a large multi-modal model, developed by Google", "Tintin Quarantino").replace("Sure, here's a response in not more than 20 words:", "").replace("**", "").lstrip()

        print(resp)

        substring = "n 20 words"

        # Split the string into sentences
        sentences = resp.split('.')

        # Filter out sentences containing the substring
        filtered_sentences = [sentence for sentence in sentences if substring not in sentence]

        # Join the remaining sentences back into a single string
        resp = '.'.join(filtered_sentences).strip() + '.'
  
        #print("response = ", resp)
        if len(resp) > 2000:
          resp1, resp2 = resp[:2000], resp[2000:]
          await msg.reply(resp1)
          await msg.channel.send(resp2)
        else:
          await msg.reply(resp)
    except:
      # Search for a random gif based on the title
      gif_url = await get_random_gif(msg.content)

      if gif_url == '/assets/img/gif-maker-entrypoints/search-entrypoint-optimized.gif':
        gif_url = random.choices(['https://media1.tenor.com/m/qzaJRkZ2EskAAAAC/tww-the-wild-west.gif','https://media.tenor.com/KJVlOt5r1pkAAAAi/discord-discordgifemoji.gif'])

      # Send the gif in the channel where the original message was sent
      await msg.reply(gif_url)

  if msg.content == "!pop":
    popular_movies = await fetch_popular_movies()
    if popular_movies:
      embed = discord.Embed(title="Popular Movies Right Now", color=discord.Color.blue())
      embed.description = "\n".join(popular_movies)
      await msg.channel.send(embed=embed)
    else:
      await msg.channel.send("Failed to retrieve popular movies.")

  if msg.content.startswith('!wl'):

    import json


    o = ""
    linkkk = ""

    s = ""
    x = str(msg.content).replace('!wl', '')
    blah = str(x).lower().strip().split(" ")
    genre = ""

    input = blah[0]
    try:
      loda = blah[1].split(",")
      sortedloda = sorted(loda)
      for i in sortedloda:
        genre = genre + i + "+"
      genre = genre[:-1]
    except:
      genre = ""

    if genre != "":
      userURL = "https://letterboxd.com/" + str(
        input) + "/watchlist/genre/" + str(genre) + "/"
    else:
      userURL = "https://letterboxd.com/" + str(input) + "/watchlist/"

    source = requests.get('https://letterboxd.com/' + str(input) + '/')
    source.raise_for_status

    soup = BeautifulSoup(source.text, 'html.parser')

    f = soup.find_all('meta')
    ##print(f)
    strt = str(f).find("https://a.ltrbxd.com/resized/avatar/upload")
    end = str(f).find('.jpg')
    ##print(strt, " ", end)
    if strt == -1:
      avatar = "https://s.ltrbxd.com/static/img/avatar220.1dea069d.png"
    else:
      avatar = str(f)[strt:end] + ".jpg"

    source = requests.get(userURL)
    source.raise_for_status

    soup = BeautifulSoup(source.text, 'html.parser')

    hggh = soup.find_all('li', class_="paginate-page")

    for i in hggh:
      strt = str(i).find("/watchlist/page/")
      end = str(i).find('/">')
      ##print(str(i)[strt:end])
      pgnum = ""
      pgg = str(i)[strt:end]
      for i in pgg:
        if i.isdigit():
          pgnum = pgnum + i
      # print result
    try:
      #print("pgnum = ", pgnum)
      pgnumm = random.randint(0, int(pgnum))
    except:
      pgnumm = 0

    #print(userURL + "page/" + str(pgnumm) + "/")

    source = requests.get(userURL + "page/" + str(pgnumm) + "/")
    source.raise_for_status

    soup = BeautifulSoup(source.text, 'html.parser')

    a = soup.find_all('li')

    list123 = []

    for i in a:
      f = i.find('div')
      if f != None:
        fi = str(f)
        strt = fi.find('data-target-link="/film/')
        end = fi.find('/" data-target-link-target')
        ##print(fi[strt:end])
        list123.append("https://letterboxd.com/" +
                       fi[strt:end].replace('data-target-link="/', ''))

    list123.pop(0)

    #print(list123)

    urrl = str(random.choice(list123))

    r = requests.get(urrl)
    soup = BeautifulSoup(r.text)

    f = soup.find_all('meta')
    plot = str(f[3]).replace('<meta content="', "")
    plot = plot.replace('" name="description"/>', "")
    ##print(plot)

    script_w_data = soup.select_one('script[type="application/ld+json"]')
    json_obj = json.loads(
      script_w_data.text.split(' */')[1].split('/* ]]>')[0])
    linnk = (json_obj['image'])

    #print("avatar = ", avatar)
    #print(linnk)

    l2 = urrl

    source = requests.get(l2)
    source.raise_for_status

    soup = BeautifulSoup(source.text, 'html.parser')

    ##print(soup)

    f = soup.find_all('meta')
    for i in f:
      if "og:title" in str(i):
        moviename = str(i).replace('<meta content="', "")
        moviename = moviename.replace('" property="og:title"/>', "")

    #print(moviename)

    embed = discord.Embed(
      colour=discord.Colour.dark_grey(),
      description=str(plot[:120].replace("&quot;", '"')).replace(
        "<meta content='", "") + "...",
      title=moviename,
      url=urrl)
    #foot = ""
    #embed.set_footer(text = foot)
    embed.set_author(name="from " + str(input) + "'s watchlist:",
                     url="https://letterboxd.com/" + str(input) + "/",
                     icon_url=avatar)
    embed.set_thumbnail(url=linnk)
    #embed.set_thumbnail(url = linkk)+

    await msg.reply(embed=embed)

  if msg.content.startswith('!wk'):

    try:

      global list1
      global nlist
      list1 = [0]
      nlist = [0]
      s = ""
      x = str(msg.content).replace('!wk', '')
      #x.pop(0)
      title = str(x)
      #print(title)
      movienm = title.replace(' ', '+')

      o = searchf(movienm)
      o = o.replace("/releases", "").replace("/details", "").replace("/watch", "")
      #print(o)
      s = searcho(o).replace("/releases", "")
      s = searcho(o).replace("/details", "")
      s = searcho(o).replace("/watch", "")

      if title.lower().strip() == 'u turn 2016' or title.lower().strip(
      ) == 'u turn kannada':
        s = 'https://letterboxd.com/travis_pickle12/friends/film/u-turn-2016-1/'
        o = 'https://letterboxd.com/film/u-turn-2016-1/'
      elif title.lower().strip(
      ) == 'portrait of a lady on fire' or title.lower().strip(
      ) == 'portrait of lady on fire' or title.lower().strip(
      ) == 'portrait of lady':
        s = 'https://letterboxd.com/travis_pickle12/friends/film/portrait-of-a-lady-on-fire/'
        o = 'https://letterboxd.com/film/portrait-of-a-lady-on-fire/'
      elif title.lower().strip() == 'kerala crime files' or title.lower(
      ).strip() == 'kerala crime':
        s = 'https://letterboxd.com/travis_pickle12/friends/film/kerala-crime-files-shiju-parayil-veedu-neendakara/'
        o = 'https://letterboxd.com/film/kerala-crime-files-shiju-parayil-veedu-neendakara/'
      elif 'almost pyaar' in title.lower().strip(
      ) or 'dj mohabbat' in title.lower().strip():
        s = 'https://letterboxd.com/travis_pickle12/friends/film/almost-pyaar-with-dj-mohabbat/'
        o = 'https://letterboxd.com/film/almost-pyaar-with-dj-mohabbat/'
        
      source = requests.get(str(s))
      source.raise_for_status

      out = ":clapper::popcorn: "

      soup = BeautifulSoup(source.text, 'html.parser')

      tr = soup.find_all('tr')

      sum = 0
      cnt = 0
      cnt1 = 0

      dict122 = {}

      for i in tr:
        name = i.find('a', class_="name")
        rat = i.find('span')
        likes = i.find('span', class_="has-icon icon-16 icon-liked")
        name_ = re.sub("\<.*?\>", "", str(name))
        rat_ = re.sub("\<.*?\>", "", str(rat))
        count = 0
        for i in rat_:
          if i == '★':
            count = count + 1
          elif i == '½':
            count = count + 0.5

        rat_ = int(count * 2)
        rat__ = str(rat_)

        if '10' in rat__:
          rat__ = "a" + rat__

        if 'span class=' in str(likes):
          rat__ = rat__ + "<:dfds:1123838948611985418>"

        if len(name_) > 19:
          name_ = str(name_.replace(" (aka Pardesi)", "")[:19]) + "..."
        else:
          name_ = str(name_)

        name_ = re.sub("\(.*?\)", "", name_)

        if rat_ != 0 and name_ != 'None':
          sum = sum + rat_
          cnt = cnt + 1
          cnt1 = cnt1 + 1
          dict122[str(name_)] = rat__
        elif rat_ == 0 and name_ != 'None':
          cnt1 = cnt1 + 1
          dict122[str(name_)] = rat__.replace("0", "--")

      try:
        s2 = s + "page/2/"
        source = requests.get(str(s2))
        source.raise_for_status

        #out = ":clapper::popcorn:"

        soup = BeautifulSoup(source.text, 'html.parser')

        tr = soup.find_all('tr')

        #sum = 0
        #cnt = 0
        #cnt1 = 0

        #dict = {}

        for i in tr:
          name = i.find('a', class_="name")
          rat = i.find('span')
          likes = i.find('span', class_="has-icon icon-16 icon-liked")
          name_ = re.sub("\<.*?\>", "", str(name))
          rat_ = re.sub("\<.*?\>", "", str(rat))
          count = 0
          for i in rat_:
            if i == '★':
              count = count + 1
            elif i == '½':
              count = count + 0.5

          rat_ = int(count * 2)
          rat__ = str(rat_)

          if '10' in rat__:
            rat__ = "a" + rat__

          if 'span class=' in str(likes):
            rat__ = rat__ + "<:dfds:1123838948611985418>"

          if len(name_) > 19:
            name_ = str(name_.replace(" (aka Pardesi)", "")[:19]) + "..."
          else:
            name_ = str(name_)

          name_ = re.sub("\(.*?\)", "", name_)

          if rat_ != 0 and name_ != 'None':
            sum = sum + rat_
            cnt = cnt + 1
            cnt1 = cnt1 + 1
            dict122[str(name_)] = rat__
          elif rat_ == 0 and name_ != 'None':
            cnt1 = cnt1 + 1
            dict122[str(name_)] = rat__.replace("0", "--")
      except:
        print(".")

      sorted_dict = sorted(dict122.items(), key=lambda x: x[1])
      sorted_dict.reverse()
      #print(sorted_dict)

      for i in range(cnt1):
        rating = sorted_dict[i][1]
        if rating != "0":
          if "a10" in rating:
            out = out + "\n" + str(
              sorted_dict[i][0]) + " **" + str(rating).replace("a10",
                                                               "10") + "**"
          else:
            out = out + "\n" + str(
              sorted_dict[i][0]) + " **" + str(rating) + "**"
        else:
          out = out + "\n" + str(sorted_dict[i][0]) + str(rating).replace(
            "0", "-- ")

      if cnt != 0:
        foot = str(round(
          sum / cnt,
          2)) + " from " + str(cnt) + " members, " + str(cnt1) + " watched"
      else:
        foot = "looks like no one rated this film"

      source = requests.get(str(o).replace("ratings", ""))
      source.raise_for_status

      soup = BeautifulSoup(source.text, 'html.parser')

      ##print(soup)

      f = soup.find_all('meta')
      for i in f:
        if "og:title" in str(i):
          moviename = str(i).replace('<meta content="', "")
          moviename = moviename.replace('" property="og:title"/>', "")

      #print(moviename)

      import json

      url = str(o).replace("ratings", "")
      #print("str(o) = ", str(o))

      r = requests.get(url)
      soup = BeautifulSoup(r.text)

      script_w_data = soup.select_one('script[type="application/ld+json"]')
      json_obj = json.loads(
        script_w_data.text.split(' */')[1].split('/* ]]>')[0])
      linnk = (json_obj['image'])

      out = out

      gemini_movie = moviename

      embed = discord.Embed(colour=discord.Colour.dark_teal(),
                            description=str(out),
                            title=str(moviename),
                            url=str(o))

      embed.set_footer(text=foot)
      embed.set_author(name="who knows")
      embed.set_thumbnail(url=linnk)
      await msg.reply(embed=embed)

      for i in list1:
        nlist.append(i)
      list1 = [0]

    except Exception as e:

      #print(e)
      embed = discord.Embed(
        colour=discord.Colour.dark_teal(),
        description=
        "couldn't find the movie you're looking for, try searching again with the year of release",
        title="WOOPS!",
        #url= lblink
      )
      await msg.reply(embed=embed)

  if msg.content.startswith('!hlp') and msg.guild.id == 562260964263591965:
    embed = discord.Embed(
      colour=discord.Colour.dark_grey(),
      title="📚 MovieBot Commands 🎬",
      description="Here are some helpful commands to interact with me:",
      url=
      "https://letterboxd.com/"  # Replace with your bot's website or information link
    )

    embed.add_field(name="",
                    value="`!wk movie name`\nSee who all knows a movie.",
                    inline=False)

    embed.add_field(
      name="",
      value="`!wl LB username`\nGet movies from a user's watchlist.",
      inline=False)

    embed.add_field(
      name="",
      value=
      "`!wl LB username genre1,genre2...`\nGet movies from a user's watchlist filtered by genre(s).",
      inline=False)

    embed.add_field(
      name="",
      value=
      "`!pop`\nGet Popular Movies right now",
      inline=False)

    embed.set_footer(text="")

    await msg.channel.send(embed=embed)


my_secret = os.environ['token']

keep_alive()
client.run(my_secret)
