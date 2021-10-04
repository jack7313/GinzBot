'''
봇 코드를 사용할 때 꼭 출처를 남기고 사용해주세요!

수정 필요 코드: 번역의 'token', 'client_id', 'client_secret'
               검색_구글의 'my_api_key', 'my_cse_id'
               검색_네이버의 'client_id', 'client_secret'
               검색_짤의 'apikey'
               client.run('Token')의 'Token'
'''


import asyncio
from discord import Client, Intents, Activity, ActivityType, Status, Embed, __version__, ChannelType
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option, wait_for_component, ComponentContext
from discord_slash.model import SlashCommandOptionType, ButtonStyle
import time
import datetime
import random
from urllib.request import urlopen, Request
from urllib.request import HTTPError
from urllib.parse import quote
import json
from googleapiclient.discovery import build
import urllib.request
from module.SlashPaginator import Paginator
import requests
from discordTogether import DiscordTogether, errors
from module.GameUserInfo import pubg

client = Client(intents=Intents.all())
slash = SlashCommand(client, sync_commands=True)
togetherControl = DiscordTogether(client)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(__version__)
    print('------')
    print('Servers connected to:')
    guildslen = []
    for guild in client.guilds:
        guildslen.append(guild)
    print(f"[{len(guildslen)}개의 서버]")
    global start_uptime
    start_uptime = time.time()
    print("Ready!")
    while True:
        guilds = []
        members = []
        for i in client.guilds:
            guilds.append(i.name)
            members.append(i.member_count)
        act = ["'/' 슬래시로 작동", f"{len(guilds)}개의 서버에서 ", f"{sum(members)}명과 함께", "도움말은 [/도움말]", "버그 제보는 [/건의]"]
        for i in act:
            if i == act[3]:
                acttype = ActivityType.watching
            elif i == act[4]:
                acttype = ActivityType.watching
            else:
                acttype = ActivityType.playing
            activity = Activity(type=acttype, name=i)
            await client.change_presence(status=Status.online, activity=activity)
            await asyncio.sleep(3)

guildlist = []
for guild in client.guilds:
    list.append(guild.id)
guild_ids = guildlist


@client.event
async def on_message(ctx):
    if ctx.content.startswith("/hellothisisverification"):
        await ctx.channel.send("긴급재난문자_#1978")
    if ctx.content.startswith("+건의 "):
        if ctx.author.id == 755775043426058340:
            with open('D:\Python_Discord_BOT\Slash_EDB\suggest.json','r', encoding='UTF8') as f:
                suggest = json.load(f)
                msg = ctx.content[4:30]
                msg1 = ctx.content[31:]
                userid = int(suggest[msg]["suggestorid"])
                content = suggest[msg]["content"]
                sugtype = suggest[msg]["type"]
                username = suggest[msg]["suggestor"]
                username1 = client.get_user(userid)
                embed = Embed(title=sugtype, description=content, color=0x0067a3)
                embed.set_footer(text=f"{username}님의 건의", icon_url=username1.avatar_url)
                await username1.send(embed=embed)
                embed = Embed(title="[답장] " + msg1, color=0x008000)
                await username1.send(embed=embed)
        else:
            return None

@slash.slash(name="핑",
            description="봇의 핑을 알려줍니다.")
async def ping(ctx):
    await ctx.send(f"퐁! `{round(client.latency*1000)}ms`")

@slash.slash(name="유저정보",
            description="유저의 정보를 불러옵니다.",
            options=[
                create_option(
                    name="유저",
                    description="정보를 불러올 유저를 선택하세요.",
                    option_type=6,
                    required=True)])
async def userinfo(ctx, 유저: int):
    date = datetime.datetime.utcfromtimestamp(((유저.id >> 22) + 1420070400000) / 1000)
    embed=Embed(title="유저 정보", description=f"{유저.name}님의 정보", colour=0x0067a3)
    embed.set_author(name=유저,icon_url=유저.avatar_url)
    embed.set_thumbnail(url=유저.avatar_url)
    embed.add_field(name="닉네임", value=유저.name, inline=True)
    embed.add_field(name="ID", value=유저.id, inline=True)
    embed.add_field(name="디스코드 가입일", value=f"{date.year}년 {date.month}월 {date.day}일", inline=True)
    await ctx.send(embed=embed)

@slash.slash(name="서버정보",
            description="이 서버의 정보를 불러옵니다.",)
