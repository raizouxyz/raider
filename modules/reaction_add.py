import time
import emoji
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def add(cache, channel_id, message_id, reaction):
    response = requests.put(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me?location=Message&type=0', headers=cache['headers'], proxies=cache['proxy'])
    print(response.status_code, response.text)

def start(channel_id, message_id, reaction):
    global module_status
    module_status = True

    reaction = emoji.emojize(reaction, language='alias')

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=add, args=(cache, channel_id, message_id, reaction)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    channel_id = tkinter.StringVar()
    message_id = tkinter.StringVar()
    reaction = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Message ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=message_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Reaction', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=reaction, width=10).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(channel_id.get(),message_id.get(),reaction.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Reaction Adder',
    'description':'リアクションを付けます'
}