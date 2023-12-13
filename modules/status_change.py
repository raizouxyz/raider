import time
import emoji
import random
import tkinter
import requests
import websocket
import threading
from modules import _utils

module_status = False

def change(cache, status, custom_status, custom_status_emoji, spotify_track):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream", http_proxy_host=cache['proxy_detail']['host'], http_proxy_port=cache['proxy_detail']['port'], http_proxy_auth=(cache['proxy_detail']['username'], cache['proxy_detail']['password']))
    ws.send(f'{{"op":2,"d":{{"token":"{cache["login_information"]["token"]}","capabilities":16381,"properties":{{"os":"Windows","browser":"Chrome","device":"","system_locale":"ja","browser_user_agent":"{_utils.config["useragent"]}","browser_version":"{_utils.config["chrome_version"]}","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":{_utils.config["client_build_number"]},"client_event_source":null}},"presence":{{"status":"{status}","since":0,"activities":[],"afk":false}},"compress":false,"client_state":{{"guild_versions":{{}},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1,"private_channels_version":"0","api_code_version":0}}}}}}')
    if spotify_track != '':
        ws.send(spotify_track)
    elif custom_status != '':
        custom_status = custom_status.replace('<RANDOM>', _utils.random_string(10, 5))
        if custom_status_emoji == '':
            custom_status_emoji = 'null'
        else:
            custom_status_emoji = emoji.emojize(custom_status_emoji, language='alias')
            custom_status_emoji = f'{{"id":null,"name":"{custom_status_emoji}","animated":false}}'

def start(status, custom_status, custom_status_emoji, spotify_track_id):
    global module_status
    module_status = True

    status_list = ['online', 'idle', 'dnd', 'invisible']

    spotify_track = None
    if spotify_track_id != '':
        response = requests.get(f'https://api.spotify.com/v1/tracks/{spotify_track_id}', headers={'Authorization':f'Bearer {_utils.config["spotify"]["access_token"]}'})
        spotify_track = f'{{"op":3,"d":{{"status":"{status_list[status]}","since":0,"activities":[{{"type":2,"name":"Spotify","assets":{{"large_image":"spotify:{_utils.remove_string(response.json()["album"]["images"][0]["url"], "https://i.scdn.co/image/")}","large_text":"{response.json()["album"]["name"]}"}},"details":"{response.json()["name"]}","state":"{response.json()["artists"][0]["name"]}","timestamps":{{"start":{time.time()*1000},"end":{time.time()*1000+response.json()["duration_ms"]}}},"party":{{"id":"spotify:{random.randint(1000000000000000000, 2000000000000000000)}"}},"sync_id":"{_utils.random_string(22)}","flags":48,"metadata":{{"context_uri":"spotify:album:{response.json()["album"]["id"]}","album_id":"{response.json()["album"]["id"]}","artist_ids":["{response.json()["artists"][0]["id"]}"]}}}}],"afk":false}}}}'

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache,status_list[status],custom_status,custom_status_emoji,spotify_track)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    status = tkinter.IntVar()
    custom_status = tkinter.StringVar()
    custom_status_emoji = tkinter.StringVar()
    spotify_track_id = tkinter.StringVar()

    tkinter.Radiobutton(module_frame, value=0, variable=status, text='オンライン', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Radiobutton(module_frame, value=1, variable=status, text='退席中', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Radiobutton(module_frame, value=2, variable=status, text='取り込み中', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Radiobutton(module_frame, value=3, variable=status, text='オンライン状態を隠す', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Label(master=module_frame, text='Spotify Track ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(module_frame, width=50, textvariable=spotify_track_id).pack()
    tkinter.Label(master=module_frame, text='Custom Status', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(module_frame, width=50, textvariable=custom_status).pack()
    tkinter.Label(master=module_frame, text='Custom Status Emoji', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(module_frame, width=10, textvariable=custom_status_emoji).pack()
    tkinter.Button(master=module_frame, text='Start', foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(status.get(),custom_status.get(),custom_status_emoji.get(),spotify_track_id.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Status Changer',
    'description':'ステータスを変更します'
}