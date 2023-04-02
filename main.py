from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
import Globals

import interactions


bot = interactions.Client(
    token=Globals.DAVINCI_TOKEN,
    default_scope=Globals.SERVER_ID,
    )

# 登录状态确认
@bot.event
async def on_ready():
    print(f"Logged in Alright")



# 测试用的狗屎代码
@bot.command(
    name = "fuck",
    description = "重构一坨狗屎放在这里",
)
@interactions.option()
async def my_first_command(ctx: interactions.CommandContext, propmt: str = "SHIT CODE"):
    await ctx.send("Fucking Good Guys about This {}".format(propmt))



# 调用imagine
@bot.command(
    name = "dj",
    description = "问问远处的机器人吧家人们",
)
@interactions.option()
async def mj_imagine(ctx, prompt: str):

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = PassPromptToSelfBot(prompt)
    
    if response.status_code >= 400:
        print(response.txt)
        print(response.status_code)
        await ctx.respond("Request has failed; please try later")
    else:
        await ctx.respond(
            "Your image is being prepared, please wait a moment...")


bot.start()
