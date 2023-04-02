import interactions, os

bot = interactions.Client(token=os.environ.get('DAVINCI_TOKEN'))

@bot.command(
    name="my_first_command yeap",
    description="This is the first command I made!",
    scope=os.environ.get('CHANNEL_ID'),
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

bot.start()
