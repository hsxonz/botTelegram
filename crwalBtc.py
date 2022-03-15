import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import random
from googletrans import Translator
translator = Translator()
coinlive_url = "https://coinlive.me/category/crypto-news"
bitcoinnews_url = "https://news.bitcoin.com/"
# cointelegraph_url = "https://cointelegraph.com"
my_date = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
current_date = my_date.strftime(" %B %d, %Y")
current_time = my_date.strftime("%Y-%m-%d")
timePost = int(my_date.strftime("%H"))  # hours local vi


def getHtml(url):
    try:
        payload = ''
        headers = {
        }

        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=10)
        text = response.text
        return text
    except Exception as e:
        print(e)
        return None


def getImage(text):
    return text.find('img')['data-src']


def check_time_CoinLive(element):
    date = element.find(class_="jeg_meta_date").text
    if date == current_date:
        return True
    return False


def handleUrlCoinLive(text):
    news = []
    images = []
    soup = BeautifulSoup(text)
    block_news = soup.find_all(class_="jeg_post")
    for i in block_news:
        if check_time_CoinLive(i):
            try:
                caption = i.find('h3').text.replace("\n", '')
            except:
                caption = i.find('h2').text.replace("\n", '')
            link = i.find('a')['href']
            try:
                image = i.find('img').attrs['src']
                images.append(image)
            except Exception as e:
                pass
            news.append({caption: link})
    return images, news


def check_time_bitcoinnews(element):
    time = ''
    try:
        time = element.find(class_="story__footer").text
    except:
        time = element.find("h5").text
    if time.find('mins') != -1:
        return True
    elif time.find('hours') != -1:
        number = int(re.findall(r'\d+', time)[0])
        return number < timePost
    return False


def handle_bitcoinnews_url(text):
    news = []
    images = []
    soup = BeautifulSoup(text, "html.parser")
    block_news = soup.find_all(class_="story")
    for i in block_news:
        if check_time_bitcoinnews(i):
            try:
                image = i.find('img').attrs['src']
                images.append(image)
            except:
                pass

            link = i.find('a').attrs['href']

            try:
                caption = i.find('h6').text.replace("\n", '')
            except:
                caption = i.find('h5').text.replace("\n", '')

            news.append({caption: link})

    return images, news


# def check_time_cointelegraph(element):
#     time = element.find("time").text
#     if time.find('minutes') != -1:
#         return True
#     elif time.find('hours') != -1:
#         number = int(re.findall(r'\d+', time)[0])
#         return number < timePost
#     return False


# def handle_cointelegraph_url(text):
#     news = []
#     images = []
#     soup = BeautifulSoup(text, "html.parser")
#     block_news = soup.find(class_="post-card__article")
#     for i in block_news:
#         image = i.find('img').attrs['src']
#         images.append(image)
#         link = i.find('a').attrs['href']
#         caption = i.find('img').alt.replace("\n", '')
#         news.append({caption: link})
#     return images, news


def getNews(newsList):
    res = ''
    for i in newsList:
        for k, v in i.items():
            res += k + " ||| "
    return res


def getNewsListVi(newsList, captionVi):
    res = []
    for i in range(len(newsList)):
        for k, v in newsList[i].items():
            res.append({captionVi[i]: v})
    return res


def getInformation():

    text_bitcoinnews = getHtml(bitcoinnews_url)
    images_bitcoinnews, news_bitcoinnews = handle_bitcoinnews_url(
        text_bitcoinnews)
    text_coinlive = getHtml(coinlive_url)
    images_Coinlive, news_Coinlive = handleUrlCoinLive(text_coinlive)

    list_news = news_Coinlive + news_bitcoinnews
    list_images = images_Coinlive + images_bitcoinnews
    try:
        list_news = random.sample(list_news, 6)
    except:
        list_news = list_news
    try:
        image = random.sample(list_images, 1)[0]
    except:
        image = ''
    news = getNews(list_news)
    captionVi = translator.translate(news, dest='vi')
    captionList = captionVi.text.split("|||")[:-1]
    newListVi = getNewsListVi(list_news, captionList)
    return newListVi, image
