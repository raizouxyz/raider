import json
import MeCab
import base64
import tkinter
import requests
import markovify
import threading
import webbrowser
from flask import Flask
from flask import request
from modules import _utils
from tkinter import messagebox

caches = []
tokens = []
def refresh_cache(line):
    global caches, tokens
    if line.count(':') == 2:
        account_information = line.split(':')
        login_information = {'email':account_information[0],'password':account_information[1],'token':account_information[2]}
        tokens.append(account_information[2])

        proxy = _utils.get_random_proxy()
        headers = _utils.empty_headers(proxy)
        headers['Authorization'] = account_information[2]
        print(login_information)
        caches.append({'login_information':login_information, 'headers':headers, 'proxy': proxy, 'proxy_detail': _utils.proxy_details[proxy['http']]})
    elif line.count(':') == 0:
        login_information = {'email':None,'password':None,'token':line}
        tokens.append(line)

        proxy = _utils.get_random_proxy()
        headers = _utils.empty_headers(proxy)
        headers['Authorization'] = line
        print(login_information)
        caches.append({'login_information':login_information, 'headers':headers, 'proxy': proxy, 'proxy_detail': _utils.proxy_details[proxy['http']]})

def refresh_caches_start():
    global caches, tokens
    manager = _utils.threading_manager()
    with open('./data/tokens.txt', mode='r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        if '\n' in lines:
            lines.remove('\n')
        for line in lines:
            if line != '':
                manager.start(target=refresh_cache, args=(line,))
        manager.join(True, True)

    with open('./data/caches.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(caches))

    _utils.caches = caches
    _utils.tokens = tokens
    caches = []
    tokens = []

valid_tokens = ''
flagged_tokens = ''
valid_caches = []
flagged_caches = []
invalid_caches_count = 0

def check_token(cache):
    global valid_tokens, flagged_tokens, valid_caches, flagged_caches, invalid_caches_count
    response = None
    while True:
        response = requests.get(f'https://discord.com/api/v9/users/@me/survey', headers=cache['headers'], proxies=cache['proxy'])
        print(response.status_code, response.text)
        if response.status_code == 200 or response.status_code == 429:
            valid_tokens += f'{cache["login_information"]["email"]}:{cache["login_information"]["password"]}:{cache["headers"]["Authorization"]}\n'
            valid_caches.append(cache)
            break
        elif response.status_code == 403:
            flagged_tokens += f'{cache["login_information"]["email"]}:{cache["login_information"]["password"]}:{cache["headers"]["Authorization"]}\n'
            flagged_caches.append(cache)
            break
        else:
            invalid_caches_count += 1
            break

def check_token_start():
    global valid_tokens, flagged_tokens, valid_caches, flagged_caches, invalid_caches_count
    manager = _utils.threading_manager()
    i = 0
    for cache in _utils.caches:
        manager.start(target=check_token, args=(cache,))
        i += 1
        if i % 10 == 0 or i == len(_utils.caches):
            manager.join(True, True)

    print(f'[Token Checker] All:{len(_utils.caches)}, Valid:{len(valid_caches)}, Flagged:{len(flagged_caches)}, Invalid:{invalid_caches_count}')

    with open('./data/caches.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(valid_caches))
    with open('./data/checker/flagged_caches.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(flagged_caches))
    with open('./data/tokens.txt', mode='w', encoding='utf-8') as f:
        f.write(valid_tokens)
    with open('./data/checker/flagged_tokens.txt', mode='w', encoding='utf-8') as f:
        f.write(flagged_tokens)

    _utils.tokens = []
    for token in valid_tokens.split('\n'):
        if token != '':
            _utils.tokens.append(token)
    _utils.caches = valid_caches

    valid_tokens = ''
    flagged_tokens = ''
    valid_caches = []
    flagged_caches = []
    invalid_caches_count = 0

valid_proxy = ''
valid_proxy_count = 0
invalid_proxy_count = 0

def check_proxy(proxy):
    global valid_proxy, valid_proxy_count, invalid_proxy_count
    response = None
    try:
        response = requests.get('https://checkip.amazonaws.com', proxies=proxy, timeout=4)
    except requests.exceptions.ProxyError:
        invalid_proxy_count += 1
        return
    if response.status_code == 200:
        print(response.text)
        valid_proxy += proxy + '\n'
        valid_proxy_count += 1
    else:
        print(response.status_code)
        invalid_proxy_count += 1

def check_proxy_start():
    global valid_proxy, valid_proxy_count, invalid_proxy_count
    manager = _utils.threading_manager()
    for proxy in _utils.proxies:
        i += 1
        manager.start(target=check_proxy, args=(proxy,))
        if i % 10 == 0 or i == len(_utils.caches):
            manager.join(True, True)

    print(f'[Proxy Checker] All:{len(_utils.proxies)}, Valid:{valid_proxy_count}, Invalid:{invalid_proxy_count}')

    with open('./data/checker/valid_proxies.txt', mode='w', encoding='utf-8') as f:
        f.write(valid_proxy)

    _utils.proxies = []
    _utils.proxy_details = {None:{'protocol':None,'username':None,'password':None,'host':None,'port':None}}
    _proxies = valid_proxy.split('\n')
    for proxy in _proxies:
        if proxy != '':
            proxy_detail_list = proxy.split(':')
            proxy_detail = {}
            if len(proxy_detail_list) == 1:
                proxy_detail = {
                    'protocol': 'http',
                    'username': None,
                    'password': None,
                    'host': proxy_detail_list[0],
                    'port': '8080'
                }
            elif len(proxy_detail_list) == 2:
                proxy_detail = {
                    'protocol': 'http',
                    'username': None,
                    'password': None,
                    'host': proxy_detail_list[0],
                    'port': proxy_detail_list[1]
                }
            elif len(proxy_detail_list) == 4:
                proxy_detail = {
                    'protocol': proxy_detail_list[0],
                    'username': proxy_detail_list[1].replace('//', ''),
                    'password': proxy_detail_list[2].split('@')[0],
                    'host': proxy_detail_list[2].split('@')[1],
                    'port': proxy_detail_list[3]
                }
            if '://' in proxy:
                _utils.proxy_details[proxy] = proxy_detail
                _utils.proxies.append({'http': proxy, 'https': proxy})
            else:
                _utils.proxy_details[f'http://{proxy}'] = proxy_detail
                _utils.proxies.append({'http': f'http://{proxy}', 'https': f'http://{proxy}'})

    valid_proxy = ''
    valid_proxy_count = 0
    invalid_proxy_count = 0

def reload_markov():
    with open("./data/markov.txt", mode="r", encoding='utf-8') as f:
        markov_data = f.read()
        mecab = MeCab.Tagger("-Owakati")
        text = ''
        if markov_data != '':
            for line in markov_data.split('\n'):
                if line != '':
                    parsed_data = ' '.join(mecab.parse(line).split())
                    text += f'{parsed_data}\n'
            _utils.markov_model = markovify.NewlineText(text, well_formed=False)
        else:
            _utils.markov_model = None

flask_app = Flask(__name__)

@flask_app.route("/callback")
def callback():
        if request.method == 'GET':
            code = request.args.get('code')
            if code != None:
                base64_encoded = base64.b64encode(f'{_utils.config["spotify"]["client_id"]}:{_utils.config["spotify"]["client_secret"]}'.encode()).decode()
                request_data = {
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': 'http://localhost:8888/callback',
                }
                headers = {
                    'Authorization': f'Basic {base64_encoded}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=request_data)
                print(response.status_code, response.text)
                if response.status_code == 200:
                    print(response.json()['access_token'])
                    with open('./data/config.json', mode='w', encoding='utf-8') as f:
                        _utils.config['spotify']['access_token'] = response.json()['access_token']
                        f.write(json.dumps(_utils.config))
                    messagebox.showinfo('Information', 'AccessTokenを更新しました\n再起動してください')
                    return 'AccessTokenを更新しました\n再起動してください'
                else:
                    return 'もう一度やり直して下さい'

def refresh_spotify_token():
    if _utils.config['spotify']['client_id'] != None and _utils.config['spotify']['client_secret'] != None:
        webbrowser.open(f'https://accounts.spotify.com/authorize?client_id={_utils.config["spotify"]["client_id"]}&response_type=code&redirect_uri=http://localhost:8888/callback&scope=user-read-playback-state')
        flask_app.run(host="0.0.0.0", port=8888)
    else:
        messagebox.showinfo('Information', 'config.jsonにSpotifyの情報を入力してください')

def save_config(delay, spotify_client_id, spotify_client_secret, poipoi_token, poipoi_sessionhash):
    _utils.config['delay'] = delay
    if spotify_client_id != '':
        _utils.config['spotify']['client_id']
    if spotify_client_secret != '':
        _utils.config['spotify']['client_secret']
    if poipoi_token != '':
        _utils.config['poipoi']['token'] = poipoi_token
    if poipoi_sessionhash != '':
        _utils.config['poipoi']['sessionhash'] = poipoi_sessionhash

    with open('./data/config.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(_utils.config))

def draw_module(module_frame):
    delay = tkinter.DoubleVar()
    spotify_client_id = tkinter.StringVar()
    spotify_client_secret = tkinter.StringVar()
    poipoi_token = tkinter.StringVar()
    poipoi_sessionhash = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Delay', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Scale(master=module_frame, variable=delay, from_=0.1, to=10, length=300, orient=tkinter.HORIZONTAL, resolution=0.1, foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Label(master=module_frame, text='Spotify Client ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=spotify_client_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Spotify Client Secret', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=spotify_client_secret, width=50).pack()
    tkinter.Label(master=module_frame, text='m.kuku.lu Token', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=poipoi_token, width=50).pack()
    tkinter.Label(master=module_frame, text='m.kuku.lu SessionHash', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=poipoi_sessionhash, width=50).pack()
    tkinter.Button(master=module_frame, text='Save Config', command=lambda:save_config(delay.get(),spotify_client_id.get(),spotify_client_secret.get(),poipoi_token.get(),poipoi_sessionhash.get()), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Label(master=module_frame, background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Refresh Caches', command=lambda:threading.Thread(target=refresh_caches_start).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Check Tokens', command=lambda:threading.Thread(target=check_token_start).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Check Proxies', command=lambda:threading.Thread(target=check_proxy_start).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Refresh Spotify Token', command=lambda:threading.Thread(target=refresh_spotify_token).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Reload Markov Data', command=lambda:threading.Thread(target=reload_markov).start(), foreground='#ffffff', background='#2c2f33').pack()

module = {
    'name': 'Config Menu'
}