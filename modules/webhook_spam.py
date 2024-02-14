import time
import random
import tkinter
import requests
import threading
import playsound
from modules import _utils

module_status = False

def spam(webhook_url, content, username, avatar_url, convert):
    if convert:
        content = _utils.randomconvert(content)
    if avatar_url == None:
        avatar_url = f'https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png'
    request_data = {'content':content, 'username': username, 'avatar_url': avatar_url}
    response = requests.post(webhook_url, proxies=_utils.get_random_proxy(), json=request_data)
    print(response.status_code, response.text)

def start(webhook_url, content, username, avatar_url):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    while module_status:
        threading.Thread(target=spam, args=(webhook_url, content, username, avatar_url)).start()

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    webhook_url = tkinter.StringVar()
    content = tkinter.StringVar()
    username = tkinter.StringVar()
    avatar_url = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Webhook URL', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, width=50).pack()
    tkinter.Label(master=module_frame, text='Message', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, width=50).pack()
    tkinter.Label(master=module_frame, text='UserName', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, width=50).pack()
    tkinter.Label(master=module_frame, text='Avatar URL', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(webhook_url.get(),content.get(),username.get(),avatar_url.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Webhook Spammer',
    'description':'Webhookを送信します'
}