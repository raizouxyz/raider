import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def report(cache, user_id):
    request_data = {
        "version":"1.0",
        "variant":"1",
        "language":"en",
        "breadcrumbs":[13,8,7,9],
        "elements":{
            "user_profile_select":["photos"]
        },
        "name":"user",
        "user_id":user_id
    }
    response = requests.post(f'https://discord.com/api/v9/reporting/user', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(user_id):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=report, args=(cache, user_id)).start()
            time.sleep(_utils.config['delay'])
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    user_id = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='User ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=user_id, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(user_id.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'UserProfile Reporter',
    'description':'ユーザーのプロフィールを通報します'
}