# bot.py
import os
import discord
from dotenv import load_dotenv
from PIL import Image
import keep_alive
from unidecode import unidecode

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
pingfisher = None

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    user = await client.fetch_user(313480641935179777)
    pfp = user.avatar_url_as(format='png', static_format = 'png', size = 512)
    with open('pfp.png','wb') as pfpimg:
        await pfp.save(pfpimg)
    with open('pfp.png','rb') as pfpimg:
        data = pfpimg.read()
        # await client.user.edit(avatar=data)
    client.get_emoji(760570803942588487)


def generate_image():
    # load the template and pfp from disk
    template = Image.open('template.png')
    pfp = Image.open('pfp.png')
    userpfp = Image.open('userpfp.png')

    # use PIL to overlay the pfp (at a slight angle, of course)
    # center at (958, 346)
    # rotated CCW by about 5-7 degrees
    # size is roughly 251x241 (can use 255 square)
    pfp = pfp.resize((257,257)).rotate(7)
    print(pfp.size)
    template.paste(pfp, (1092 - pfp.size[0], 464 - pfp.size[1]))

    # User pfp at (316, 61)
    userpfp = userpfp.resize((257,257))
    template.paste(userpfp, (316, 61))
    # save the image and return the filename
    template.save('meme.png', 'png')
    return 'meme.png'

@client.event
async def on_message(message):
    # Primary function
    if message.content.lower() == "snouty mark it down":
        snouty = await client.fetch_user(313480641935179777)
        pfp = snouty.avatar_url_as(format='png', static_format = 'png', size = 512)
        user = message.author
        user_pfp = user.avatar_url_as(format='png', static_format = 'png', size = 512)
        with open('pfp.png','wb') as pfpimg:
            await pfp.save(pfpimg)
        with open('userpfp.png','wb') as pfpimg:
            await user_pfp.save(pfpimg)
        generate_image()
        await message.channel.send(file=discord.File('meme.png'))
    # print(message.content)
    # This doesn't actually have anything to do with the bot, but it's a nice lightweight "aliveness" check so we can keep it
    if "@763965972360724482" in message.content or "@!763965972360724482" in message.content:
      # print("mentioned")
      print(pingfisher)
      await message.channel.send("<:pingfisher:760570803942588487>")
    msg = unidecode(message.content.lower())
    # I don't really get this one? It would be interesting if we could get another bot to respond to it with "you know"
    #if msg == "based":
    #  await message.channel.send("on what")
    # People (mainly mag) were abusing this as an oracle.
    # if "jermaJup1" in message.content and "jermaJup2" in message.content:
    #   await message.channel.send("no")
    # Added because of something snouty said
    if msg == "botty do you love your mother and namesake":
      emoji = client.get_emoji(538250797558005772)
      await message.channel.send(str(emoji))
    # Disabling this, too much potential for abuse.
    # Deathly will say more odd things to make people spam this.
    # if msg == "shut up deathly":
    #   await message.channel.send("https://cdn.discordapp.com/attachments/508525430224060417/789004191594971156/obama_deathly.mp4")
    # for cursed chat days
   # if msg == "what has this place become":
    #  await message.channel.send("https://cdn.discordapp.com/attachments/384231586205270027/791530703421702154/image0.png")
    #if msg == "bonk drone has found the horny":
    #  await message.channel.send("https://cdn.discordapp.com/attachments/384231586205270027/809617407240962128/ced.png")
    #if msg == "heard u were talkin shit":
    #  await message.channel.send("https://cdn.discordapp.com/attachments/384231586205270027/816535684596367400/505xbj.png")

@client.event
async def on_disconnect():
    pass


keep_alive.keep_alive()
client.run(TOKEN)
