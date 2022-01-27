from replit import db
import discord
import credentials
from setup_db import setup_tables, add_users_to_db, get_user, set_user, get_user_occurance
from respond_randomizer import evil_randomizer


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def get_all_members():
    res = client.get_guild(869221659733807125).members
    for user in res:
        print(user.name)
    return res


@client.event
async def on_ready():
    print(f"Logged In as {client.user}")
    # del db["users"]
    setup_tables(get_all_members())


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    user = message.author
    user = get_user(message.author.id)
    if user:
      if message.content.startswith('$salavat') or message.content.startswith('$صلوات'):
            await message.channel.send(f" اللّهم صلّ علی مُحمّد و آلِ محمّد و عجّل فرجهم {user.username}")
            with open("assets/plus15sc.png", "rb") as f:
                plus_15_pic = discord.File(f)
                await message.channel.send(file=plus_15_pic)
            print(f"[INFO]: Current Social Credit: {user.social_credit}")
            print(f"[INFO]: User Occurance: {get_user_occurance(user.id)}")
            user.increase_social_credit(15)
            await message.channel.send(f"Social Credit Balance {user.social_credit}")
            set_user(user)

      if "Feshar" in message.content or "feshar" in message.content or "فشار" in message.content:
        await message.channel.send(f"Feshar estefade kardi, {user.username}")
        with open(f"assets/{evil_randomizer()}", "rb") as f:
                minus_30_pic = discord.File(f)
                await message.channel.send(file=minus_30_pic)
        user.decrease_social_credit(30)
        await message.channel.send(f"Social Credit Balance {user.social_credit}")
        set_user(user)
        
client.run(credentials.bot_token)
