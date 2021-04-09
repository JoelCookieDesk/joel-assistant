# Import all the necessary stuffs
import discord, os, pyjokes, pyshorteners, gtts, requests, random
from discord.ext import commands
from dotenv import load_dotenv

# Setting something...
bot = commands.Bot(command_prefix=".")
bot.remove_command("help")

# loading the env variables in .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

# When bot is ready this script will execute
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f"{bot.user} is connected to the following guild:\n{guild.name}(id: {guild.id})")

# When a user joins the discord server, it will execute this
async def on_member_join(member):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    # Sends a private message(DM) to the user that joined the server
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to {guild.name} server :star_struck:!")

# Handle the errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":woozy-face: You are missing permissions ;-;")
    elif isinstance(error, commands.NotOwner):
        await ctx.send(":rofl: Tf are you the owner lol ;-;")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send(":unamused: What I don't know any roles related or same to that ;-;")

# All the commands for our bot
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help...", description="Type .help <command> to get more information in that command")
    embed.add_field(name=":desktop: Owner commands", value="`eval [a] [operator] [b]`", inline=False)
    embed.add_field(name=":hammer: Moderation", value="`ban [mention user]`, `mute [mention user]`,\n`unban [mention member name and discriminator]`, `kick [mention user]`,\n`dm [mention user] [message]`, `clear`, `add_role`, `remove_role`", inline=False)
    embed.add_field(name=":tada: Fun", value="`coin_flip`, `random_number`,`dev_joke`, `mention [mention user] [text]`", inline=False)
    embed.add_field(name=":face_with_monocle: Facts", value="`dog_fact`, `cat_fact`, `panda_fact`", inline=False)
    embed.add_field(name=":earth_asia: Global", value="`info [mention user]`, `ping`, `users`", inline=False)
    embed.add_field(name=":gear: Settings", value="`version`", inline=False)
    embed.add_field(name=":tools: Utilities", value="`tts [text](text-to-speech)`, `shorten_url [website eg:bitly] [link]`, `url_clicks [link] (only if you shorten your url with bitly)`", inline=False)
    await ctx.send(embed=embed)

