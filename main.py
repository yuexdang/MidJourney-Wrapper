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
    if message.content == "" or message.author.username == "MidRelay" or message.author.username == "Midjourney Bot" : return


    if "丁真" in message.content:
        try:
            Globals.targetID = str(message.message_reference.message_id)
	    #Get the hash from the url
            Globals.targetHash = str((message.referenced_message.attachments[0].url.split("_")[-1]).split(".")[0])
            print("User:{},Content:{},MessageID:{}".format(message.author.username, message.content, message.message_reference.message_id))
        except:
            await message.reply("再回复一次，丁真忙着回笼没看清")
            await message.delete()
            return
        if str(message.referenced_message.author.id) != Globals.MID_JOURNEY_ID:
            await message.reply("只能对Mid Journey说丁真")
            return
        await message.reply("丁真明白了")
        await message.delete()



# 测试用的狗屎代码
@bot.command(
    name = "fuck",
    description = "测试用的捏",
    options=[
        interactions.Option(
            name="propmt",
            description="随便输入一个内容",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)
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
        await ctx.send("丁真也不知道哦，再发一次去问问丽丽...")
    else:
        print("作画：{}".format(prompt))
        await ctx.send(
            "丁真正在画")

	
# 进行内容变体
@bot.command(
    name = "c",
    description = "发送图片细分命令( U0 - U4 | V0 - V4 )",
    options=[
        interactions.Option(
            name="number",
            description="选择需要细分图片",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="ChangeSign",
            description="选择细分类型",
            type=interactions.OptionType.STRING,
            choices=["U","V"],
            required=True,
        ),
        interactions.Option(
            name="reset_target",
            description="目标重置信号，默认命令执行后删除丁真目前定位的信息",
            type=interactions.OptionType.BOOLEAN,
            required=False,
        ),
    ],
)
@bot.command(
    name = "c",
    description = "发送图片细分命令( U0 - U4 | V0 - V4 )",
    options=[
        interactions.Option(
            name="number",
            description="选择需要细分图片",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="change_sign",
            description="选择细分类型",
            type=interactions.OptionType.STRING,
            choices=["U","V"],
            required=True,
        ),
        interactions.Option(
            name="reset_target",
            description="目标重置信号，默认命令执行后删除丁真目前定位的信息",
            type=interactions.OptionType.BOOLEAN,
            required=False,
        ),
    ],
)
async def mj_variation(ctx, number: int, change_sign: str, reset_target : bool = True):
    if (number <= 0 or number > 4):
        await ctx.send("丁真只能数到四")
        return

    if Globals.targetID == "":
        await ctx.send('你还没有给丁真说用哪个图')
        return

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id
    
    if change_sign.upper() == "U":
        response = Upscale(number, Globals.targetID, Globals.targetHash)
    elif change_sign.upper() == "V":
        response = Variation(number, Globals.targetID, Globals.targetHash)
    else:
        await ctx.send("丁真无法理解你打算怎么处理这个图")
        return

    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.send("再回复一次，丁真忙着回笼没看清")
        return

    await ctx.send("丁真正在画")


bot.start()
