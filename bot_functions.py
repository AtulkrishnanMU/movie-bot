import discord
import requests
from bs4 import BeautifulSoup
import random
import re
import json

RT_POPULAR_MOVIES_URL = 'https://editorial.rottentomatoes.com/guide/popular-movies/'
RANDOM_GIF_BASE_URL = 'https://tenor.com/search/'
INSULT_API_URL = 'https://evilinsult.com/generate_insult.php'

def searcho(o):
  s = ""
  try:
    l2 = str(o)
    st1 = l2.find('film/')
    name = l2[st1 + 5:]

    s = "https://letterboxd.com/travis_pickle12/friends/film/" + str(
      name).replace("releases/", "") + "/"
    s = s.replace("ratings", "")

    page = requests.get(s)
    code = page.status_code
    if code == 404:
      s = "https://letterboxd.com/travis_pickle12/friends/film/" + str(
        name) + "/"
      page = requests.get(s)
      code = page.status_code
  except:
    print("error")
  return s

def searchf(movienm):
  source = requests.get('https://www.google.com/search?q=' + movienm +
                        '+movie+letterboxd')
  source.raise_for_status
  soup = BeautifulSoup(source.text, 'html.parser')

  a = soup.find_all('a')

  for i in a:
    if 'https://letterboxd.com/' in str(i) and '/film' in str(i):
      l = str(i)
      st = l.find('https://letterboxd.com/')
      end = l.find('/&amp;')

      s = (l[st:end])
      if st != -1 and end != -1:
        break

  s = s.replace('ratings', '')

  strt = s.find('/film')
  s = 'https://letterboxd.com' + s[strt:]

  return s

async def handle_watchlist_command(msg):
    if msg.content.startswith('!wl'):

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
        strt = str(f).find("https://a.ltrbxd.com/resized/avatar/upload")
        end = str(f).find('.jpg')
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
            pgnum = ""
            pgg = str(i)[strt:end]
            for i in pgg:
                if i.isdigit():
                    pgnum = pgnum + i
        try:
            pgnumm = random.randint(0, int(pgnum))
        except:
            pgnumm = 0

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
                list123.append("https://letterboxd.com/" +
                            fi[strt:end].replace('data-target-link="/', ''))

        list123.pop(0)

        urrl = str(random.choice(list123))

        r = requests.get(urrl)
        soup = BeautifulSoup(r.text)

        f = soup.find_all('meta')
        plot = str(f[3]).replace('<meta content="', "")
        plot = plot.replace('" name="description"/>', "")

        script_w_data = soup.select_one('script[type="application/ld+json"]')
        json_obj = json.loads(
            script_w_data.text.split(' */')[1].split('/* ]]>')[0])
        linnk = (json_obj['image'])

        l2 = urrl

        source = requests.get(l2)
        source.raise_for_status

        soup = BeautifulSoup(source.text, 'html.parser')

        f = soup.find_all('meta')
        for i in f:
            if "og:title" in str(i):
                moviename = str(i).replace('<meta content="', "")
                moviename = moviename.replace('" property="og:title"/>', "")

        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            description=str(plot[:120].replace("&quot;", '"')).replace(
                "<meta content='", "") + "...",
            title=moviename,
            url=urrl)
        embed.set_author(name="from " + str(input) + "'s watchlist:",
                        url="https://letterboxd.com/" + str(input) + "/",
                        icon_url=avatar)
        embed.set_thumbnail(url=linnk)
        await msg.reply(embed=embed)

async def handle_watch_command(msg):
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

                soup = BeautifulSoup(source.text, 'html.parser')

                tr = soup.find_all('tr')

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

            embed = discord.Embed(
                colour=discord.Colour.dark_teal(),
                description=
                "couldn't find the movie you're looking for, try searching again with the year of release",
                title="WOOPS!",
            )
            await msg.reply(embed=embed)

# Get insult from API
def get_insult(language='en', response_type='json'):
    params = {'lang': language, 'type': response_type}
    try:
        response = requests.get(INSULT_API_URL, params=params)
        response.raise_for_status()
        data = response.json() if response_type == 'json' else response.text
        return data.get('insult', 'No insult found.') if response_type == 'json' else data
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Fetch a random GIF based on keyword
async def get_random_gif(keyword):
    url = f'{RANDOM_GIF_BASE_URL}{keyword}-gifs'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    gif_divs = soup.find_all("div", class_="Gif")
    gifs = [div.find("img")["src"] for div in gif_divs if div.find("img")]
    return random.choice(gifs) if gifs else None

# Search Letterboxd movie by name
def search_letterboxd(movienm):
    source = requests.get('https://www.google.com/search?q=' + movienm + '+movie+letterboxd')
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')
    a_tags = soup.find_all('a')
    for a in a_tags:
        if 'https://letterboxd.com/' in str(a) and '/film' in str(a):
            url = re.search(r'(https://letterboxd\.com/.+?/)', str(a))
            if url:
                return url.group(1).replace('ratings', '')
    return None

# Create embedded message for movies
def create_embed(movie_data, page_number, user, avatar):
    color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed = discord.Embed(title="Month Diary", color=color)
    embed.set_author(name=user, icon_url=avatar)
    for idx, movie in enumerate(movie_data, start=(page_number - 1) * 10 + 1):
        title, link, date, rating = movie.split('](')[0], movie.split('](')[1].split(')')[0], movie.split(') ')[1].split(', ')[0], movie.split(', ')[-1]
        rating = '' if rating == '0/10' else rating
        embed.add_field(name=f"{idx}. {title}", value=f"[{date}, {rating}]({link})", inline=False)
    return embed

def fetch_popular_movies():
    response = requests.get(RT_POPULAR_MOVIES_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        movie_items = soup.find_all('div', class_='col-sm-18 col-full-xs countdown-item-content')
        return [item.find('div', class_='article_movie_title').find('a').text + f" ({item.find('span', class_='subtle start-year').text.strip('()')})" for item in movie_items[:10]]
    return []

async def help(msg):
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