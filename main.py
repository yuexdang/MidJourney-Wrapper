import discord
from discord.ext import commands

import Globals
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/",intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command(name="hello",description="绷不住了")
async def hello(ctx, prompt):
    await ctx.send('Hello!'+prompt)


@bot.command(description="This command is a wrapper of MidJourneyAI")
async def mj_imagine(ctx, prompt):

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = PassPromptToSelfBot(prompt)
    
    if response.status_code >= 400:
        print(response.txt)
        print(response.status_code)
        await ctx.send("Request has failed; please try later")
    else:
        await ctx.send(
            "Your image is being prepared, please wait a moment...")


@bot.command(description="Upscale one of images generated by MidJourney")
async def mj_upscale(ctx, index, reset_target=True):
    if (index <= 0 or index > 4):
        await ctx.send("Invalid argument, pick from 1 to 4")
        return

    if Globals.targetID == "":
        await ctx.send(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    if (Globals.USE_MESSAGED_CHANNEL):
          Globals.CHANNEL_ID = ctx.channel.id
    response = Upscale(index, Globals.targetID, Globals.targetHash)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.send("Request has failed; please try later")
        return

    await ctx.send("Your image is being prepared, please wait a moment...")

@bot.command(description="Upscale to max targetted image (should be already upscaled using mj_upscale)")
async def mj_upscale_to_max(ctx):
    if Globals.targetID == "":
        await ctx.send(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = MaxUpscale(Globals.targetID, Globals.targetHash)
    Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.send("Request has failed; please try later")
        return

    await ctx.send("Your image is being prepared, please wait a moment...")

@bot.command(description = "Make variation given index after target has been set")
async def mj_variation(ctx, index, reset_target=True):
    if (index <= 0 or index > 4):
        await ctx.send("Invalid argument, pick from 1 to 4")
        return

    if Globals.targetID == "":
        await ctx.send(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return


    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id
        
    response = Variation(index, Globals.targetID, Globals.targetHash)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.send("Request has failed; please try later")
        return

    await ctx.send("Your image is being prepared, please wait a moment...")






bot.run(Globals.DAVINCI_TOKEN)
