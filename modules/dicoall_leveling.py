import time
import tkinter
import requests
import threading
import websocket
import playsound
from modules import _utils

module_status = False

def leveling(cache, guild_id, textchannel_id, voicechannel_id):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream", http_proxy_host=cache['proxy_detail']['host'], http_proxy_port=cache['proxy_detail']['port'], http_proxy_auth=(cache['proxy_detail']['username'], cache['proxy_detail']['password']))
    ws.send(f'{{"op":2,"d":{{"token":"{cache["login_information"]["token"]}","capabilities":16381,"properties":{{"os":"Windows","browser":"Chrome","device":"","system_locale":"ja","browser_user_agent":"{_utils.config["useragent"]}","browser_version":"{_utils.config["chrome_version"]}","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":{_utils.config["client_build_number"]},"client_event_source":null}},"presence":{{"status":"online","since":0,"activities":[],"afk":false}},"compress":false,"client_state":{{"guild_versions":{{}},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1,"private_channels_version":"0","api_code_version":0}}}}}}')
    ws.send(f'{{"op":4,"d":{{"guild_id":"{guild_id}","channel_id":"{voicechannel_id}","self_mute":false,"self_deaf":false,"self_video":false,"flags":2}}}}')
    request_data = {'content': _utils.random_string(15, 5), "tts": False, "flags":0, 'mobile_network_type': "unknown"}
    response = requests.post(f'https://discord.com/api/v9/channels/{textchannel_id}/messages', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(guild_id, textchannel_id, voicechannel_id):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=leveling, args=(cache, guild_id, textchannel_id, voicechannel_id)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    textchannel_id = tkinter.StringVar()
    voicechannel_id = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text=' TextChannel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=textchannel_id, width=50).pack()
    tkinter.Label(master=module_frame, text='VoiceChannel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=voicechannel_id, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),textchannel_id.get(),voicechannel_id.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Dicoall Leveling',
    'description':'Dicoallのランキングを上げます'
}