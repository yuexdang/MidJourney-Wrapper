# MidJourney-Wrapper（Yuexdang翻译版）

## 代码来源
作者：[Wildric-Auric](https://github.com/Wildric-Auric)\
原始版本：[MidJourney-Wrapper](https://github.com/Wildric-Auric/MidJourney-Wrapper)

## 目前现状
简单介绍一下，目前的项目支持用户在discord上部署一个机器人，这个机器人会替代号主（买了会员之类的，能用MidJourney的人），转发群成员提出的MidJourney需求，比如/Imagine等。\
为什么要这样？因为现在MidJourney不再支持白嫖，一个账号同时又只能支持8个人同时在线，也就是说如果团购，最多可能只能支持同时8个人使用这个机器人，这显然不符合原始的预期（虽然这么组团本身就违反了Midjourney的预期）。我希望这样一个转发机器人可以提高群成员的数量，也算是变相支持大家团购。\
这里面的图不对？不对就对了，我懒得录 Sorry

## 怎么用
* 项目下载下来
* 安装 [requirements](https://github.com/yuexdang/MidJourney-Wrapper/blob/main/requirements.txt) (我的程序中，pycord不再使用了，不用去在意pycord的版本)  注意需要Python 3.8 及以上的版本  
* 把你的数据填入 [Globals.py](https://github.com/yuexdang/MidJourney-Wrapper/blob/main/Globals.py) 
* 运行main.py即可

## 实例

### 对标 /imagine —> /dj
dj我不说是什么，我只能说是你第一个想到的那个人
```
/dj [ 必填 : 参数 (string)]
```


![ezgif-3-c4476f9a09](https://user-images.githubusercontent.com/70033490/185647413-1177b21a-2c2f-4f02-885e-c35d82179ba3.gif)


### 细分图片
图像生成后，一般会有U与V两排按钮（细分类型），但是如果账号不是购买账号，就没法用这个。这里提供一个整合版的调用规则
1. 定位你想细分的消息
```
回复MidJourney的图像消息： 丁真
```
回复丁真后如果正常，机器人会回复你丁真知道了，这个时候你的消息就已经定位好了<br>


2. 细分图片
这个我改的比较多，已经和原作者用法不一样了，可以先去理解一下原作者的想法，再看我这个就很明朗了。
```
/xf [ 必填 : 细分图片索引 (integer) ] [ 必填 : 细分方式（String：U/V）] [ 可填 : 是否重置丁真的目标 (boolean) ]
```
这个不难理解，比如你打算选V3进行图片细分，那么指令即为
```
/xf 3 V
```



## 关于这个东西
作者这边是说了关于请求失败的一些问题，我没触发过因为项目已经让我整成Railway发布了，现在在上面跑的还算顺利。\

关于Global文件内的几个参数怎么来的，我懒得放图，简单描述一下\
DAVINCI_TOKEN = [Token of Discord bot]\
SERVER_ID = [Server id here]\
SALAI_TOKEN = [Token of the Account from which you paid MidJourney ]\
CHANNEL_ID = [Channel in which commands are sent]\

- 第一个放你注册的Discord 机器人的Token，在discord developer页找到你的机器人，进入bot页面后就能看到（写了个什么只展示一次）
- 第二个放你服务器的ID，这个打开discord的开发者模式（高级设置里），然后右键你的频道，有个复制ID
- 第三个放买了会员的账号的authorization，在页面加载时去网络请求里找
- 第四个放你频道ID，这个需要在频道发个消息，然后shift+右键，选复制ID，这样复制出来的是频道ID+消息ID，你只需要前一个

机器人怎么配网上很多教程，自己找吧\

虽然代码有证书安全保护，但是CSDN等毒瘤完全不把这个当一回事，我只希望我用爱发电做出来的机器人，不会有一天出现在什么MID公众号上，打着一个听都没听过的人的名义（甚至不是程序员），两毛钱一张售卖这个机器人转发后生成的图。

*Enjoy!*（在这里保留一点原作者的内容，这样你才能知道你看的是翻译版）



