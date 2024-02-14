import time
import tkinter
import websocket
import threading
import playsound
from modules import _utils

module_status = False

def join(cache, guild_id, channel_id, video, mic_mute, speaker_mute, keep):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream", http_proxy_host=cache['proxy_detail']['host'], http_proxy_port=cache['proxy_detail']['port'], http_proxy_auth=(cache['proxy_detail']['username'], cache['proxy_detail']['password']))
    ws.send(f'{{"op":2,"d":{{"token":"{cache["login_information"]["token"]}","capabilities":16381,"properties":{{"os":"Windows","browser":"Chrome","device":"","system_locale":"ja","browser_user_agent":"{_utils.config["useragent"]}","browser_version":"{_utils.config["chrome_version"]}","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":{_utils.config["client_build_number"]},"client_event_source":null}},"presence":{{"status":"online","since":0,"activities":[],"afk":false}},"compress":false,"client_state":{{"guild_versions":{{}},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1,"private_channels_version":"0","api_code_version":0}}}}}}')
    ws.send(f'{{"op":4,"d":{{"guild_id":"{guild_id}","channel_id":"{channel_id}","self_mute":{mic_mute},"self_deaf":{speaker_mute},"self_video":{video},"flags":2}}}}'.replace('True','true').replace('False','false'))

def start(guild_id, channel_id, video, mic_mute, speaker_mute, keep):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=join, args=(cache, guild_id, channel_id, video, mic_mute, speaker_mute, keep)).start()
            if not keep:
                time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    channel_id = tkinter.StringVar()
    video = tkinter.BooleanVar()
    mic_mute = tkinter.BooleanVar()
    speaker_mute = tkinter.BooleanVar()
    keep = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='Server ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Voice Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='Camera', variable=video, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Checkbutton(master=module_frame, text='Mic Mute', variable=mic_mute, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Checkbutton(master=module_frame, text='Speaker Mute', variable=speaker_mute, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Checkbutton(master=module_frame, text='Keep Alive', variable=keep, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),channel_id.get(),video.get(),mic_mute.get(),speaker_mute.get(),keep.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'VC Joiner',
    'description':'ボイスチャットに入室します'
}