async def guildinfo(ctx):
    embed=Embed(title="서버 정보", description=f"{ctx.guild}의 정보", colour=0x0067a3)
    embed.set_author(name=ctx.guild,icon_url=ctx.guild.icon_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="이름", value=ctx.guild, inline=True)
    embed.add_field(name="ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="생성일", value=ctx.guild.created_at, inline=True)
    embed.add_field(name="주인", value=ctx.guild.owner, inline=True)
    embed.add_field(name="멤버 수", value=ctx.guild.member_count, inline=True)
    await ctx.send(embed=embed)

@slash.slash(name="업타임",
            description="봇이 작동된 시간을 알려줍니다.")
async def uptime(ctx):
    new_uptime = time.time()
    now_uptime = new_uptime - start_uptime
    bot_uptime = str(datetime.timedelta(seconds=int(round(now_uptime)))).split(":")
    uptime = f"**{bot_uptime[0]}**시간 **{bot_uptime[1]}**분 **{bot_uptime[2]}**초"
    await ctx.send(f"봇이 작동된지 {uptime}가 지났습니다.")

@slash.slash(name="킥",
            description="유저를 킥합니다.",
            options=[
                create_option(
                    name="유저",
                    description="킥할 유저를 선택하세요.",
                    option_type=6,
                    required=True),
                create_option(
                    name="사유",
                    description="킥하는 이유를 입력하세요.",
                    option_type=3,
                    required=True)])
async def kick(ctx, 유저: str, 사유: str):
    if ctx.author.guild_permissions.manage_guild:
        embed = Embed(title="킥",description=f"`{사유}`의 이유로 {유저.name}님을 킥했습니다.",colour=0xff0000)
        await ctx.send(embed=embed)
        await ctx.guild.kick(유저,reason=사유)
    else:
        embed = Embed(title=":warning: 권한 없음",description=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="밴",
            description="유저를 밴합니다.",
            options=[
                create_option(
                    name="유저",
                    description="밴할 유저를 선택하세요.",
                    option_type=6,
                    required=True),
                create_option(
                    name="사유",
                    description="밴하는 이유를 입력하세요.",
                    option_type=3,
                    required=True)])
async def ban(ctx, 유저: str, 사유: str):
    if ctx.author.guild_permissions.manage_guild:
        embed = Embed(title="밴",description=f"`{사유}`의 이유로 {유저.name}님을 밴했습니다.",colour=0xff0000)
        await ctx.send(embed=embed)
        await ctx.guild.ban(유저,reason=사유)
    else:
        embed = Embed(title=":warning: 권한 없음",description=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="뮤트",
            description="유저를 뮤트합니다.",
            options=[
                create_option(
                    name="유저",
                    description="뮤트할 유저를 선택하세요.",
                    option_type=6,
                    required=True),
                create_option(
                    name="사유",
                    description="뮤트하는 이유를 입력하세요.",
                    option_type=3,
                    required=True)])
async def mute(ctx, 유저: str, 사유: str):
    if ctx.author.guild_permissions.manage_channels:
        embed = Embed(title=f"`{사유}`의 이유로 {유저.name}님을 뮤트했습니다.",colour=0xff0000)
        await ctx.send(embed=embed)
        await ctx.channel.set_permissions(유저, send_messages=False)
    else:
        embed = Embed(title=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="언뮤트",
            description="유저를 언뮤트합니다.",
            options=[
                create_option(
                    name="유저",
                    description="언뮤트할 유저를 선택하세요.",
                    option_type=6,
                    required=True)])
async def unmute(ctx, 유저: str):
    if ctx.author.guild_permissions.manage_channels:
        embed = Embed(title=f"{유저.name}님의 뮤트를 해제했습니다.",colour=0xff0000)
        await ctx.send(embed=embed)
        await ctx.channel.set_permissions(유저, send_messages=None)
    else:
        embed = Embed(title=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="번역",
            description="번역할 내용을 번역합니다.",
            options=[
                create_option(
                    name="언어",
                    description="언어를 선택하세요.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="한국어 -> 영어",
                            value="ko-en"),
                        create_choice(
                            name="영어 -> 한국어",
                            value="en-ko"),
                        create_choice(
                            name="한국어 -> 일본어",
                            value="ko-ja"),
                        create_choice(
                            name="일본어 -> 한국어",
                            value="ja-ko"),
                        create_choice(
                            name="한국어 -> 중국어",
                            value="ko-ch"),
                        create_choice(
                            name="중국어 -> 한국어",
                            value="ch-ko"),
                        ]),
                create_option(
                    name="내용",
                    description="번역할 내용을 입력하세요.",
                    option_type=3,
                    required=True
                )])
