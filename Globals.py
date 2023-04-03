import os

#strings

DAVINCI_TOKEN = os.environ.get('DAVINCI_TOKEN')

SERVER_ID = os.environ.get('SERVER_ID')

SALAI_TOKEN = os.environ.get('SALAI_TOKEN')

CHANNEL_ID = os.environ.get('CHANNEL_ID')

waitTime = os.environ.get('WAIT_TIME')

#boolean
USE_MESSAGED_CHANNEL = True if(os.environ.get('CHANNEL_SIGN')=="True") else False

#don't edit the following variable
HAS_RUN = False

MID_JOURNEY_ID = "936929561302675456"  #midjourney bot id
targetID       = ""
targetHash     = ""
userInfo       = {
    "userName":"",
    "lastTime" : 0,
                  }


# bot information
bot_name = "理塘丁真"

update_msg = f"""
DandjourneyV1.2 正式上线！
Github链接：https://github.com/yuexdang/MidJourney-Wrapper
目前挂载机器人：""" + bot_name + """
最近更新时间：2023-04-03
更新内容：
谨防盗版，支持白嫖
"""

help_info = f'''
        丁真珍珠目前支持图片的生成与细分，不想支持blend功能，info功能暂时也不打算集成上去

        指令：
        /fuck 测试用的没什么用
        /dj 等价/imagine
        /xf 细分图片
	
        如何进行细分：
        1.先找到你想要进行操作的Midjourney消息，并回复这条消息：丁真
        2.丁真删了你的消息并回复丁真知道了即为成功，失败的话请重试
        3.输入/xf 调整需求后发送指令即可
    '''


