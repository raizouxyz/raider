import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def change(cache, bannercolor):
    request_data = {'accent_color':bannercolor}
    response = requests.patch('https://discord.com/api/v9/users/@me/profile', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(bannercolor):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, bannercolor)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    bannercolor = tkinter.StringVar()
    
    tkinter.Label(master=module_frame, text='BannerColor', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=bannercolor, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(bannercolor.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'BannerColor Changer',
    'description':'バナーカラーを変更します'
}