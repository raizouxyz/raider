import time
import tkinter
import requests
import threading
import playsound
from modules import _utils

module_status = False

def boost(cache, guild_id):
    response = requests.get('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', headers=cache['headers'], proxies=cache['proxy'])
    print(response.status_code, response.text)
    if len(response.json()) != 0:
        for subscription in response.json():
            if subscription['premium_guild_subscription'] == None:
                slot_id = subscription['id']
                request_data = {'user_premium_guild_subscription_slot_ids':[slot_id]}
                response = requests.put(f'https://discord.com/api/v9/guilds/{guild_id}/premium/subscriptions', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
                print(response.status_code, response.text)

def start(guild_id):
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=boost, args=(cache, guild_id)).start()
            time.sleep(_utils.config['delay'])
        else:
            break
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Server ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Guild Booster',
    'description':'サーバーをブーストします'
}