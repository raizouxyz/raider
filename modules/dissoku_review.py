import time
import tkinter
import requests
import threading
import playsound
import urllib.parse
from modules import _utils

module_status = False

def post(cache, guild_id, message, score, like, convert):
    message = _utils.replace_content(message)
    if convert:
        message = _utils.random_convert(message)
    request_data = {"permissions":"0","authorize":True}
    response = requests.post('https://discord.com/api/v9/oauth2/authorize?client_id=761562078095867916&response_type=code&redirect_uri=https%3A%2F%2Fdissoku.net%2Faccounts%2Fdiscord%2Flogin%2Fcallback&scope=identify%20guilds', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.status_code)
    code = urllib.parse.parse_qs(urllib.parse.urlparse(response.json()['location']).query)['code'][0]
    response = requests.get(response.json()['location'], proxies=cache['proxy'])
    print(response.status_code, response.status_code)
    request_data = {"code":code}
    response = requests.post('https://app.dissoku.net/api/rest-auth/discord/', proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.status_code)
    dissoku_token = f'JWT {response.json()["access"]}'
    headers = {'Authorization': dissoku_token}
    if like:
        response = requests.post(f'https://app.dissoku.net/api/guilds/{guild_id}/like/', headers=headers, proxies=cache['proxy'])
        print(response.status_code, response.status_code)
    request_data = {"guild":guild_id,"message":message,"score":score}
    response = requests.post('https://app.dissoku.net/api/guildreviews/', headers=headers, proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(guild_id, message, score, like, convert):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=post, args=(cache, guild_id, message, score, like, convert)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    message = tkinter.StringVar()
    score = tkinter.IntVar()
    like = tkinter.BooleanVar()
    convert = tkinter.BooleanVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Message', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=message, width=50).pack()
    tkinter.Checkbutton(master=module_frame, text='Random Convert', variable=convert, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Label(master=module_frame, text='Score', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Scale(master=module_frame, variable=score, from_=1, to=5, length=150, orient=tkinter.HORIZONTAL, foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Checkbutton(master=module_frame, text='Like', variable=like, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),message.get(),score.get(),like.get(),convert.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Dissoku Review Spammer',
    'description':'Dissokuのレビューにスパムします'
}