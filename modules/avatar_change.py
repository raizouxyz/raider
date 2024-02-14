import time
import base64
import tkinter
import requests
import threading
import playsound
import tkinter.filedialog
from modules import _utils

module_status = False
filename = None

def change(cache, avatar):
    request_data = {'avatar':avatar}
    response = requests.patch('https://discord.com/api/v9/users/@me', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def openfile():
    global filename
    filename = tkinter.filedialog.askopenfilename(filetypes=[('Image File','*.jpg;*.jpeg;*.png;*.gif;')])

def start(filename):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    with open(filename, mode='rb') as f:
        avatar = f'data:image/png;base64,{base64.b64encode(f.read()).decode("utf-8")}'

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=change, args=(cache, avatar)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    global filename

    tkinter.Button(master=module_frame, text='Avatar Image File', width=20, foreground='#ffffff', background='#2c2f33', command=openfile).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(filename,)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Avatar Changer',
    'description':'アバターを変更します'
}