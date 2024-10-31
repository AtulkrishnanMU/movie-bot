import random
import discord
from discord.ext import commands, tasks
from discord import app_commands
import google.generativeai as genai
from bot_functions import handle_watch_command, handle_watchlist_command, get_insult, get_random_gif, fetch_popular_movies, help

# Constants
GOOGLE_API_KEY = 'gemini_api'
PREFIX = "!!"

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, intents=intents)

# Configure GenAI with API key
genai.configure(api_key=GOOGLE_API_KEY)

# Event: on bot ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event: on message received
@client.event
async def on_message(msg):
    if client.user.mentioned_in(msg) or (msg.reference and msg.reference.resolved.author == client.user):
        try:
            content = msg.content.replace(f"<@{client.user.id}>", "").strip()
            model = genai.GenerativeModel('gemini-pro')
            
            response_text = (
                    model.generate_content(content).text 
                )
            
            await msg.reply(response_text)
        except:
            await msg.reply(await get_random_gif(content))
    
    if msg.content == "!pop":
        popular_movies = fetch_popular_movies()
        if popular_movies:
            embed = discord.Embed(title="Popular Movies Right Now", color=discord.Color.blue())
            embed.description = "\n".join(popular_movies)
            await msg.channel.send(embed=embed)
        else:
            await msg.channel.send("Failed to retrieve popular movies.")

    elif msg.content.startswith('!wl'):
        await handle_watchlist_command(msg)
    elif msg.content.startswith('!wk'):
        await handle_watch_command(msg)

    if msg.content.startswith('!hlp'):
        await help(msg)

my_secret = 'bot_token'
client.run(my_secret)