async def translate(ctx, 언어: str, 내용: str):
    if 언어 == "ko-en":
        #discord bot tokken
        token = 'token'
        #Naver Open API application ID
        client_id = "client_id"
        #Naver Open API application token
        client_secret = "client_secret"
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = 내용.split(" ")
        try:
            if 내용 == None:
                await ctx.send(embed=Embed(title="내용이 입력되지 않았습니다.", color=0xff0000), hidden=True)
            else:
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ko&target=en&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))
                responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = Embed(title="번역 결과 | 한국어 -> 영어", description="", color=0x5CD1E5)
                embed.add_field(name="한국어", value=savedCombineword, inline=False)
                embed.add_field(name="영어", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                embed.set_footer(text="네이버 파파고 API를 사용합니다.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode,hidden=True)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.",hidden=True)
    if 언어 == "ko-ja":
        #discord bot tokken
        token = 'token'
        #Naver Open API application ID
        client_id = "client_id"
        #Naver Open API application token
        client_secret = "client_secret"
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = 내용.split(" ")
        try:
            if 내용 == None:
                await ctx.send(embed=Embed(title="내용이 입력되지 않았습니다.", color=0xff0000), hidden=True)
            else:
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ko&target=ja&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))
                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = Embed(title="번역 결과 | 한국어 -> 일본어", description="", color=0x5CD1E5)
                    embed.add_field(name="한국어", value=savedCombineword, inline=False)
                    embed.add_field(name="일본어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="네이버 파파고 API를 사용합니다.")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Error Code : " + responsedCode,hidden=True)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.",hidden=True)
    if 언어 == "ko-ch":
        #discord bot tokken
        token = 'token'
        #Naver Open API application ID
        client_id = "client_id"
        #Naver Open API application token
        client_secret = "client_secret"
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = 내용.split(" ")
        try:
            if 내용 == None:
                await ctx.send(embed=Embed(title="내용이 입력되지 않았습니다.", color=0xff0000), hidden=True)
            else:
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ko&target=zh-CN&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))
                responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = Embed(title="번역 결과 | 한국어 -> 중국어(간체)", description="", color=0x5CD1E5)
                embed.add_field(name="한국어", value=savedCombineword, inline=False)
                embed.add_field(name="중국어(간체)", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                embed.set_footer(text="네이버 파파고 API를 사용합니다.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode,hidden=True)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.",hidden=True)
    if 언어 == "en-ko":
        #discord bot tokken
        token = 'token'
        #Naver Open API application ID
        client_id = "client_id"
        #Naver Open API application token
        client_secret = "client_secret"
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = 내용.split(" ")
        try:
            if 내용 == None:
                await ctx.send(embed=Embed(title="내용이 입력되지 않았습니다.", color=0xff0000), hidden=True)
            else:
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=en&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))
                responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = Embed(title="번역 결과 | 영어 -> 한국어", description="", color=0x5CD1E5)
                embed.add_field(name="영어", value=savedCombineword, inline=False)
                embed.add_field(name="한국어", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                embed.set_footer(text="네이버 파파고 API를 사용합니다.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode,hidden=True)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.",hidden=True)
    if 언어 == "ja-ko":
        #discord bot tokken
        token = 'token'
        #Naver Open API application ID
        client_id = "client_id"
        #Naver Open API application token
        client_secret = "client_secret"
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = 내용.split(" ")
        try:
            if 내용 == None:
                await ctx.send(embed=Embed(title="내용이 입력되지 않았습니다.", color=0xff0000), hidden=True)
            else:
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ja&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))
                responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = Embed(title="번역 결과 | 일본어 -> 한국어", description="", color=0x5CD1E5)
                embed.add_field(name="일본어", value=savedCombineword, inline=False)
                embed.add_field(name="한국어", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                embed.set_footer(text="네이버 파파고 API를 사용합니다.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode,hidden=True)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.",hidden=True)
    if 언어 == "ch-ko":
        #discord bot tokken
        token = 'token'
        #Naver Open API application ID
        client_id = "client_id"
        #Naver Open API application token
        client_secret = "client_secret"
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = 내용.split(" ")
        try:
            if 내용 == None:
                await ctx.send(embed=Embed(title="내용이 입력되지 않았습니다.", color=0xff0000), hidden=True)
            else:
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=zh-CN&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))
                responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = Embed(title="번역 결과 | 중국어(간체) -> 한국어", description="", color=0x5CD1E5)
                embed.add_field(name="중국어(간체)", value=savedCombineword, inline=False)
                embed.add_field(name="한국어", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                embed.set_footer(text="네이버 파파고 API를 사용합니다.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode,hidden=True)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.",hidden=True)

@slash.slash(name="봇정보",
            description="Slash_ED봇의 정보를 알려줍니다.")
async def botinfo(ctx):
    edbslash = client.get_user(837530519892787270)
    date = datetime.datetime.utcfromtimestamp(((int(edbslash.id) >> 22) + 1420070400000) / 1000)
    list = []
    for i in client.guilds:
        list.append(i.name)
    list1 = []
    for i in client.guilds:
        list1.append(i.member_count)
    embed=discord.Embed(title="긵봇 정보", colour=0x0067a3)
    embed.set_author(name=edbslash,icon_url=edbslash.avatar_url)
    embed.set_thumbnail(url=edbslash.avatar_url)
    embed.add_field(name="소개", value="긵봇", inline=True)
    embed.add_field(name="기능", value="`/도움말`을 참고해주세요.", inline=True) 
    embed.add_field(name="탄생일", value=f"**{date.year}**년 **{date.month}**월 **{date.day}**일", inline=True)
    embed.add_field(name="가입된 서버 수", value=f"{len(list)}개\n({sum(list1)}명)", inline=True)
    embed.add_field(name="초대 링크", value="https://c11.kr/discordbot_ginzbot", inline=True)
    embed.add_field(name="개발자", value="긴급재난문자_#1978", inline=True) 
    await ctx.send(embed=embed)

@slash.slash(name="타이머",
            description="타이머를 잽니다.",
            options=[
                create_option(
                    name="제목",
                    description="타이머의 제목을 입력하세요.",
                    option_type=3,
                    required=True),
                create_option(
                    name="시간",
                    description="타이머 시간(초)을 입력하세요. (중간에 봇이 꺼지면 타이머가 취소됩니다.)",
                    option_type=4,
                    required=True)
            ])
async def timer(ctx, 제목: str, 시간: int):
    if 시간 < 0:
        embed = Embed(title="시간을 자연수로 입력해주세요.", colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)
    else:
        embed = Embed(title=f":timer: {제목}", description=f"{시간}초 타이머를 시작합니다.", colour=0x0067a3)
        timer = await ctx.send(embed=embed)
        await asyncio.sleep(시간)
        embed = Embed(title=f":timer: {제목}", description=f"{시간}초 타이머가 끝났습니다.", colour=0xff0000)
        await timer.reply(ctx.author.mention, embed=embed)

@slash.slash(name="검색_구글",
            description="구글에서 검색할 내용을 검색합니다.",
            options=[
                create_option(
                    name="내용",
                    description="검색할 내용을 입력하세요.",
                    option_type=3,
                    required=True
                )])
async def googlesearch(ctx, 내용: str):
    my_api_key = "my_api_key"
    my_cse_id = "my_cse_id"  
    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res

    search_result = google_search(내용, my_api_key, my_cse_id)
    items=search_result['items']
    title = []
    link = []

    for i in items:
        title.append(str(i['title']))
        link.append(str(i['link']))

    searchlen = len(title)

    embed = Embed(title=내용,description="구글 검색 결과",colour=0x4285f4)
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScuoKGScAHkMXYEpDAOr4y3zPJz3Kura9TesWte2ueTAIGdyeP5KVwq-0Q8BobSm-iaqs&usqp=CAU")
    for i in range(searchlen):
        embed.add_field(name=title[i], value=link[i], inline=False)
        if i == 5:
            break
    embed.set_footer(text="구글 검색 API를 사용합니다.",icon_url="https://img.icons8.com/color/452/google-logo.png")

    await ctx.send(embed=embed)

@slash.slash(name="검색_네이버",
            description="네이버에서 검색할 내용을 검색합니다.",
            options=[
                create_option(
                    name="내용",
                    description="검색할 내용을 입력하세요.",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="종류",
                    description="검색할 종류를 선택하세요.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="블로그",
                            value="blog"),
                        create_choice(
                            name="뉴스",
                            value="news"),
                        create_choice(
                            name="책",
                            value="book"),
                        create_choice(
                            name="백과사전",
                            value="encyc"),
                        create_choice(
                            name="영화",
                            value="movie"),
                        create_choice(
                            name="카페글",
                            value="cafearticle"),
                        create_choice(
                            name="지식IN",
                            value="kin"),
                        create_choice(
                            name="지역",
                            value="local"),
                        create_choice(
                            name="쇼핑",
                            value="shop")]
                )])
