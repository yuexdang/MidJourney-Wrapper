import interactions

bot = interactions.Client(token="your_secret_bot_token")

@bot.command(
    name="my_first_command",
    description="This is the first command I made!",
    scope=the_id_of_your_guild,
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

bot.start()
