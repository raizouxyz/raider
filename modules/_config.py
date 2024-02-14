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

def check_token():
    valid_tokens_list = []
    valid_tokens = ''
    flagged_tokens = ''
    ratelimited_tokens = ''
    invalid_tokens = ''
    valid_caches = []
    valid_tokens_count = 0
    flagged_tokens_count = 0
    ratelimited_tokens_count = 0
    invalid_tokens_count = 0

    for cache in _utils.caches:
        response = requests.get(f'https://discord.com/api/v9/users/@me/survey', headers=cache['headers'], proxies=cache['proxy'])
        #response = requests.get(f'https://discord.com/api/v9/users/@me/billing/country-code', headers=cache['headers'], proxies=cache['proxy'])
        print(response.status_code, response.text)
        if response.status_code == 200:
            valid_tokens_list.append(cache["headers"]["Authorization"])
            valid_tokens += f'{cache["login_information"]["email"]}:{cache["login_information"]["password"]}:{cache["headers"]["Authorization"]}\n'
            valid_caches.append(cache)
            valid_tokens_count += 1
        elif response.status_code == 403:
            flagged_tokens += f'{cache["login_information"]["email"]}:{cache["login_information"]["password"]}:{cache["headers"]["Authorization"]}\n'
            flagged_tokens_count += 1
        elif response.status_code == 429:
            ratelimited_tokens += f'{cache["login_information"]["email"]}:{cache["login_information"]["password"]}:{cache["headers"]["Authorization"]}\n'
            ratelimited_tokens_count += 1
        else:
            invalid_tokens += f'{cache["login_information"]["email"]}:{cache["login_information"]["password"]}:{cache["headers"]["Authorization"]}\n'
            invalid_tokens_count += 1

    print(f'[Token Checker] All:{len(_utils.caches)}, Valid:{valid_tokens_count}, Flagged:{flagged_tokens_count}, RateLimited:{ratelimited_tokens_count}, Invalid:{invalid_tokens_count}')

    with open('./data/tokens.txt', mode='w', encoding='utf-8') as f:
        f.write(valid_tokens)
    with open('./data/checker/token/flagged_tokens.txt', mode='w', encoding='utf-8') as f:
        f.write(flagged_tokens)
    with open('./data/checker/token/ratelimited_tokens.txt', mode='w', encoding='utf-8') as f:
        f.write(ratelimited_tokens)
    with open('./data/checker/token/invalid_tokens.txt', mode='w', encoding='utf-8') as f:
        f.write(invalid_tokens)

    _utils.tokens = valid_tokens_list
    _utils.caches = valid_caches

def check_proxy():
    valid_proxies_list = []
    valid_proxy_details_list = []
    valid_proxies = ''
    invalid_proxies_list = []
    invalid_proxies = ''
    for proxy in _utils.proxies:
        try:
            response = requests.get('https://checkip.amazonaws.com', proxies=proxy, timeout=4)
        except requests.exceptions.ProxyError:
            invalid_proxies += _utils.proxy_details[proxy['http']]['raw'] + '\n'
            invalid_proxies_list.append(proxy)
            continue
        if response.status_code == 200:
            print(response.text)
            valid_proxies_list.append(proxy)
            valid_proxy_details_list.append(_utils.proxy_details[proxy['http']])
            valid_proxies += _utils.proxy_details[proxy['http']]['raw'] + '\n'

    print(f'[Proxy Checker] All:{len(_utils.proxies)}, Valid:{len(valid_proxies_list)}, Invalid:{len(invalid_proxies_list)}')

    with open('./data/proxies.txt', mode='w', encoding='utf-8') as f:
        f.write(valid_proxies)
    with open('./data/checker/proxy/invalid_proxies.txt', mode='w', encoding='utf-8') as f:
        f.write(invalid_proxies)

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

    if _utils.markov_model == None:
        tkinter.Label(master=module_frame, text='Markov Chain: Disabled', foreground='#ffffff', background='#2c2f33').pack()
    else:
        tkinter.Label(master=module_frame, text='Markov Chain: Enabled', foreground='#ffffff', background='#2c2f33').pack()

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
    
    tkinter.Button(master=module_frame, text='Check Tokens', command=lambda:threading.Thread(target=check_token).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Check Proxies', command=lambda:threading.Thread(target=check_proxy).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Refresh Spotify Token', command=lambda:threading.Thread(target=refresh_spotify_token).start(), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Button(master=module_frame, text='Reload Markov Data', command=lambda:threading.Thread(target=reload_markov).start(), foreground='#ffffff', background='#2c2f33').pack()

module = {
    'name': 'Config Menu'
}