async def naversearch(ctx, 내용: str, 종류: int):
    client_id = "client_id"
    client_secret = "client_secret"
    encText = urllib.parse.quote(내용)
    url = f"https://openapi.naver.com/v1/search/{종류}?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        api_callResult = response_body.decode('utf-8')
        api_callResult = json.loads(api_callResult)
        items=api_callResult['items']
        title = []
        link = []
        for i in items:
            title.append(str(i['title']).replace("<b>", "").replace("</b>", ""))
            link.append(str(i['link']))
        searchlen = len(title)
        if 종류 == "blog":
            category = "블로그"
        elif 종류 == "news":
            category = "뉴스"
        elif 종류 == "book":
            category = "책"
        elif 종류 == "encyc":
            category = "백과사전"
        elif 종류 == "movie":
            category = "영화"
        elif 종류 == "cafearticle":
            category = "카페글"
        elif 종류 == "kin":
            category = "지식IN"
        elif 종류 == "local":
            category = "지역"
        elif 종류 == "shop":
            category = "쇼핑"
        embed = Embed(title = 내용, description = f"네이버 {category} 검색 결과", colour=0x04cf5c)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861433037031866368/asdfasdfasdfasdfasdf.png")
        for i in range(searchlen):
            embed.add_field(name=title[i], value=link[i], inline=False)
            if i == 5:
                break
        embed.set_footer(text="네이버 검색 API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861437791917178880/asdfadsfasdfadsf.png")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=Embed(title = "Error Code:" + rescode, color = 0xff0000), hidden=True)

@slash.slash(name="검색_짤",
            description="Tenor에서 짤을 검색합니다.",
            options=[
                create_option(
                    name="내용",
                    description="검색할 짤의 내용을 입력하세요.",
                    option_type=3,
                    required=True)])
