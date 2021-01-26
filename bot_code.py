# bot.py
import os
import logging 
import random
import discord
import requests
import io
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

#subreddit code 
import urllib.request, json 


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


#utility function for downloading image from this person blah blah blah 
def download(fileName):
    url = 'https://thispersondoesnotexist.com/image'
    return requests.get(url, headers={'User-Agent': 'My User Agent 1.0'}).content


bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        #if guild.name == GUILD:
            #break

    # print(
    #     f'{bot.user} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id})'
    # )

@bot.command(name='qt',help = 'this command gives 1 of 17 beautiful quotes from local array',inline = False)
async def send_quote(ctx):
    quotes = [
        'I think being in love with life is a key to eternal youth.',
        'You’re only here for a short visit. Don’t hurry, don’t worry. And be sure to smell the flowers along the way.',
        'A man who dares to waste one hour of time has not discovered the value of life.',
        'If life were predictable it would cease to be life, and be without flavor.',
        'All life is an experiment. The more experiments you make the better.',
        'All of life is peaks and valleys. Don’t let the peaks get too high and the valleys too low.',
        'Find ecstasy in life; the mere sense of living is joy enough.',
        'My mission in life is not merely to survive, but to thrive; and to do so with some passion, some compassion, some humor, and some style.',
        'However difficult life may seem, there is always something you can do and succeed at.',
        'Life is like riding a bicycle. To keep your balance, you must keep moving.',
        'The more you praise and celebrate your life, the more there is in life to celebrate.',
        'The most important thing is to enjoy your life—to be happy—it’s all that matters.',
        'I enjoy life when things are happening. I don’t care if it’s good things or bad things. That means you’re alive.',
        'Life is short, and it is up to you to make it sweet.',
        'Life doesn’t require that we be the best, only that we try our best.',
        'I always like to look on the optimistic side of life, but I am realistic enough to know that life is a complex matter.',
        'The truth is you don’t know what is going to happen tomorrow. Life is a crazy ride, and nothing is guaranteed.',
    ]

    response = random.choice(quotes) + ' Have a nice day '  + str(ctx.author.mention)
    await ctx.send(response)
    


@bot.command(name='create-channel',help = 'this commands helps to create new text channels', inline = False)
@commands.has_role('admin')
async def create_channel(ctx, channel_name='unity-trash'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await ctx.send(f'{channel_name} successfully created by {ctx.author.mention}')



@bot.command(name='get-fake-person',help = 'this command gets an image from thispersondoesntexist.com',inline = False)
async def generate_file(ctx):
    data = download('eg.png')
    await ctx.send(file=discord.File(io.BytesIO(data),'eg.png'))


@bot.command(name='gtis',help = 'this command gets an image from subreddit',inline = False)
async def get_subreddit(ctx,*,urlparttwo):
    
    #variables for subreddit
    suffix = ['.jpg','.png','.gif','.bmp']
    counter = 1
    urlpartone = "https://reddit.com/r/"
    urlpartthree = "/random.json"
    checkerurl = ".json"

    finalurl = urlpartone + urlparttwo + urlpartthree
    while True:
        response = requests.get(finalurl,headers = {'User-agent': 'test bot 0.1'})
        #parsedjson = json.loads(response.data.decode('utf-8'))
        parsedjson = response.json()
        img = parsedjson[0]['data']['children'][0]['data']['url']
        if img.endswith('.png') or img.endswith('.jpg') or img.endswith('.gif'):
            await ctx.send(img)
            return
        else: 
            counter += 1
        if counter == 11:
            await ctx.send('Failed to get image after 10 tries. If you\'re sure there are images, try again. Bad luck!')
            return
        await ctx.send('Incorrect syntax. use correct subreddit name')
        return 
    
@bot.command(name='gen_fake_per',help = 'this command gets an image from thispersondoesntexist.com using different method',inline = False)
async def send_image(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://thispersondoesnotexist.com/image') as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'cool_image.png'))


@bot.listen('on_message')
async def sends_reactions(message):
    if not 'Have a nice day' in message.content:
        logging.debug('the phrase in not detected in msg. ')
        return
    if message.author == bot.user :
        emoji = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.Try contacting Jerome and get admin role by paying him $200.')
    else:
        await ctx.send(f'something wrong happened.I have the error for you {error}')

bot.run(TOKEN)
