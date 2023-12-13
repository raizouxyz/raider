import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def change(cache, pronouns, convert):
    pronouns = _utils.replace_content(pronouns)
    if convert:
        pronouns = _utils.random_convert(pronouns)
    request_data = {'pronouns':pronouns}
    response = requests.patch('https://discord.com/api/v9/users/@me/profile', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(pronouns, convert):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, pronouns, convert)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    pronouns = tkinter.StringVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='Pronouns', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=pronouns, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(pronouns.get(),convert.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Pronouns Changer',
    'description':'代名詞を変更します'
}