async def tenorgif(ctx, 내용: str):
    apikey = "apikey"  # test value
    lmt = 10

    # our test search
    search_term = 내용

    # get the top 8 GIFs for the search term using default locale of EN_US
    r = requests.get(f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        def gif(asdf):
            return top_8gifs["results"][asdf]["media"][0]["gif"]["url"]
        embed1 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed2 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed3 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed4 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed5 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed6 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed7 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed8 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed9 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed10 = discord.Embed(title=내용, description="짤 검색 결과", colour=0x47aafb)
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed6.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed7.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed8.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed9.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed10.set_thumbnail(url="https://cdn.discordapp.com/attachments/849872302707441694/861804356758929448/fd.png")
        embed1.set_image(url=gif(0))
        embed2.set_image(url=gif(1))
        embed3.set_image(url=gif(2))
        embed4.set_image(url=gif(3))
        embed5.set_image(url=gif(4))
        embed6.set_image(url=gif(5))
        embed7.set_image(url=gif(6))
        embed8.set_image(url=gif(7))
        embed9.set_image(url=gif(8))
        embed10.set_image(url=gif(9))
        embed1.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed2.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed3.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed4.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed5.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed6.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed7.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed8.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed9.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        embed10.set_footer(text="Tenor API를 사용합니다.",icon_url="https://cdn.discordapp.com/attachments/849872302707441694/861805242814038076/ds.png")
        await Paginator(bot=client, ctx=ctx, pages=[embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10])
    else:
        await ctx.send(embed=Embed(title = "Error Code:" + r.status_code, color = 0xff0000), hidden=True)

@slash.slash(name="도움말",
            description="Slash_ED봇의 도움말입니다.")
async def help(ctx):
    embed = Embed(title="도움말", description="기본 명령어", color=0x0067a3)
    embed1 = Embed(title="도움말", description="관리 명령어", color=0x0067a3)
    embed10 = Embed(title="도움말", description="즐겨찾기 명령어", color=0x0067a3)
    embed7 = Embed(title="도움말", description="게임 명령어", color=0x0067a3)
    embed2 = Embed(title="도움말", description="정보 명령어", color=0x0067a3)
    embed4 = Embed(title="도움말", description="번역 명령어", color=0x0067a3)
    embed5 = Embed(title="도움말", description="검색 명령어", color=0x0067a3)
    embed8 = Embed(title="도움말", description="QR코드 명령어", color=0x0067a3)
    embed6 = Embed(title="도움말", description="그 외 명령어", color=0x0067a3)

    embed.add_field(name="핑", value="봇의 핑을 알려줍니다.", inline=False)
    embed.add_field(name="업타임", value="봇이 작동된 시간을 알려줍니다.")
    embed.add_field(name="타이머", value="타이머를 잽니다.\n중간에 봇이 꺼지면 타이머가 취소됩니다.", inline=False)

    embed1.add_field(name="킥", value="유저를 킥합니다.\n이때 킥된 유저는 다시 서버에 들어올 수 있습니다.", inline=False)
    embed1.add_field(name="밴", value="유저를 밴합니다.\n이때 밴된 유저는 관리자가 차단 목록에서 빼지 않는 이상 다시 들어올 수 없습니다.", inline=False)
    embed1.add_field(name="뮤트", value="유저를 뮤트합니다.\n`/언뮤트` 명령어 유저를 언뮤트할 수 있습니다.", inline=False)
    embed1.add_field(name="언뮤트", value="유저를 언뮤트합니다.\n`/뮤트` 명령어로 다시 유저를 뮤트할 수 있습니다.", inline=False)
    embed1.add_field(name="삭제", value="메시지를 삭제합니다.\n입력한 개수만큼 메시지가 삭제됩니다.", inline=False)
    embed1.add_field(name="역할부여", value="유저에게 역할을 부여합니다.\n`/역할해제` 명령어로 다시 해제할 수 있습니다.", inline=False)
    embed1.add_field(name="역할해제", value="유저의 역할을 해제합니다.\n`/역할부여` 명령어로 다시 역할을 부여할 수 있습니다.", inline=False)

    embed10.add_field(name="즐겨찾기 (컨텍스트 메뉴)", value="메시지를 즐겨찾기 목록에 추가합니다.\n`/즐겨찾기_목록` 명령어로 즐겨찾기 목록을 확인할 수 있습니다.", inline=False)
    embed10.add_field(name="즐겨찾기_목록", value="즐겨찾기 목록을 확인합니다.")

    embed7.add_field(name="게임", value="음성 채널에서 게임(활동)을 합니다.\n유튜브 시청, 추리 게임, 낚시 게임, 체스 게임에서 선택할 수 있습니다.\n음성 채널을 선택하지 않으면 오류가 발생합니다.\n(꼭 음성 채널을 선택해주세요!)\n오류는 https://docs.discord-together.ml/docs/errors 를 참고해주세요.\n그 외 오류는 `/건의` 명령어를 사용해주세요.", inline=False)

    embed2.add_field(name="유저정보", value="유저의 정보를 불러옵니다.\n유저의 닉네임, 아이콘, ID, 디스코드 가입일을 불러옵니다.", inline=False)
    embed2.add_field(name="서버정보", value="이 서버의 정보를 불러옵니다.\n서버의 이름, 아이콘, ID, 생성일, 주인, 멤버 수를 불러옵니다.", inline=False)
    embed2.add_field(name="봇정보", value="Slash_ED봇의 정보를 알려줍니다.\n봇의 닉네임, 아이콘, 소개, 기능, 탄생일, 서버 수, 초대 링크, 개발자를 알려줍니다.", inline=False)

    embed4.add_field(name="번역", value="번역할 내용을 번역합니다.\n한국어에서 영/일/중으로, 영/일/중에서 한국어로 번역합니다.", inline=False)

    embed5.add_field(name="검색_구글", value="구글에서 검색할 내용을 검색합니다.\n검색 결과 중 5개만 표시됩니다.", inline=False)
    embed5.add_field(name="검색_네이버", value="네이버에서 검색할 내용을 검색합니다.\n블로그, 뉴스, 책, 백과사전, 영화, 카페글, 지식IN, 지역, 쇼핑 중 하나로 검색할 수 있습니다.\n검색 결과 중 5개만 표시됩니다.", inline=False)
    embed5.add_field(name="검색_짤", value="Tenor에서 짤을 검색합니다.\n검색된 짤 중 10개만 표시됩니다.", inline=False)

    embed8.add_field(name="QR코드_생성", value="QR코드를 생성합니다.\n입력된 내용으로 QR코드가 만들어집니다.\n(띄어쓰기를 입력하면 오류가 발생하니 주의해주세요!)", inline=False)
    embed8.add_field(name="QR코드_인식", value="QR코드를 인식합니다.\n입력된 QR코드의 이미지 주소를 인식합니다.\n흔들렸거나 흐릿한 QR코드는 인식을 못할 수도 있습니다.", inline=False)

    embed6.add_field(name="건의", value="봇의 버그나 필요한 기능을 건의합니다.\n건의가 관리자에게 전송됩니다.\n버그는 최대 일주일 이내로 고쳐집니다.\n버그가 수정됐거나 필요한 기능이 추가되면 건의자의 DM으로 처리되었다는 메시지가 보내집니다.", inline=False)

    await Paginator(bot=client, ctx=ctx, pages=[embed, embed1, embed10, embed7, embed2, embed4, embed5, embed8, embed6])

@slash.slash(name="건의",
            description="봇의 버그나 필요한 기능을 건의합니다.",
            options=[
                create_option(
                    name="종류",
                    description="건의할 종류를 선택하세요.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="버그",
                            value="bug"),
                        create_choice(
                            name="필요한 기능",
                            value="required")]),
                create_option(
                    name="내용",
                    description="건의할 내용을 입력하세요.",
                    option_type=3,
                    required=True)])
