import interactions, os

bot = interactions.Client(token=os.environ.get('DAVINCI_TOKEN'))

@bot.command(
    name="my_first_command yeap",
    description="This is the first command I made!",
    scope=the_id_of_your_guild,
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

bot.start()
