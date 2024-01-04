import time
import tkinter
import requests
import threading
from modules import _utils
from tkinter import colorchooser

module_status = False
accent_color = '0'

def change(cache):
    request_data = {'accent_color':accent_color}
    response = requests.patch('https://discord.com/api/v9/users/@me/profile', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def choose_color():
    global accent_color
    accent_color = colorchooser.askcolor()
    if accent_color == None:
        accent_color = 0
    else:
        accent_color = accent_color[1].replace('#', '0x')

def start():
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, accent_color)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    tkinter.Button(master=module_frame, text='Choose Color', width=20, foreground='#ffffff', background='#2c2f33', command=choose_color).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'BannerColor Changer',
    'description':'バナーカラーを変更します'
}