async def suggest(ctx, 종류: str, 내용: str):
    if 종류 == "bug":
        type = "버그"
    else:
        type = "필요한 기능"
    SUGGEST = {"type": 종류, "content": 내용, "suggestor": f"{ctx.author}", "suggestorid": f"{ctx.author.id}"}
    with open('suggest.json','r', encoding='UTF8') as f:
        suggest = json.load(f)
        suggest[str(datetime.datetime.now())] = SUGGEST
        with open('suggest.json','w',encoding='utf-8') as mk_f:
            json.dump(suggest,mk_f,indent='\t', ensure_ascii=False)
            embed = Embed(title="성공적으로 건의가 등록됐습니다.", color=0x008000)
            await ctx.send(embed=embed, hidden=True)
            embed = Embed(title=type, description=내용, color=0x0067a3)
            embed.set_footer(text=f"{ctx.author.name}님의 건의", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed, hidden=True)
            print("==========")
            print(f"{ctx.author}님의 건의:")
            print(f"[{type}] {내용}")
            print(datetime.datetime.now())
            print("==========")
            edm = client.get_user(755775043426058340)
            embed = Embed(title="새로운 건의가 등록되었습니다.", color=0x008000)
            await edm.send(embed=embed)
            embed = Embed(title=type, description=내용, color=0x0067a3)
            embed.set_footer(text=f"{ctx.author.name}님의 건의", icon_url=ctx.author.avatar_url)
            await edm.send(embed=embed)
            
@slash.slash(name="삭제",
            description="메시지를 삭제합니다.",
            options=[
                create_option(
                    name="개수",
                    description="삭제할 메시지의 개수를 입력하세요.",
                    option_type=4,
                    required=True)])
