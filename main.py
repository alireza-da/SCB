import functools
import json
import os
import typing

import discord
import requests
from bs4 import BeautifulSoup

import credentials
import logging

from precommands import run_pre_commands
from setup_db import setup_tables, get_user, update_user, get_user_occurance, get_admin, create_connection
from discord.ext import commands
from respond_randomizer import evil_randomizer, happy_zarif_randomizer
from keep_alive import keep_alive
from youtube import YTDLSource
from music import Music

logger = logging.getLogger(__name__)
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)
# bot = commands.Bot(command_prefix='$',intents=intents)
FFMPEG_OPTIONS = {}
guild = None
g_filename = ""


# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

async def non_blocking_data_insertion(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args, **kwargs)
    return await client.loop.run_in_executor(None, func)


def get_all_members():
    res_mhkn = client.get_guild(869221659733807125).members
    res_leg = client.get_guild(706038344450310215).members
    return res_mhkn + res_leg


@client.event
async def on_ready():
    print(f"Logged In as {client.user}")
    # delete_tables()
    # run_pre_commands()
    # setup_tables(get_all_members())
    await non_blocking_data_insertion(setup_tables, get_all_members())
    client.add_cog(Music(client))


@client.event
async def on_message(message):
    ctx = await client.get_context(message)
    if message.author == client.user:
        return
    user = message.author
    user = get_user(user.id)
    if user:
        if message.content.startswith('salavat') or message.content.startswith('صلوات'):
            await message.channel.send(
                f" اللّهم صلّ علی مُحمّد و آلِ محمّد و عجّل فرجهم {user.username}, +15 social credit")
            with open("assets/plus15sc.png", "rb") as SC15:
                plus_15_pic = discord.File(SC15)
                await message.channel.send(file=plus_15_pic)
            # print(f"[INFO]: Current Social Credit: {user.social_credit}")
            # print(f"[INFO]: User Occurance: {get_user_occurance(user.id)}")
            user.increase_social_credit(15)
            await message.channel.send(f"Social Credit Balance {user.social_credit}")
            update_user(user)

        if "feshar" in message.content.lower() or "فشار" in message.content:
            await message.channel.send(f"{user.username}, Feshar estefade kardi,-30 social credit")
            with open(f"assets/{evil_randomizer()}", "rb") as f:
                minus_30_pic = discord.File(f)
                await message.channel.send(file=minus_30_pic)
            user.decrease_social_credit(30)
            await message.channel.send(f"Social Credit Balance {user.social_credit}")
            update_user(user)

        if "kir" in message.content.lower() or "کیر" in message.content:
            await message.channel.send(f"{user.username}, mohtavaye na monaseb, -300 social credit")
            with open(f"assets/{evil_randomizer()}", "rb") as f:
                minus_30_pic = discord.File(f)
                await message.channel.send(file=minus_30_pic)
            user.decrease_social_credit(300)
            await message.channel.send(f"Social Credit Balance {user.social_credit}")
            update_user(user)

        if "marg bar amrica" in message.content.lower() or "مرگ بر آمریکا" in message.content:
            await message.channel.send(f"{user.username}, kare basiji anjam dadi +15 Social credit")
            user.increase_social_credit(15)
            with open(f"assets/{happy_zarif_randomizer()}", "rb") as SC15:
                plus_15_pic = discord.File(SC15)
                await message.channel.send(file=plus_15_pic)
            await message.channel.send(f"Social Credit Balance {user.social_credit}")
            update_user(user)

        # if ("salam" in message.content.lower() or "سلام" in message.content) or ("hi" in message.content.lower() or
        #                                                                          "hello" in message.content.lower()):
        #     await message.channel.send(f"{user.username}, salam bar shoma shahrvand aziz, +15 Social credit")
        #     user.increase_social_credit(15)
        #     with open(f"assets/{happy_zarif_randomizer()}", "rb") as SC15:
        #         plus_15_pic = discord.File(SC15)
        #         await message.channel.send(file=plus_15_pic)
        #     await message.channel.send(f"Social Credit Balance {user.social_credit}")
        #     update_user(user)

        if "dota" in message.content.lower() or "dota2" in message.content.lower() or "dota 2" in message.content.lower() or "دوتا" in message.content or "دوتا2" in message.content:
            await message.channel.send(
                f"{user.username} parsi ra pas bedarim va az kalame defa az bastan 2 estefade konim, -30 social credit")
            with open(f"assets/{evil_randomizer()}", "rb") as f:
                minus_30_pic = discord.File(f)
                await message.channel.send(file=minus_30_pic)
            user.decrease_social_credit(30)
            await message.channel.send(f"Social Credit Balance {user.social_credit}")
            update_user(user)

        if message.content.startswith("$decrease"):
            try:
                admin = get_admin(user)
                if admin:
                    target = message.mentions[0]
                    amount = message.content.split(' ')[-1]
                    user = get_user(target.id)
                    if user:
                        embedVar = discord.Embed(title="Social Credit Transaction", description=f"{target.name}",
                                                 color=0x00ff00)
                        embedVar.add_field(name="Amount", value=f"-{amount}", inline=False)
                        admin.reduce(user, int(amount))
                        update_user(user)
                        embedVar.add_field(name="Social Credit Balance", value=f"{user.social_credit}", inline=False)
                        await message.channel.send(embed=embedVar)
                else:
                    await message.channel.send("You are not admin")
            except Exception as e:
                print(f"[Error]: {e}")

        if message.content.startswith("$p "):
            await join(message)

        if message.content.startswith("$dc"):
            await disconnect(message)

        if message.content.startswith("$play_yt "):
            await play_yt(ctx, message.content.split(' ')[1])

        else:
            await client.process_commands(message)


