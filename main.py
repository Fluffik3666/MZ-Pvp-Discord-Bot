import discord
from discord.ext import commands
import asyncio
from discord.ext import tasks
import re


intents = discord.Intents.all()
intents.typing = False
intents.presences = False


allowed_users = ['Fluffik#0001', 'Mz#4151']
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, I am {bot.user.mention}!')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1107727864272531600)
    if channel is not None:
        await channel.send(f'Welcome, {member.mention}! Enjoy your stay.')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1107727883587309679)
    if channel is not None:
        await channel.send(f'Goodbye, {member.display_name}! We will miss you.')

@bot.command()
async def poll(ctx, *, args):
    options = re.findall(r'"(.*?)"', args)
    for option in options:
        args = args.replace(f'"{option}"', '').strip()
    question = args

    if len(options) <= 1:
        await ctx.send("You need to provide at least 2 options for the poll.")
        return

    poll_message = f"**{question}**\n\n"
    for i, option in enumerate(options):
        emoji = chr(0x1F1E6 + i)
        poll_message += f"{emoji} : {option}\n"
    
    poll_message += "\nVote using the reactions below."
    poll = await ctx.send(poll_message)
    
    for i in range(len(options)):
        emoji = chr(0x1F1E6 + i)
        await poll.add_reaction(emoji)

@bot.command()
async def ban(ctx, member: discord.Member):
    if str(ctx.author) in allowed_users:
        await member.send("You have been banned.")
        await member.ban(reason="Banned by moderator")
        await ctx.send(f"{member.display_name} has been banned.")
    else:
        await ctx.send("You are not authorised to use this command.")

def initiate_bot():
  bot.run(input('Enter token: '))

initiate_bot()
