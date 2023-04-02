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


# 检测at了哪个图图
@bot.event
async def on_message(message):
    print(message)
    if message.content == "": return
    if "!15dj" in message.content and message.content[0] == '!':
        try:
            Globals.targetID = str(message.reference.message_id)
	    #Get the hash from the url
            Globals.targetHash = str((message.reference.resolved.attachments[0].url.split("_")[-1]).split(".")[0])
        except:
            await message.channel.send(
                "再回复一次，丁真忙着回笼没看清"
            )
            await message.delete()
            return
        if str(message.reference.resolved.author.id) != Globals.MID_JOURNEY_ID:
            await message.channel.send(
                "丁师傅，回复不是这么用的")
            await message.delete()
            return
        await message.channel.send("丁真知道你想的图了")
        await message.delete()



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
        await ctx.send("网卡了哦，丁真也不知道哦...")
    else:
        await ctx.send(
            "丁真正在画，再催就测你🐎....")





bot.start()
