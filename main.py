import discord
from discord.ext import commands

import Globals
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="/",
    intents=intents
)




@bot.command(name='example', description='这是一个示例命令。')
async def example(ctx):
    await ctx.send('这是一个示例命令。')



bot.help_command = commands.DefaultHelpCommand(no_category='Commands')

bot.run(Globals.DAVINCI_TOKEN)
