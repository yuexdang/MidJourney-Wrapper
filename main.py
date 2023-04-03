from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
import Globals

import interactions

import time


bot = interactions.Client(
    token=Globals.DAVINCI_TOKEN,
    default_scope=Globals.SERVER_ID,
    intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT,
    )



# 登录状态确认
@bot.event
async def on_ready():
    print(f"丁真来咯")



# 检测at了哪个图图
@bot.event
async def on_message_create(message):
    if not Globals.HAS_RUN:
        print(f"丁真准备好了")
        Globals.HAS_RUN = True
        await message.reply(Globals.update_msg)
    print(Globals.targetID,Globals.userInfo)
    if message.content == "" or message.author.username == Globals.bot_name or message.author.username == "Midjourney Bot" : return

    try:
        if "丁真" in message.content and "@" in message.referenced_message.content:
            try:
                if Globals.targetID:
                    if time.time() - Globals.userInfo['lastTime'] <= Globals.waitTime:
                        await message.reply("目前丁真正在为{}进行一眼鉴定，请于{}s后进行重试".format(
                                                                                Globals.userInfo["userName"],
                                                                                int(time.time() - Globals.userInfo['lastTime'] ),
                                                                                ))
                        return
                Globals.targetID = str(message.message_reference.message_id)
            #Get the hash from the url
                Globals.targetHash = str((message.referenced_message.attachments[0].url.split("_")[-1]).split(".")[0])
                print("User:{},Content:{},MessageID:{},KeyWords:{}".format(
                    message.author.username, 
                    message.content, 
                    message.message_reference.message_id, 
                    message.referenced_message.content.split("**")[1],
                    ))
                Globals.userInfo["userName"] = message.author.username
                Globals.userInfo['lastTime'] = time.time()
                
            except:
                await message.reply("丁真抽嗨了，再发一次")
                # await message.delete()
                return
            if str(message.referenced_message.author.id) != Globals.MID_JOURNEY_ID:
                await message.reply("只能对Mid Journey说丁真")
                return
            await message.reply("丁真接收到{}的请求,已获取关键词为：{}的消息，并为用户保留{}s的时间用于键入下一步指令".format( message.author.username, 
                                                                   message.referenced_message.content.split("**")[1],
                                                                   Globals.waitTime
                                                                   ))
            await message.delete()
    except AttributeError:
        pass
    except Exception:
        print("消息监听出错：", Exception)


# 测试用的狗屎代码
@bot.command(
    name = "fuck",
    description = "测试用的捏",
    options=[
        interactions.Option(
            name="prompt",
            description="随便输入一个内容",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)
async def fuckcode(ctx: interactions.CommandContext, prompt: str = "SHIT CODE"):
    await ctx.send("Fucking Good Guys about This {}".format(prompt))



# 关于
@bot.command(
    name = "info",
    description = "关于这个程序",
)
async def info(ctx: interactions.CommandContext):
    await ctx.send(Globals.update_msg)



# 用法
@bot.command(
    name = "usage",
    description = "怎么用",
)
async def usage(ctx: interactions.CommandContext):
    await ctx.send(Globals.help_info)
    



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
        interactions.Option(
            name="area",
            description="图像比例( 1：2 ~ 2：1 )",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="versions",
            description="MidJourney使用版本( 1 - 5 )",
            type=interactions.OptionType.INTEGER,
            max_value=5,
            min_value=1,
            required=False,
        ),
        interactions.Option(
            name="quality",
            description="图片质量（ 0.25 - 2.0 ）",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="stylize",
            description="图片参数（ 0 - 1000 ）",
            type=interactions.OptionType.INTEGER,
            max_value=1000,
            min_value=0,
            required=False,
        ),
        interactions.Option(
            name="seed",
            description="种子",
            type=interactions.OptionType.INTEGER,
            max_value=4294967295,
            min_value=0,
            required=False,
        ),
        interactions.Option(
            name="chaos",
            description="设置四张图像的差异化",
            type=interactions.OptionType.INTEGER,
            max_value=100,
            min_value=0,
            required=False,
        ),
    ],
)
async def dj_imagine(ctx, prompt: str, area: str = "1:1", versions: int = 5, quality: str = "1.0", stylize: int = 2000, seed: int = 5294967295, chaos: int = 0):

    if (Globals.USE_MESSAGED_CHANNEL):
        # print(ctx.channel)
        Globals.CHANNEL_ID = str(ctx.channel.id)

    prompt = prompt + "--v {} --chaos {}".format(versions, chaos)

    if float(quality) > 0.25 and float(quality) < 2.0:
        prompt = prompt + " --quality {}".format(quality)
    
    area_num = int(area.split(":")[0])/int(area.split(":")[1]) \
                if \
                    area.count(":") == 1 and \
                    len(area.split(":")) == 2 and \
                    all(_area.isdigit() for _area in area.split(":")) \
                else 1

    if float(area_num) > 0.5 and float(area_num) < 2.0 and float(area_num) != 1.0:
        prompt = prompt + " --ar {}".format(area)
    elif float(area_num) == 1.0:
        prompt = prompt + " --ar {}".format("1:1")
    
    if seed > 0 and seed < 4294967295:
        prompt = prompt + " --seed {}".format(seed)
    
    if stylize > 0 and stylize < 1000:
        prompt = prompt + " --stylize {}".format(stylize)

    response = PassPromptToSelfBot(prompt)
    
    if response.status_code >= 400:
        print(response.txt)
        print(response.status_code)
        await ctx.send("丁真也不知道哦，再发一次去问问丽丽...")
    else:
            
        print("作画：{}".format(prompt))
        await ctx.send(
            "丁真正在画:{}".format(prompt))

	

# 进行内容变体
@bot.command(
    name = "xf",
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
            required=True,
            choices = [
                interactions.Choice(name="U:继承细分", value="U"),
                interactions.Choice(name="V:变体细分", value="V"),
            ],
        ),
        interactions.Option(
            name="reset_target",
            description="目标重置信号，默认命令执行后删除丁真目前定位的信息",
            type=interactions.OptionType.BOOLEAN,
            required=False,
        ),
    ],
)
async def dj_subdivision(ctx, number: int, change_sign: str = "U", reset_target : bool = True):
    if (number <= 0 or number > 4):
        await ctx.send("丁真只能数到四")
        return

    if Globals.targetID == "":
        await ctx.send('你还没有给丁真说用哪个图')
        return

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = str(ctx.channel.id)
    
    if change_sign.upper() == "U":
        response = Upscale(number, Globals.targetID, Globals.targetHash)
    elif change_sign.upper() == "V":
        response = Variation(number, Globals.targetID, Globals.targetHash)
    else:
        await ctx.send("丁真无法理解你打算怎么处理这个图")
        return

    if reset_target:
        Globals.targetID = ""
        Globals.userInfo = { "userName":"", "lastTime" : 0, }
    else:
        Globals.userInfo["lastTime"] = time.time()
    if response.status_code >= 400:
        await ctx.send("再回复一次，丁真忙着回笼没看清")
        return

    await ctx.send("丁真正在进行细分")


bot.start()
