import time
import copy
import tkinter
import requests
import threading
from modules import _utils
from urllib.parse import urlparse

module_status = False

def add(cache, url_query):
    request_data = {"name":_utils.random_string(10),"icon":None,"channels":[],"system_channel_id":None,"guild_template_code":"2TffvPucqHkN"}
    response = requests.post('https://discord.com/api/v9/guilds', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)
    if response.status_code == 201:
        request_data = {'guild_id': response.json()['id'], 'permissions': '0', 'authorize': True, 'integration_type': 0}
        headers = copy.deepcopy(cache['headers'])
        response = requests.post(f'https://discord.com/api/v9/oauth2/authorize?{url_query}', headers=headers, proxies=cache['proxy'], json=request_data)
        print(response.status_code, response.text)
        if response.status_code == 400:
            captcha_sitekey = response.json()['captcha_sitekey']
            captcha_result = _utils.solve_captcha(captcha_sitekey, 'https://discord.com/', headers['User-Agent'])
            if captcha_result:
                headers['X-Captcha-Key'] = captcha_result
                response = requests.post(f'https://discord.com/api/v9/oauth2/authorize?{url_query}', headers=headers, proxies=cache['proxy'], json=request_data)
                print(response.status_code, response.text)
            else:
                return

def start(url):
    global module_status
    module_status = True

    parsed_url = urlparse(url)
    while True:
        threading.Thread(target=add, args=(_utils.get_random_cache(), parsed_url.query)).start()
        time.sleep(_utils.config['delay'])

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    url = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Invite URL', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=url, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(url.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Bot Adder',
    'description':'新しくサーバーを作成して指定したボットを導入します'
}