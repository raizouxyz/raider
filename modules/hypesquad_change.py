import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def change(cache, house_id):
    request_data = {'house_id':house_id}
    response = requests.post('https://discord.com/api/v9/hypesquad/online', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(house):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, house)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    house = tkinter.IntVar()

    tkinter.Label(master=module_frame, text='HypeSquad ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Radiobutton(module_frame, value=1, variable=house, text='Bravery', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Radiobutton(module_frame, value=2, variable=house, text='Brilliance', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Radiobutton(module_frame, value=3, variable=house, text='Balance', foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(house.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'HypeSquad Changer',
    'description':'HypeSquadを変更します'
}