async def clear(ctx, 개수: int):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.channel.purge(limit=개수)
        embed = Embed(title=f"{개수}개의 메시지를 삭제했습니다.",colour=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = Embed(title=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)
        
@slash.slash(name="역할부여",
            description="유저에게 역할을 부여합니다.",
            options=[
                create_option(
                    name="유저",
                    description="역할을 부여할 유저를 선택하세요.",
                    option_type=6,
                    required=True),
                create_option(
                    name="역할",
                    description="유저에게 부여할 역할을 선택하세요.",
                    option_type=8,
                    required=True)])
async def giverole(ctx, 유저: str, 역할: str):
    if ctx.author.guild_permissions.manage_guild:
        embed = Embed(title=f"{유저.name}님에게 `{역할.name}` 역할을 부여했습니다.", colour=0x008000)
        await ctx.send(embed=embed)
        await 유저.add_roles(역할)
    else:
        embed = Embed(title=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="역할해제",
            description="유저의 역할을 해제합니다.",
            options=[
                create_option(
                    name="유저",
                    description="역할을 해제할 유저를 선택하세요.",
                    option_type=6,
                    required=True),
                create_option(
                    name="역할",
                    description="유저에게 해제할 역할을 선택하세요.",
                    option_type=8,
                    required=True)])
async def receiverole(ctx, 유저: str, 역할: str):
    if ctx.author.guild_permissions.manage_guild:
        embed = Embed(title=f"{유저.name}님의 `{역할.name}` 역할을 해제했습니다.", colour=0x008000)
        await ctx.send(embed=embed)
        await 유저.remove_roles(역할)
    else:
        embed = Embed(title=f"{ctx.author.name}님은 권한이 없습니다.",colour=0xff0000)
        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="게임",
            description="음성 채널에서 게임(활동)을 합니다.",
            guild_ids=guildlist,
            options=[
                create_option(
                    name="채널",
                    description="게임(활동)을 할 음성 채널을 선택하세요.",
                    option_type=7,
                    required=True),
                create_option(
                    name="활동",
                    description="음성 채널에서 할 활동을 선택하세요.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="YouTube Together",
                            value="youtube"),
                        create_choice(
                            name="Betrayal.io",
                            value="betrayal"),
                        create_choice(
                            name="Fishington.io",
                            value="fishing"),
                        create_choice(
                            name="Chess in the Park",
                            value="chess"),
                        create_choice(
                            name="Letter Tile",
                            value="letter-tile"),
                        create_choice(
                            name="Word Snack",
                            value="word-snack"),
                        create_choice(
                            name="Doodle Crew",
                            value="doodle-crew"),])])
async def gameactivity(ctx: SlashContext, 채널: int, 활동: str):
    if 활동 == "youtube":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/870542147781296158/b099b4395fab6da6.png"
        name = "Youtube Together"
        desc = "유튜브를 시청하세요!"
    elif 활동 == "betrayal":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/870543023656828988/icon.png"
        name = "Betrayal.io"
        desc = "Betrayal.io를 플레이하세요!"
    elif 활동 == "fishing":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/870543484040409138/fishington-io-game37.png"
        name = "Fishington.io"
        desc = "Fishington.io를 플레이하세요!"
    elif 활동 == "chess":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/870569799116288001/dfdfdsfsasdf.png"
        name = "Chess in the Park"
        desc = "Chess in the Park를 플레이하세요!"
    elif 활동 == "letter-tile":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/893401950169739274/unknown.png"
        name = "Letter Tile"
        desc = "Letter Tile를 플레이하세요!"
    elif 활동 == "word-snack":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/893403658484584468/unknown.png"
        name = "Word Snack"
        desc = "Word Snack를 플레이하세요!"
    elif 활동 == "doodle-crew":
        icon = "https://cdn.discordapp.com/attachments/849872302707441694/893402639180656660/unknown.png"
        name = "Doodle Crew"
        desc = "Doodle Crew를 플레이하세요!"
    link = await togetherControl.create_link(채널.id, 활동)
    embed = Embed(title=name, description=f"https://{link.short_link}\n위 링크로 들어가 {desc}", color=0x0067a3)
    embed.set_thumbnail(url=icon)
    embed.set_footer(text="DiscordTogether 모듈을 사용합니다.",icon_url="https://i.ibb.co/nCr7dnf/DT-Logo-New.png")
    if 채널.type == ChannelType.voice:
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=Embed(title="선택한 채널이 음성 채널이 아닙니다.", colour=0xff0000), hidden=True)

@slash.slash(name="QR코드_생성",
            description="QR코드를 생성합니다.",
            options=[
                create_option(
                    name="내용",
                    description="QR코드를 만들 내용을 입력하세요.",
                    option_type=3,
                    required=True)])
async def createqr(ctx, 내용: str):
    await ctx.defer()
    # qrcode = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?data={내용}")
    qrcode = requests.get(f"https://chart.googleapis.com/chart?cht=qr&chs=250x250&chl={내용}")
    if qrcode.status_code == 200:
        embed = Embed(title=내용, color=0x0067a3)
        # embed.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?data={내용}")
        embed.set_image(url=f"https://chart.googleapis.com/chart?cht=qr&chs=250x250&chl={내용}")
        # embed.set_footer(text="QR Code Generator API를 사용합니다.", icon_url="https://api.qrserver.com/v1/create-qr-code/?qzone=10&data=https://goqr.me/")
        embed.set_footer(text="구글 QR코드 API를 사용합니다.", icon_url="https://api.qrserver.com/v1/create-qr-code/?qzone=10&data=https://developers.google.com/chart/infographics/docs/qr_codes")
        # await asyncio.sleep(5)
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=Embed(title=f"Error Code: {qrcode.status_code}", color=0xff0000), hidden=True)

