import discord
import aiohttp

async def pubg(nick, platform, match):

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://yhs.kr/api/PUBG/player?nickname={nick}&platform={platform}") as link:
            if link.status == 200:
                info = await link.json()
                update = info["lastupdate"]

                if "id" in info:
                    id = info["id"]

                    if platform == 0:
                        platform = "Steam"
                    elif platform == 1:
                        platform = "Kakao"
                    elif platform == 2:
                        platform = "XBox"
                    elif platform == 3:
                        platform = "PlayStation"
                    elif platform == 4:
                        platform = "Stadia"

                    if match == "normal":
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://yhs.kr/api/PUBG/{match}?id={id}") as link:
                                if link.status == 200:
                                    info = await link.json()

                                    if "id" in info:

                                        match = "일반전"

                                        infosolo = info["gameMode"]["solo"]
                                        infosolofpp = info["gameMode"]["solo-fpp"]
                                        infoduo = info["gameMode"]["duo"]
                                        infoduofpp = info["gameMode"]["duo-fpp"]
                                        infosquad = info["gameMode"]["squad"]
                                        infosquadfpp = info["gameMode"]["squad-fpp"]

                                        embed1 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 솔로 [TPP])", color=0xf5ab00)
                                        embed2 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 솔로 [FPP])", color=0xf5ab00)
                                        embed3 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 듀오 [TPP])", color=0xf5ab00)
                                        embed4 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 듀오 [FPP])", color=0xf5ab00)
                                        embed5 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 스쿼드 [TPP])", color=0xf5ab00)
                                        embed6 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 스쿼드 [FPP])", color=0xf5ab00)

                                        embed1.add_field(name="닉네임", value=nick)
                                        embed1.add_field(name="플레이 횟수", value=infosolo["roundsPlayed"])
                                        embed1.add_field(name="킬 횟수", value=str(infosolo["kills"]) + "\n평균: " + str(infosolo["roundMostKills"]))
                                        embed1.add_field(name="평균 피해량", value=infosolo["damageDealt"])
                                        embed1.add_field(name="사망 횟수", value=infosolo["losses"])
                                        embed1.add_field(name="도움 횟수", value=infosolo["assists"])
                                        embed1.add_field(name="K/D", value=infosolo["KD_point"])
                                        embed1.add_field(name="우승 횟수", value=infosolo["wins"])
                                        embed1.add_field(name="Top10 횟수", value=infosolo["top10s"])

                                        embed2.add_field(name="닉네임", value=nick)
                                        embed2.add_field(name="플레이 횟수", value=infosolofpp["roundsPlayed"])
                                        embed2.add_field(name="킬 횟수", value=str(infosolofpp["kills"]) + "\n평균: " + str(infosolo["roundMostKills"]))
                                        embed2.add_field(name="평균 피해량", value=infosolofpp["damageDealt"])
                                        embed2.add_field(name="사망 횟수", value=infosolofpp["losses"])
                                        embed2.add_field(name="도움 횟수", value=infosolofpp["assists"])
                                        embed2.add_field(name="K/D", value=infosolofpp["KD_point"])
                                        embed2.add_field(name="우승 횟수", value=infosolofpp["wins"])
                                        embed2.add_field(name="Top10 횟수", value=infosolofpp["top10s"])

                                        embed3.add_field(name="닉네임", value=nick)
                                        embed3.add_field(name="플레이 횟수", value=infoduo["roundsPlayed"])
                                        embed3.add_field(name="킬 횟수", value=str(infoduo["kills"]) + "\n평균: " + str(infosolo["roundMostKills"]))
                                        embed3.add_field(name="평균 피해량", value=infoduo["damageDealt"])
                                        embed3.add_field(name="사망 횟수", value=infoduo["losses"])
                                        embed3.add_field(name="도움 횟수", value=infoduo["assists"])
                                        embed3.add_field(name="K/D", value=infoduo["KD_point"])
                                        embed3.add_field(name="우승 횟수", value=infoduo["wins"])
                                        embed3.add_field(name="Top10 횟수", value=infoduo["top10s"])

                                        embed4.add_field(name="닉네임", value=nick)
                                        embed4.add_field(name="플레이 횟수", value=infoduofpp["roundsPlayed"])
                                        embed4.add_field(name="킬 횟수", value=str(infoduofpp["kills"]) + "\n평균: " + str(infosolo["roundMostKills"]))
                                        embed4.add_field(name="평균 피해량", value=infoduofpp["damageDealt"])
                                        embed4.add_field(name="사망 횟수", value=infoduofpp["losses"])
                                        embed4.add_field(name="도움 횟수", value=infoduofpp["assists"])
                                        embed4.add_field(name="K/D", value=infoduofpp["KD_point"])
                                        embed4.add_field(name="우승 횟수", value=infoduofpp["wins"])
                                        embed4.add_field(name="Top10 횟수", value=infoduofpp["top10s"])

                                        embed5.add_field(name="닉네임", value=nick)
                                        embed5.add_field(name="플레이 횟수", value=infosquad["roundsPlayed"])
                                        embed5.add_field(name="킬 횟수", value=str(infosquad["kills"]) + "\n평균: " + str(infosolo["roundMostKills"]))
                                        embed5.add_field(name="평균 피해량", value=infosquad["damageDealt"])
                                        embed5.add_field(name="사망 횟수", value=infosquad["losses"])
                                        embed5.add_field(name="도움 횟수", value=infosquad["assists"])
                                        embed5.add_field(name="K/D", value=infosquad["KD_point"])
                                        embed5.add_field(name="우승 횟수", value=infosquad["wins"])
                                        embed5.add_field(name="Top10 횟수", value=infosquad["top10s"])

                                        embed6.add_field(name="닉네임", value=nick)
                                        embed6.add_field(name="플레이 횟수", value=infosquadfpp["roundsPlayed"])
                                        embed6.add_field(name="킬 횟수", value=str(infosquadfpp["kills"]) + "\n평균: " + str(infosolo["roundMostKills"]))
                                        embed6.add_field(name="평균 피해량", value=infosquadfpp["damageDealt"])
                                        embed6.add_field(name="사망 횟수", value=infosquadfpp["losses"])
                                        embed6.add_field(name="도움 횟수", value=infosquadfpp["assists"])
                                        embed6.add_field(name="K/D", value=infosquadfpp["KD_point"])
                                        embed6.add_field(name="우승 횟수", value=infosquadfpp["wins"])
                                        embed6.add_field(name="Top10 횟수", value=infosquadfpp["top10s"])

                                        embed1.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed2.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed3.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed4.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed5.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed6.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")

                                        embed1.set_footer(text=f"(전적 업데이트: {update['normal']['hours']}시 {update['normal']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed2.set_footer(text=f"(전적 업데이트: {update['normal']['hours']}시 {update['normal']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed3.set_footer(text=f"(전적 업데이트: {update['normal']['hours']}시 {update['normal']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed4.set_footer(text=f"(전적 업데이트: {update['normal']['hours']}시 {update['normal']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed5.set_footer(text=f"(전적 업데이트: {update['normal']['hours']}시 {update['normal']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed6.set_footer(text=f"(전적 업데이트: {update['normal']['hours']}시 {update['normal']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        
                                        return [embed1, embed2, embed3, embed4, embed5, embed6]
                        
                                    else:
                                        return discord.Embed(title=f"유저를 찾을 수 없습니다.", color=0xff0000)

                                else:
                                    return discord.Embed(title=f"Error Code: {link.status}", color=0xff0000)
                    else:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://yhs.kr/api/PUBG/{match}?id={id}") as link:
                                if link.status == 200:
                                    info = await link.json()

                                    if "id" in info:

                                        match = "경쟁전"

                                        infosolo = info["gameMode"]["solo"]
                                        infosolofpp = info["gameMode"]["solo-fpp"]
                                        infosquad = info["gameMode"]["squad"]
                                        infosquadfpp = info["gameMode"]["squad-fpp"]

                                        try:
                                            infosolo["roundsPlayed"]
                                        except KeyError:
                                            infosolo["roundsPlayed"] = 0
                                        
                                        try:
                                            infosolofpp["roundsPlayed"]
                                        except KeyError:
                                            infosolofpp["roundsPlayed"] = 0

                                        try:
                                            infosquad["roundsPlayed"]
                                        except KeyError:
                                            infosquad["roundsPlayed"] = 0

                                        try:
                                            infosquadfpp["roundsPlayed"]
                                        except KeyError:
                                            infosquadfpp["roundsPlayed"] = 0

                                        embed1 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 솔로 [TPP])", color=0xf5ab00)
                                        embed2 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 솔로 [FPP])", color=0xf5ab00)
                                        embed5 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 스쿼드 [TPP])", color=0xf5ab00)
                                        embed6 = discord.Embed(title=f"[{platform}] 배틀그라운드 유저 정보", description=f"{nick}님의 정보 ({match} 스쿼드 [FPP])", color=0xf5ab00)
                                        
                                        embed1.add_field(name="닉네임", value=nick)
                                        embed1.add_field(name="플레이 횟수", value=infosolo["roundsPlayed"])
                                        embed1.add_field(name="랭크", value=infosolo["currentRankAnswer"])
                                        embed1.add_field(name="랭크 점수", value=infosolo["currentRankPoint"])
                                        embed1.add_field(name="킬 횟수", value=infosolo["kills"])
                                        embed1.add_field(name="사망 횟수", value=infosolo["deaths"])
                                        embed1.add_field(name="도움 횟수", value=infosolo["assists"])
                                        embed1.add_field(name="K/D", value=infosolo["KD_point"])
                                        embed1.add_field(name="우승 횟수", value=infosolo["wins"])
                                        embed1.add_field(name="승률", value=str(infosolo["win_point"]) + "%")
                                        embed1.add_field(name="Top10 횟수", value=infosolo["top10s"])

                                        embed2.add_field(name="닉네임", value=nick)
                                        embed2.add_field(name="플레이 횟수", value=infosolofpp["roundsPlayed"])
                                        embed2.add_field(name="랭크", value=infosolofpp["currentRankAnswer"])
                                        embed2.add_field(name="랭크 점수", value=infosolofpp["currentRankPoint"])
                                        embed2.add_field(name="킬 횟수", value=infosolofpp["kills"])
                                        embed2.add_field(name="사망 횟수", value=infosolofpp["deaths"])
                                        embed2.add_field(name="도움 횟수", value=infosolofpp["assists"])
                                        embed2.add_field(name="K/D", value=infosolofpp["KD_point"])
                                        embed2.add_field(name="우승 횟수", value=infosolofpp["wins"])
                                        embed2.add_field(name="승률", value=str(infosolofpp["win_point"]) + "%")
                                        embed2.add_field(name="Top10횟수", value=infosolofpp["top10s"])

                                        embed5.add_field(name="닉네임", value=nick)
                                        embed5.add_field(name="플레이 횟수", value=infosquad["roundsPlayed"])
                                        embed5.add_field(name="랭크", value=infosquad["currentRankAnswer"])
                                        embed5.add_field(name="랭크 점수", value=infosquad["currentRankPoint"])
                                        embed5.add_field(name="킬 횟수", value=infosquad["kills"])
                                        embed5.add_field(name="사망 횟수", value=infosquad["deaths"])
                                        embed5.add_field(name="도움 횟수", value=infosquad["assists"])
                                        embed5.add_field(name="K/D", value=infosquad["KD_point"])
                                        embed5.add_field(name="우승 횟수", value=infosquad["wins"])
                                        embed5.add_field(name="승률", value=str(infosquad["win_point"]) + "%")
                                        embed5.add_field(name="Top10 횟수", value=infosquad["top10s"])

                                        embed6.add_field(name="닉네임", value=nick)
                                        embed6.add_field(name="플레이 횟수", value=infosquadfpp["roundsPlayed"])
                                        embed6.add_field(name="랭크", value=infosquadfpp["currentRankAnswer"])
                                        embed6.add_field(name="랭크 점수", value=infosquadfpp["currentRankPoint"])
                                        embed6.add_field(name="킬 횟수", value=infosquadfpp["kills"])
                                        embed6.add_field(name="사망 횟수", value=infosquadfpp["deaths"])
                                        embed6.add_field(name="도움 횟수", value=infosquadfpp["assists"])
                                        embed6.add_field(name="K/D", value=infosquadfpp["KD_point"])
                                        embed6.add_field(name="우승 횟수", value=infosquadfpp["wins"])
                                        embed6.add_field(name="승률", value=str(infosquadfpp["win_point"]) + "%")
                                        embed6.add_field(name="Top10 횟수", value=infosquadfpp["top10s"])

                                        embed1.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed2.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed5.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")
                                        embed6.set_thumbnail(url="https://lh3.googleusercontent.com/a4u1SAoo7ytp02FtcCwXvSuW3qJoFEraO2PoeObmOt4x3pAHn1FFIRHWQ2Cfkipd-ck")

                                        embed1.set_footer(text=f"(전적 업데이트: {update['ranked']['hours']}시 {update['ranked']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed2.set_footer(text=f"(전적 업데이트: {update['ranked']['hours']}시 {update['ranked']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed5.set_footer(text=f"(전적 업데이트: {update['ranked']['hours']}시 {update['ranked']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        embed6.set_footer(text=f"(전적 업데이트: {update['ranked']['hours']}시 {update['ranked']['minutes']}분)\nPUBG Open-API를 사용합니다.",icon_url="https://img.icons8.com/color/452/pubg.png")
                                        
                                        return [embed1, embed2, embed5, embed6]
                        
                                    else:
                                        return discord.Embed(title=f"유저를 찾을 수 없습니다.", color=0xff0000)

                                else:
                                    return discord.Embed(title=f"Error Code: {link.status}", color=0xff0000)

                else:
                    return discord.Embed(title=f"유저를 찾을 수 없습니다.", color=0xff0000)

            else:
                return discord.Embed(title=f"Error Code: {link.status}", color=0xff0000)
