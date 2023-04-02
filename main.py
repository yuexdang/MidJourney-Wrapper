import discord
from discord.ext import commands

import Globals
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="/",intents=intents)


class MyHelpCommand(commands.DefaultHelpCommand):
    async def command_not_found(self, string):
        return f"没有找到名为'{string}'的命令。"

    async def command_has_no_subcommands(self, command):
        return f"{command}没有子命令。"



@bot.command(name='example', description='这是一个示例命令。')
async def example(ctx):
    await ctx.send('这是一个示例命令。')



bot.help_command = MyHelpCommand()

bot.run(Globals.DAVINCI_TOKEN)
