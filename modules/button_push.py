import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def push(cache, guild_id, channel_id, message_id, application_id, button_id):
    request_data = {
        "type":3,
        "guild_id":guild_id,
        "channel_id":channel_id,
        "message_flags":0,
        "message_id":message_id,
        "application_id":application_id,
        "session_id":_utils.random_string(32),
        "data":{
            "component_type":2,
            "custom_id":button_id
        }
    }
    response = requests.post('https://discord.com/api/v9/interactions', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(guild_id, channel_id, message_id, application_id, button_id):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=push, args=(cache, guild_id, channel_id, message_id, application_id, button_id)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    channel_id = tkinter.StringVar()
    message_id = tkinter.StringVar()
    application_id = tkinter.StringVar()
    button_id = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Message ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=message_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Application ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=application_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Button ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=button_id, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),channel_id.get(),message_id.get(),application_id.get(),button_id.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Button Pusher',
    'description':'ボタンを押します'
}