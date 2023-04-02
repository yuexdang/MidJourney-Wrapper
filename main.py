from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
import Globals

import interactions


bot = interactions.Client(token=Globals.DAVINCI_TOKEN)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(
    name = "Fuck",
    description = "Holy shit It Works",
    scope = Globals.SERVER_ID,
)
async def my_first_command(ctx: interactions.CommandContext, propmt: str = "SHIT CODE"):
    await ctx.send("Fucking Good Guys about This {}".format(propmt))

bot.start()
