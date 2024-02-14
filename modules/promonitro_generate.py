import uuid
import tkinter
import requests
import threading
import playsound
import tkinter.filedialog
from modules import _utils

module_status = False

def start():
    global module_status
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    with open('./data/promonitro.txt', mode='a') as f:
        while module_status:
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Origin": "https://www.opera.com",
                "Referer": "https://www.opera.com/",
                "Sec-Ch-Ua": '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
            }
            response = requests.post('https://api.discord.gx.games/v1/direct-fulfillment', json={"partnerUserId": str(uuid.uuid4())}, headers=headers)
            f.write(f'https://discord.com/billing/partner-promotions/1180231712274387115/{response.json()["token"]}\n')
            print(f'https://discord.com/billing/partner-promotions/1180231712274387115/{response.json()["token"]}')
        
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Promotion Nitro Generator',
    'description':'プロモニトロを生成します'
}