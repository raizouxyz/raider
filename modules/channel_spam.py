import sys
import json
import time
import base64
import random
import tkinter
import requests
import websocket
import threading
import playsound
from modules import _utils
from tkinter import messagebox

module_status = False

def spam(cache, guild_id, channel_list, content, reply_message_id, typing, convert, mention_members):
    channel_id = random.choice(channel_list)
    content = _utils.replace_content(content, mention_members)
    if convert:
        content = _utils.random_convert(content)
    request_data = {'content': content, "tts": False, "flags": 0, 'mobile_network_type': "unknown"}
    if reply_message_id != '':
        request_data['message_reference'] = {'guild_id':guild_id,'channel_id':channel_id,'message_id':reply_message_id}
    if typing:
        response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/typing', headers=cache['headers'], proxies=cache['proxy'])
        print(response.status_code, response.text)
    response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(guild_id, channel_id, content, reply_message_id, all_channels, typing, convert):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    channel_list = []
    if all_channels:
        if guild_id != '':
            response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=_utils.caches[0]['headers'], proxies=_utils.caches[0]['proxy'])
            print(response.status_code, response.text)
            for channel in response.json():
                if channel['type'] == 0:
                    channel_list.append(channel['id'])
        else:
            messagebox.showerror('Error', message='All Channelsを使用する場合\nGuild IDを指定してください')
    else:
        channel_list = channel_id.split(',')

    if reply_message_id != '':
        if len(channel_list) > 1 or all_channels:
            messagebox.showerror('Error', message='Reply Message IDを指定している場合、\n複数個のチャンネルにスパムを行うことはできません')
            return
    
    mention_members = ['']
    if '<RANDOM_MENTION>' in content:
        if guild_id != '' and channel_id != '':
            cache = _utils.get_random_cache()

            ranges = {
                1:'[0,99],[100,199]',
                2:'[0,99],[100,199],[200,299]',
                3:'[0,99],[200,299],[300,399]',
                4:'[0,99],[300,399],[400,499]',
                5:'[0,99],[400,499],[500,599]',
                6:'[0,99],[500,599],[600,699]',
                7:'[0,99],[600,699],[700,799]',
                8:'[0,99],[700,799],[800,899]',
                9:'[0,99],[800,899],[900,999]'
            }

            def on_open(ws):
                print(cache["login_information"]["token"])
                ws.send(f'{{"op":2,"d":{{"token":"{cache["login_information"]["token"]}","capabilities":16381,"properties":{{"os":"Windows","browser":"Chrome","device":"","system_locale":"ja","browser_user_agent":"{_utils.config["useragent"]}","browser_version":"{_utils.config["chrome_version"]}","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":{_utils.config["client_build_number"]},"client_event_source":null}},"presence":{{"status":"online","since":0,"activities":[],"afk":false}},"compress":false,"client_state":{{"guild_versions":{{}},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1,"private_channels_version":"0","api_code_version":0}}}}}}')
                ws.send(f'{{"op":14,"d":{{"guild_id":"{guild_id}","channels":{{"{channel_id}":[[0,99]]}}}}}}')

            def on_message(ws, msg):
                global mention_members
                msg = json.loads(msg)
                if msg['t'] == 'GUILD_MEMBER_LIST_UPDATE':
                    for member in msg['d']['ops'][0]['items']:
                        if 'member' in member.keys():
                            mention_members.append(f'<@{member["member"]["user"]["id"]}>')
                            print(f'<@{member["member"]["user"]["id"]}>')
                    member_count = msg['d']['member_count']
                    online_count = msg['d']['online_count']
                    if msg['d']['ops'][0]['range'] == [0,99]:
                        if member_count >= 100 and member_count < 1000:
                            for i in range(member_count/100):
                                ws.send(f'{{"op":14,"d":{{"guild_id":"{guild_id}","channels":{{"{channel_id}":[{ranges[i]}]}}}}}}')
                        elif online_count >= 100:
                            for i in range(online_count/100):
                                ws.send(f'{{"op":14,"d":{{"guild_id":"{guild_id}","channels":{{"{channel_id}":[{ranges[i]}]}}}}}}')
                        else:
                            ws.close()
                    else:
                        if member_count < 1000:
                            if msg['d']['ops'][0]['range'] == [int(member_count/100)*100,int(member_count/100)*100+99]:
                                ws.close()
                        else:
                            if msg['d']['ops'][0]['range'] == [int(online_count/100)*100,int(online_count/100)*100+99]:
                                ws.close()

            ws = websocket.WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9", on_open=on_open, on_message=on_message)
            ws.run_forever()
        else:
            messagebox.showerror('Error', message='ランダムメンション機能を使用する場合、\nGuild IDとChannel IDを指定してください')
        if mention_members == ['']:
            messagebox.showerror('Error', message='メンバーリストの取得に失敗しました')
            return

    while module_status:
        threading.Thread(target=spam, args=(_utils.get_random_cache(), guild_id, channel_list, content, reply_message_id, typing, convert, mention_members)).start()
        time.sleep(_utils.config['delay'])

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    channel_id = tkinter.StringVar()
    content = tkinter.StringVar()
    reply_message_id = tkinter.StringVar()
    all_channels = tkinter.BooleanVar()
    typing = tkinter.BooleanVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Text', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=content, width=50).pack()
    tkinter.Label(master=module_frame, text='Reply Message ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=reply_message_id, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='All Channels', variable=all_channels, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Checkbutton(master=module_frame, text='Typing', variable=typing, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(), channel_id.get(), content.get(), reply_message_id.get(), all_channels.get(), typing.get(), convert.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Channel Spammer',
    'description':'テキストチャンネルにスパムします'
}