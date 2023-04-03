from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
import Globals

import interactions


bot = interactions.Client(
    token=Globals.DAVINCI_TOKEN,
    default_scope=Globals.SERVER_ID,
    intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT,
    )

# 登录状态确认
@bot.event
async def on_ready():
    print(f"Logged in Alright")


# 检测at了哪个图图
@bot.event
async def on_message_create(message):
    print(message)
    if message.content == "" or message.author.username == "MidRelay" or message.author.username == "Midjourney Bot" : return
#     print("name:{},content:{}".format(message.author.username,message.content))
    if "丁真" in message.content:
        try:
            Globals.targetID = str(message.message_reference.message_id)
	    #Get the hash from the url
            Globals.targetHash = str((message.referenced_message.attachments[0].url.split("_")[-1]).split(".")[0])
        except:
            await message.send(
                "再回复一次，丁真忙着回笼没看清"
            )
            await message.delete()
            return
        if str(message.referenced_message.author.id) != Globals.MID_JOURNEY_ID:
            await message.send(
                "只能对Mid Journey说丁真")
            await message.delete()
            return
        await message.send("丁真明白了")
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
    description = "问问远处的丁真吧家人们",
    options=[
        interactions.Option(
            name="prompt",
            description="图片参数",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def mj_imagine(ctx, prompt: str):

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = PassPromptToSelfBot(prompt)
    
    if response.status_code >= 400:
        print(response.txt)
        print(response.status_code)
        await ctx.send("丁真也不知道哦，不如再发一次去问问丽丽...")
    else:
        print("作画：{}".format(prompt))
        await ctx.send(
            "丁真正在画")

	
# 调用variation
@bot.command(
    name = "yydz",
    description = "狠狠的细分",
    options=[
        interactions.Option(
            name="number",
            description="选取数字",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="reset_target",
            description="我不好说",
            type=interactions.OptionType.BOOLEAN,
            required=False,
        ),
    ],
)

async def mj_variation(ctx, prompt: int, reset_target : bool = True):
    if (prompt <= 0 or prompt > 4):
        await ctx.send("丁真只能数到四")
        return

    if Globals.targetID == "":
        await ctx.send('你还没有给丁真说用哪个图')
        return


    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id
        
    response = Variation(prompt, Globals.targetID, Globals.targetHash)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.send("再回复一次，丁真忙着回笼没看清")
        return

    await ctx.send("丁真正在画")




bot.start()
