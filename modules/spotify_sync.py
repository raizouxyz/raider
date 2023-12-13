import time
import random
import tkinter
import requests
import threading
from modules import _utils
from tkinter import messagebox

module_status = False
now_lyric = None
sent_eighth_note =False

def spam(cache, channel_list, convert):
    global now_lyric, sent_eighth_note
    if now_lyric != None and not sent_eighth_note:
        if now_lyric == '♪':
            sent_eighth_note = True
        content = now_lyric
        if convert:
            content = _utils.random_convert(content)
        channel_id = random.choice(channel_list)
        request_data = {'content':content,"tts":False,"flags":0}
        response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
        print(response.status_code, response.text)

def update_lyrics():
    global now_lyric, sent_eighth_note, module_status
    while module_status:
        now_lyric = None
        response = requests.get('https://api.spotify.com/v1/me/player', headers={'Authorization':f'Bearer {_utils.config["spotify"]["access_token"]}'})
        print(response.status_code, response.text)
        if response.status_code == 200:
            track_id = response.json()['item']['id']
            print(f'Playing {response.json()["item"]["name"]}({track_id})')
            lyrics = requests.get(f'https://spotify-lyric-api-984e7b4face0.herokuapp.com/?trackid={track_id}').json()
            print(response.status_code, response.text)
            if not lyrics['error']:
                sync_start_ms = int(response.json()['progress_ms'])
                listen_start_unixtime = time.time() - response.json()['progress_ms']/1000
                if sync_start_ms/1000 < int(lyrics['lines'][0]['startTimeMs'])/1000:
                    time.sleep(int(lyrics['lines'][0]['startTimeMs'])/1000-sync_start_ms/1000)
                line_number_next = 1
                for line in lyrics['lines']:
                    sent_eighth_note = False
                    now_lyric = line['words']
                    while float(line['startTimeMs']) < (time.time()-listen_start_unixtime)*1000 and float(lyrics['lines'][line_number_next]['startTimeMs']) > (time.time()-listen_start_unixtime)*1000:
                        time.sleep(((float(lyrics['lines'][line_number_next]['startTimeMs']) - (time.time()-listen_start_unixtime)*1000)/1000))
                    line_number_next += 1
                    response = requests.get('https://api.spotify.com/v1/me/player', headers={'Authorization':f'Bearer {_utils.config["spotify"]["access_token"]}'})
                    if len(lyrics['lines']) <= line_number_next or track_id != response.json()['item']['id']:
                        break
            else:
                print('歌詞が無い曲を再生中です')
        if response.status_code == 403:
            messagebox.showerror(title='Error', message='Spotify Tokenを再生成してください')
            break
        time.sleep(2)

def start(guild_id, channel_id, all_channels, convert):
    global module_status
    module_status = True

    channel_list = []

    if all_channels:
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=_utils.caches[0]['headers'], proxies=_utils.caches[0]['proxy'])
        print(response.status_code, response.text)
        for channel in response.json():
            if channel['type'] == 0:
                channel_list.append(channel['id'])
    else:
        channel_list = channel_id.split(',')

    while module_status:
        threading.Thread(target=spam, args=(_utils.get_random_cache(), channel_list, convert)).start()
        time.sleep(_utils.config['delay'])

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    channel_id = tkinter.StringVar()
    all_channels = tkinter.BooleanVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='All Channels', variable=all_channels, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', foreground='#ffffff', background='#2c2f33', command=lambda:[threading.Thread(target=start, args=(guild_id.get(),channel_id.get(),all_channels.get(),convert.get())).start(), threading.Thread(target=update_lyrics).start()]).pack()
    tkinter.Button(master=module_frame, text='Stop', foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Spotify Sync Spammer',
    'description':'Spotifyで再生している曲と同期して歌詞をスパムします'
}