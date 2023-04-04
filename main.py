from urllib import response

from discord import Object
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation, BlendImg, DjRelax, DjFast
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

    if message.content == "" or message.author.username == Globals.bot_name or message.author.username == "Midjourney Bot" : return

    try:
        if "只因你太美" in message.content:
            await message.reply("大半夜不睡觉答应某人埋的彩蛋，恭喜{}作为头号小黑子触发了这个彩蛋".format(message.author.username))
            return
        elif "丁真" in message.content and "@" in message.referenced_message.content:
            try:
                if Globals.targetID:
                    if time.time() - Globals.userInfo['lastTime'] <= Globals.waitTime and message.author.username != Globals.userInfo["userName"]:
                        await message.reply("目前丁真正在为{}进行一眼鉴定，请于{}s后进行重试".format(
                                                                                Globals.userInfo["userName"],
                                                                                Globals.waitTime - int( time.time() - Globals.userInfo['lastTime'] ),
                                                                                ))
                        return
                    elif message.author.username == Globals.userInfo["userName"]:
                        await message.reply("用户{}的目标已重新确立，时间已刷新".format(Globals.userInfo["userName"]))
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
    


# fast/relax
@bot.command(
    name = "speed",
    description = "调整速度",
    options=[
        interactions.Option(
            name="speedrate",
            description="生成速度",
            type=interactions.OptionType.STRING,
            required=True,
            choices = [
                interactions.Choice(name="极速生成", value="fast"),
                interactions.Choice(name="缓速生成", value="relax"),
            ],
        )]
)
async def speed(ctx: interactions.CommandContext, speedrate: str):
    if speedrate == "fast":
        response = DjFast()
            
    elif speedrate == "relax":
        response = DjRelax()

    if response.status_code >= 400:
        print(response.text)
        print(response.status_code)
        await ctx.send("网络错误")
        return 
            
    await ctx.send("模式切换至:{}".format(speedrate))



# blend 图片混合

@bot.command(
    name = "dblend",
    description = "图像混合",
    options=[
        interactions.Option(
            name="image1",
            description="图图",
            type=interactions.OptionType.ATTACHMENT,
            required=True,
        ),
        interactions.Option(
            name="image2",
            description="图图",
            type=interactions.OptionType.ATTACHMENT,
            required=True,
        ),
        interactions.Option(
            name="dimensions",
            description="图像尺寸",
            type=interactions.OptionType.STRING,
            required=False,
            choices = [
                interactions.Choice(name="2：3 → 半身", value="--ar 2:3"),
                interactions.Choice(name="1：1 → 矩形", value="--ar 1:1"),
                interactions.Choice(name="3：2 → 广角", value="--ar 3:2"),
            ],
        ),
        interactions.Option(
            name="image3",
            description="图图",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        ),
        interactions.Option(
            name="image4",
            description="图图",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        ),
        interactions.Option(
            name="image5",
            description="图图",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        ),
    ]
)
async def dblend(ctx: interactions.CommandContext, image1: object, image2:object, image3:object = None, image4:object = None, image5:object = None, dimensions:str = "--ar 1:1"):

    if (Globals.USE_MESSAGED_CHANNEL):

        Globals.CHANNEL_ID = str(ctx.channel.id)
    
    image = []
    try:
        for _imgObj in [image1, image2, image3, image4, image5]:
            if _imgObj:
                image.append({
                    "id": len(image),
                    "filename": _imgObj.filename,
                    "uploaded_filename": _imgObj.url
                })
        
        response = BlendImg(image, dimensions)
        
        if response.status_code >= 400:
            print(response.text)
            print(response.status_code)
            await ctx.send("网络错误")
        else:
                
            print("混合图像：image:{}, dimensions:{}".format(image, dimensions))
            await ctx.send("""丁真正在根据以下内容生成混合图片：图片组：{}，画面尺寸：{}""".format(image, dimensions))
    
    except Exception:
        print(Exception)
        await ctx.send("丁真抽嗨了，再发一次吧")



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
        interactions.Option(
            name="image",
            description="参考图",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        ),
        interactions.Option(
            name="imageratio",
            description="参考图占比（ 0 - 15 ）",
            type=interactions.OptionType.INTEGER,
            max_value=15,
            min_value=0,
            required=False,
        ),
    ],
)
async def dj_imagine(ctx, prompt: str, area: str = "1:1", versions: int = 5, quality: str = "1.0", stylize: int = 2000, seed: int = 5294967295, chaos: int = 0, image = None, imageratio: int = -1):

    if (Globals.USE_MESSAGED_CHANNEL):
        # print(ctx.channel)
        Globals.CHANNEL_ID = str(ctx.channel.id)
    try:
        if image.url and "http" in image.url:
            prompt = prompt + image.url
            if imageratio > 0:
                prompt = prompt + " --iw {}".format(((imageratio + 5) * 0.1))
    except Exception:
        print(Exception)
        await ctx.send("图片元素出错,请重试")

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
        print(response.text)
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
            max_value=4,
            min_value=1,
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

    if Globals.targetID == "" or Globals.userInfo["userName"] == "" or str(ctx.user.username) != Globals.userInfo["userName"]:
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


    if response.status_code >= 400:
        await ctx.send("再回复一次，丁真忙着回笼没看清")
        return

    await ctx.send("丁真正在对{}的需求进行细分".format(
                                                Globals.userInfo["userName"],
    ))

    if reset_target:
        Globals.targetID = ""
        Globals.userInfo = { "userName":"", "lastTime" : 0, }
    else:
        Globals.userInfo["lastTime"] = time.time()

bot.start()
