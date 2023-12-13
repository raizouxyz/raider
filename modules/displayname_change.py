import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def change(cache, name, convert):
    name = _utils.replace_content(name)
    if convert:
        name = _utils.random_convert(name)
    request_data = {'global_name':name}
    response = requests.patch('https://discord.com/api/v9/users/@me', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(name, convert):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, name, convert)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    name = tkinter.StringVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='DisplayName', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=name, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(name.get(),convert.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'DisplayName Changer',
    'description':'表示名を変更します'
}