# Moderation commands
@bot.command(aliases=["k"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member=discord.Member, *, reason="No reason provided"):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    await member.send(f"You have been kick from {guild.name}.\nTo join again click this link - https://discord.gg/gKaD3Kmr")
    await member.kick(reason=reason)
    await ctx.send(f"(name: {member.name}, id: {member.id}), has been kicked from the server")

@bot.command(aliases=["b"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member=discord.Member, reason="No reason provided"):
    await ctx.send(f"(name: {member.name}, id: {member.id}), has been ban from the server")
    await member.ban(reason=reason)

@bot.command(aliases=["m"])
@commands.has_permissions(ban_members=True, kick_members=True)
async def mute(ctx, member=discord.Member):
    muted_role = ctx.guild.get_role(810772951501766687)
    await member.add_roles(muted_role)
    await ctx.send(f"{member.name}, has been muted from the server")

@bot.command(aliases=["ub"])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")
    for banned_entry in banned_users:
        user = banned_entry.user
        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f"{member_name}, has been unbanned from the server")
            return
    await ctx.send(f"{member}, was not found")

@bot.command(aliases=["c", "cls"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@bot.command(aliases=["msg", "send"])
async def dm(ctx, member:discord.Member, *, message):
    await member.send(f"{message}\nThis message was sent by (name: {ctx.author.name}, id: {ctx.author.id})")
    await ctx.send(f"Your message was send successfully to {member}")

# Owner commands
@bot.command(aliases=["eval", "calculate", "calc"])
@commands.is_owner()
async def evaluate(ctx, first_num:int, operator, second_num:int):
    if operator == "+":
        result = first_num + second_num
        await ctx.send(f"{ctx.author.mention}, {first_num} + {second_num} = {result}")
    if operator == "*":
        result = first_num * second_num
        await ctx.send(f"{ctx.author.mention}, {first_num} * {second_num} = {result}")
    if operator == "/":
        result = first_num / second_num
        await ctx.send(f"{ctx.author.mention}, {first_num} / {second_num} = {result}")
    if operator == "-":
        result = first_num - second_num
        await ctx.send(f"{ctx.author.mention}, {first_num} - {second_num} = {result}")

# Utilities command
@bot.command(aliases=["url_shortener"])
async def shorten_url(ctx, web, link):
    shortener = pyshorteners.Shortener()
    if web.lower() == "tinyurl":
        result = shortener.tinyurl.short(link)
        await ctx.send(f"{ctx.author.mention}, I have shorten this link - {link}, to this - {result}")
    elif web.lower() == "bitly":
        shortener = pyshorteners.Shortener(api_key="4e7a2522d61f9e3cb4399066ad1cd30d2826411d")
        result = shortener.bitly.short(link)
        await ctx.send(f"{ctx.author.mention}, I have shorten this link - {link}, to this - {result}")
    else:
        await ctx.send(f"{web} is not a url shortener website!")

@bot.command()
async def url_clicks(ctx, url):
    shortener = pyshorteners.Shortener(api_key="4e7a2522d61f9e3cb4399066ad1cd30d2826411d")
    try:
        total_clicks = shortener.bitly.total_clicks(url)
        await ctx.send(f"The total clicks for this url - {url}, is {total_clicks}")
    except:
        await ctx.send(f"{url}, is not a valid url, it only works if you shortened your links with bitly")

@bot.command(aliases=["text_to_speech"])
async def tts(ctx, *, text):
    def speech(say):
        tttts = gtts.gTTS(text=say, lang="en")
        tttts.save("tts/speech.mp3")
    text = str(text)
    speech(text)
    await ctx.send("Converted to text to speech here is the mp3 file: ")
    await ctx.send(file=discord.File("tts/speech.mp3"))

# Global commands
@bot.command(aliases=["latency"])
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong! Latency: {round(bot.latency * 100)}ms")

@bot.command(aliases=["server_users"])
async def users(ctx):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    await ctx.send(f"There are currently {guild.member_count} users right now, WooHoo :partying_face:")
    
# Facts commands
@bot.command()
async def dog_fact(ctx):
    url = requests.get("https://some-random-api.ml/facts/dog")
    if url.status_code == 200:
        data = url.json()
        await ctx.send(data["fact"])
    else:
        await ctx.send(f"The api returned {url.status_code} status.")

@bot.command()
async def cat_fact(ctx):
    url = requests.get("https://some-random-api.ml/facts/cat")
    if url.status_code == 200:
        data = url.json()
        await ctx.send(data["fact"])
    else:
        await ctx.send(f"The api returned {url.status_code} status.")

@bot.command()
async def panda_fact(ctx):
    url = requests.get("https://some-random-api.ml/facts/panda")
    if url.status_code == 200:
        data = url.json()
        await ctx.send(data["fact"])
    else:
        await ctx.send(f"The api returned {url.status_code} status.")

# Fun commands
@bot.command()
async def dev_joke(ctx):
    joke = pyjokes.get_joke()
    await ctx.send(f"{ctx.author.mention}, {joke}")

@bot.command()
async def mention(ctx, member:discord.Member, *, message):
    await ctx.message.delete()
    await ctx.send(f"{member.mention}, {message}")

@bot.command(aliases=["gen_num", "rand_num"])
async def random_number(ctx, first_num=1, second_num=11):
    first_num = int(first_num)
    second_num = int(second_num)
    await ctx.send(random.randrange(first_num, second_num))

@bot.command(aliases=["flip_coin"])
async def coin_flip(ctx, loop=1):
    loop = int(loop)
    for i in range(0, loop, 1):
        coin = ["Heads", "Tails"]
        toss = random.choice(coin)
        await ctx.send(f"It was... {toss}")

# Running the bot from the token variable
bot.run(TOKEN)