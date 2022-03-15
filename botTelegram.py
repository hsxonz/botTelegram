from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl import types, functions
from news3lion import getmessage
from datetime import datetime
import pytz
phone = '+84906227699'
api_id = '9367255'
api_hash = 'aaa48983d091c277b7297e17f880d41d'
# hc_private = 1280064017
# hc_channel_private = 1203964445
my_date = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
current_date_time = my_date.strftime("%Y-%m-%d-%H-%M")
current_date = my_date.strftime("%Y-%m-%d-15-30")  # %Y-%m-%d-%H-%M-%S
POST_NEW = True


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def getGroup():
    chats = []
    last_date = None
    chunk_size = 200

    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
    chats = [{'id': i.id, 'title': i.title} for i in chats]
    return list(chunks(chats, 100))


def sendMessage(client, chat_id, text):
    client.send_message(chat_id, text)


with TelegramClient(phone, api_id, api_hash) as client:

    print('Start')

    @client.on(events.NewMessage('me'))
    async def handler(event):
        if event.message.message == '/group':
            allGroup = await getGroup()
            for group in allGroup:
                reply = ''
                for chat in group:
                    reply += '{} - {}\n'.format(chat['id'], chat['title'])
                await event.reply(reply)
        if event.message.message == '/3lions':
            newsMain, image = getmessage()
            await client.send_file(1787057641, image, caption=newsMain)

    @client.on(events.NewMessage(chats=[+1676695636]))
    async def my_event_handler(event):
        result = await client(functions.messages.GetScheduledHistoryRequest(
            peer=1787057641,
            hash=0
        ))
        if current_date_time == current_date and len(result.messages) == 0:
            information = await getmessage()
            newsMain, image = information
            client.send_file(1787057641, image, caption=newsMain, schedule=datetime(
                my_date.year, my_date.month, my_date.day, 20, 8, 8, 8, pytz.timezone('Asia/Ho_Chi_Minh')))
            print('new line')

    # # chat hc private
    # @client.on(events.MessageEdited(chats=[+1280064017]))
    # async def my_event_handler(event):
    #     if event.message.pinned == True:
    #         await client.forward_messages(1604392119, event.message)
    #         print(event.message)

    # # channel hc private
    # @client.on(events.NewMessage(chats=[+1203964445]))
    # async def my_event_handler(event):
    #     await client.forward_messages(1604392119, event.message)
    #     print(event.message)

    # # chat hc group clone
    # @client.on(events.NewMessage(chats=[+1280064017]))
    # async def my_event_handler(event):
    #     await client.forward_messages(649054139, event.message)
    #     if event.message.chat.admin_rights:
    #         print(event.message.message)

    # @client.on(events.MessageEdited(chats=[+1203964445]))
    # async def my_event_handler(event):
    #     await client.forward_messages(1604392119, event.message)
    #     # print(event.message)

    client.run_until_disconnected()
