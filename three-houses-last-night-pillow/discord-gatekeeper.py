#https://discordapp.com/api/oauth2/authorize?client_id=607557575428407305&scope=bot&permissions=100352

import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import requests, textwrap
import os.path
from os import path

from dotenv import load_dotenv
load_dotenv()

print(os.getenv('CLIENT_TOKEN'))

TOKEN = os.getenv('CLIENT_TOKEN')
URL = "https://three-houses-last-night.herokuapp.com/quote/"

FONT = ImageFont.truetype('Rasa-Regular.ttf', size=39)
COLOUR = 'rgb(80, 76, 67)'
(x, y) = (350, 835)

bot = commands.Bot(command_prefix='!', description='Finding out what Gatekeeper-kun was up to last night.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def gatekeeper(ctx):
    REQUEST = requests.get(url=URL)
    data = REQUEST.json()
    image_name = 'SPOILER_guardkeeper-' + data['quote_link'][14:-5] + ".png"

    if (path.exists(image_name)):
        file = discord.File(image_name, filename=image_name)
        print("User: " + str(ctx.message.author.name) + " in " + str(ctx.guild) + " - Link: " + str(data['quote_link']))
        await ctx.send("<@!" + str(ctx.message.author.id) + "> http://www.textsfromlastnight.com" + data['quote_link'],
                       file=file)
    else:
        lines_separated = textwrap.wrap(data['quote_text'], width=60)
        lines_separated[0].capitalize()

        IMAGE = Image.open('gatekeeper-clean.png')
        draw = ImageDraw.Draw(IMAGE)
        for i in range(len(lines_separated)):
            draw.text((x, y + (i * 40)), lines_separated[i], fill=COLOUR, font=FONT)

        IMAGE.save(image_name)

        file = discord.File(image_name, filename=image_name)
        print("User: " + str(ctx.message.author.name) + " in " + str(ctx.guild) + " - Link: " + str(data['quote_link']))
        await ctx.send("<@!" + str(ctx.message.author.id) + "> http://www.textsfromlastnight.com" + data['quote_link'], file=file)


bot.run(TOKEN)