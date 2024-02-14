import time
import tkinter
import requests
import threading
import playsound
from modules import _utils

module_status = False

def change(cache, bio, convert):
    bio = _utils.replace_content(bio)
    if convert:
        bio = _utils.random_convert(bio)
    request_data = {'bio':bio}
    response = requests.patch('https://discord.com/api/v9/users/@me/profile', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(bio, convert):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, bio, convert)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    bio = tkinter.StringVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='Bio', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, width=50, textvariable=bio).pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(bio.get(),convert.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Bio Changer',
    'description':'自己紹介文を変更します'
}