@slash.slash(name="QR코드_인식",
            description="QR코드를 인식합니다.",
            options=[
                create_option(
                    name="주소",
                    description="QR코드의 이미지 주소를 입력하세요.",
                    option_type=3,
                    required=True)])
async def readqr(ctx, 주소: str):
    await ctx.defer()
    if 주소.startswith("https://") or 주소.startswith("http://"):
        qrcode = requests.get(f"https://api.qrserver.com/v1/read-qr-code/?fileurl={주소}")
        if qrcode.status_code == 200:
            qrcontent = json.loads(qrcode.content)[0]["symbol"][0]["data"]
            if qrcontent == None:
                await ctx.send(embed=Embed(title="QR코드 인식중 오류가 발생했습니다.", color=0xff0000), hidden=True)
            else:
                embed = Embed(title=qrcontent, description=f"[QR코드 이미지 주소]({주소})", color=0x0067a3)
                embed.set_footer(text="QR Code Generator API를 사용합니다.", icon_url="https://api.qrserver.com/v1/create-qr-code/?qzone=10&data=https://goqr.me/")
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=Embed(title=f"Error Code: {qrcode.status_code}", color=0xff0000), hidden=True)
    else:
        await ctx.send(embed=Embed(title="잘못된 이미지 주소입니다.", color=0xff0000), hidden=True)

@slash.slash(name="전적_배틀그라운드",
            description="유저의 배틀그라운드 전적을 알려줍니다.",
            options=[
                create_option(
                    name="닉네임",
                    description="유저의 닉네임을 입력하세요.",
                    option_type=3,
                    required=True),
                create_option(
                    name="플렛폼",
                    description="유저의 플렛폼을 선택하세요.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="Steam",
                            value="0"),
                        create_choice(
                            name="Kakao",
                            value="1"),
                        create_choice(
                            name="XBox",
                            value="2"),
                        create_choice(
                            name="PlayStation",
                            value="3"),
                        create_choice(
                            name="Stadia",
                            value='4')]),
                create_option(
                    name="매치_종류",
                    description="매치의 종류를 선택하세요.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="일반전",
                            value="normal"),
                        create_choice(
                            name="경쟁전",
                            value="ranked")])])
async def pubginfo(ctx, 닉네임: str, 플렛폼: str, 매치_종류: str):
    await ctx.defer()
    pubglist = await pubg(닉네임, int(플렛폼), 매치_종류)
    if str(type(pubglist)) == "<class 'list'>":
        await Paginator(bot=client, ctx=ctx, pages=pubglist)
    else:
        await ctx.send(embed=pubglist, hidden=True)
        
@slash.context_menu(name="즐겨찾기",
                    target=ContextMenuType.MESSAGE)
async def bookmark(ctx: MenuContext):
    data = {
        "message_id": ctx.target_message.id,
        "message_link": ctx.target_message.jump_url,
        "author_id": ctx.author.id,
        "message_channel_id": ctx.channel.id,
        "marked_date": datetime.datetime.now()
    }

    if MongoDB[str(ctx.author.id)].find_one({"message_id": ctx.target_message.id}):
        await ctx.send(embed=Embed(title="이미 메시지가 즐겨찾기에 등록되어 있습니다.", color=Colour.red()), hidden=True)

    else:
        MongoDB[str(ctx.author.id)].insert_one(data)

        embed = Embed(title="즐겨찾기", description=ctx.target_message.content, color=Colour.gold())
        embed.set_footer(text=f"즐겨찾기 등록일: {data['marked_date']}")

        await ctx.send(embed=embed, hidden=True)

@slash.slash(name="즐겨찾기_목록",
            description="등록되어 있는 즐겨찾기를 불러옵니다.")
async def loadbookmark(ctx: SlashContext):
    find_doc = list(MongoDB[str(ctx.author.id)].find())
    embeds = []
    for doc in range(len(find_doc)):
        channel = client.get_channel(int(find_doc[doc-1]["message_channel_id"]))
        message = await channel.fetch_message(int(find_doc[doc-1]["message_id"]))
        embeds.append(Embed(title="즐겨찾기", description=f"{message.content}\n[**이동하기**]({find_doc[doc-1]['message_link']})", color=Colour.gold()).set_footer(text=f"{ctx.author.name}님의 즐겨찾기 목록", icon_url=ctx.author.avatar_url))
        # embeds.append(Embed(title="즐겨찾기", description=f"(message.content)\n[**이동하기**]({find_doc[doc-1]['message_link']})", color=Colour.gold()).set_footer(text=f"{ctx.author.name}님의 즐겨찾기 목록", icon_url=ctx.author.avatar_url))
    if embeds == []:
        await ctx.send(embed=Embed(title="등록되어 있는 즐겨찾기를 찾을 수 없습니다.", color=Colour.red()), hidden=True)
    await Paginator(bot=client, ctx=ctx, pages=embeds, hidden=True)

client.run("Token")
