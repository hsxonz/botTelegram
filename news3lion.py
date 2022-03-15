from telethon.sync import TelegramClient, events
from crwalBtc import getInformation
from datetime import datetime
import pytz

my_date = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
time = my_date.strftime("%d/%m/%Y")
text = '''
📰 BẢN TIN NGÀY {}
________________________
{}


#ThreeLionsCapital #News
____________________________
📊ThreeLionsCapital's Social Media 
[Website](https://3lions.capital/) | [Twitter](https://twitter.com/3lionsCapital) | [Channel](https://t.me/LionsCapital3)| [Offcial Chat](https://t.me/threelionscapital) |  [TikTok](https://www.tiktok.com/@3lionscapital) | [Youtube](https://www.youtube.com/channel/UCMh3YnJxXv-HxXwag71stEg)
'''


def contact(title, link):
    return '''{}{}'''


def newsMini(caption, link):
    return '''
📌{}
👉[Chi tiết]({})
    '''.format(caption, link)


def combinationNews(newsList):
    text = ''
    for i in newsList:
        for j in i.keys():
            text += newsMini(j, i[j])
    return text


def getmessage():
    newsList, image = getInformation()
    information = combinationNews(newsList)
    newsMain = text.format(time, information)
    return newsMain, image


