import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def send(cache, user_id, content, convert):
    request_data = {'recipients':[user_id]}
    response = requests.post('https://discord.com/api/v9/users/@me/channels', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)
    if response.status_code == 200:
        user_id = response.json()['recipients'][0]['id']
        channel_id = response.json()['id']
        content = _utils.replace_content(content)
        if convert:
            _utils.random_convert(content)
        request_data = {'content':content,"tts":False,"flags":0}
        response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
        print(response.status_code, response.text)

def start(user_id, content, convert):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=send, args=(cache, user_id, content, convert)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    user_id = tkinter.StringVar()
    content = tkinter.StringVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='User ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=user_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Message', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=content, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(user_id.get(),content.get(),convert.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'DM Spammer',
    'description':'DMを送ります'
}