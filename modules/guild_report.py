import time
import tkinter
import requests
import threading
import playsound
from modules import _utils

module_status = False

def report(cache, guild_id):
    request_data = {
        "version":"1.0",
        "variant":"1",
        "language":"en",
        "breadcrumbs":[0,31],
        "elements":{},
        "name":"message",
        "guild_id":guild_id,
    }
    response = requests.post(f'https://discord.com/api/v9/reporting/guild', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(guild_id):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=report, args=(cache, guild_id)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Guild Reporter',
    'description':'サーバーを通報します'
}