async def disconnect(message):
    channel = message.author.voice.channel
    if channel:
        try:
            print(f"[INFO]: Disconnecting from {channel.name}")
            vc = channel.guild.voice_client
            await vc.disconnect()
        except Exception as e:
            print(f"[Error]: {e}")


@client.command(
    name="increase"
)
async def increase_sc(ctx):
    message = ctx.message
    user = get_user(message.author.id)
    admin = get_admin(user)
    if admin:
        target = message.mentions[0]
        amount = message.content.split(' ')[-1]
        user = get_user(target.id)
        if user:
            embedVar = discord.Embed(title="Social Credit Transaction", description=f"{target.name}", color=0x00ff00)
            embedVar.add_field(name="Amount", value=f"+{amount}", inline=False)
            admin.increase(user, int(amount))
            update_user(user)
            embedVar.add_field(name="Social Credit Balance", value=f"{user.social_credit}", inline=False)
            await message.channel.send(embed=embedVar)
    else:
        await message.channel.send("You are not admin")


@client.event
async def join(message):
    channel = message.author.voice.channel
    try:
        await channel.connect()
    except Exception as e:
        print(f"[Error]: {e}")
    if "bing" in message.content.split(' ') and "chilling" in message.content.split(' '):
        return await play_binchilin(message)

    elif "zarif" in message.content.split(' '):
        return await p_zarif(message)
    else:
        return await play_yt(await client.get_context(message), message.content.split(' ')[1])


async def play_binchilin(message):
    user = message.author
    voice_channel = user.voice.channel
    if voice_channel is not None:
        vc = voice_channel.guild.voice_client
        try:
            vc = await voice_channel.connect()
        except Exception as e:
            print(f"[Error]: {e}")
        source = discord.FFmpegPCMAudio("assets/john_cena_eats_bing_chilling_in_1080p_cc_2520698433256124212.m4a",
                                        **FFMPEG_OPTIONS)
        vc.play(source)
    else:
        await client.say('User is not in a channel.')


@client.command(name="p_zarif")
async def p_zarif(message):
    user = message.author
    voice_channel = user.voice.channel
    if voice_channel is not None:
        vc = voice_channel.guild.voice_client
        try:
            vc = await voice_channel.connect()
        except Exception as e:
            print(f"Cannot connect to {voice_channel}")
            logging.error(f"{e}")
        source = discord.FFmpegPCMAudio("assets/zarif talking chinies.m4a", **FFMPEG_OPTIONS)
        vc.play(source)
    else:
        await message.channel.send('User is not in a channel.')


@client.command(name="sc")
async def sc(ctx):
    user = ctx.message.author
    user = get_user(user.id)
    if user:
        await ctx.send(f"Your current social credit balance is {user.social_credit}")


@client.command(name='play_yt', help='Stream an YT content')
async def play_yt(ctx, url):
    try:
        user = ctx.message.author
        voice_channel = user.voice.channel
        if voice_channel is not None:
            vc = voice_channel.guild.voice_client
            try:
                vc = await voice_channel.connect()
            except Exception as e:
                print(f"Cannot connect to {voice_channel}")
                print(f"[Error]: {e}")
            try:
                g_filename = await YTDLSource.from_url(url, loop=client.loop)
                vc.play(discord.FFmpegPCMAudio(source=g_filename))
                await ctx.send('**Now playing:** {}'.format(g_filename))
            except Exception as e:
                logging.error(f"{e}")

    except Exception as e:
        print(f"[Error]: {e}")


@client.command(name="lyrics", help="Finding lyrics of song")
async def lyrics(ctx, filename):
    url = "https://genius.p.rapidapi.com/search"
    t_f = g_filename
    if filename:
        t_f = filename
    querystring = {"q": t_f}

    headers = {
        'x-rapidapi-host': "genius.p.rapidapi.com",
        'x-rapidapi-key': os.environ["rapidapi_key"]
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_res = json.loads(response.text)
    url = json_res["response"]["hits"][0]["result"]["url"]
    response = requests.request("GET", url)
    html = BeautifulSoup(response.text, 'html.parser')
    # print(html)
    lyrics1 = html.find("div", id="lyrics-root")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    # print(lyrics1)
    lyrics = ""
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 is None:
        lyrics = None

    # formatting the lyrics
    lyrics = lyrics.replace(", ", "\n")
    lyrics = lyrics.replace("[", "\n[")
    lyrics = lyrics.replace("]", "]\n")
    # print(lyrics)
    embedVar = discord.Embed(title="Lyrics", description=f"{filename}",
                             color=0x00ff00)
    embedVar.add_field(name="", value=f"-{lyrics}", inline=False)
    ctx.channe.send(embed=embedVar)


keep_alive()
client.run(credentials.bot_token)
