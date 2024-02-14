import time
import copy
import base64
import tkinter
import requests
import threading
import playsound
from modules import _utils

module_status = False

def request(cache, username):
    request_data = None
    if '#' in username:
        username = username.split('#')
        request_data = {"username":username[0],"discriminator":username[1]}
    else:
        request_data = {"username":username,"discriminator":None}
    headers = copy.deepcopy(cache['headers'])
    properties = '{"location":"Add Friend"}'
    headers['X-Context-Properties'] = base64.b64encode(properties.encode()).decode()
    response = requests.post('https://discord.com/api/v9/users/@me/relationships', headers=headers, proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(username):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=request, args=(cache, username)).start()
            time.sleep(_utils.config['delay'])

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    username = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='UserName', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=username, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(username.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Friend Requester',
    'description':'フレンドリクエストを送信します'
}