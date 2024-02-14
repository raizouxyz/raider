import re
import json
import time
import base64
import random
import tkinter
import requests
import threading
import playsound
import websocket
from modules import _utils
from bs4 import BeautifulSoup
import tls_client
module_status = False

tokens = ''
caches = []

def generate(poipoi_session, poipoi_token, email_verify):
    global tokens, caches
    session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
    proxy = _utils.get_random_proxy()
    proxy_detail = _utils.proxy_details[proxy['http']]
    headers = _utils.empty_headers(proxy=proxy)
    username = _utils.random_string(10, 8)
    password = _utils.random_string(20, 15, True).replace(':', '0')

    email = None
    if email_verify:
        response = poipoi_session.get(f'https://m.kuku.lu/index.php?action=addMailAddrByManual&by_system=1&csrf_token_check={poipoi_token}&newdomain=tatsu.uk&newuser=')
        email = _utils.remove_string(response.text, 'OK:')
        print(f'[Generated Email] {email}')
    else:
        email = f'{_utils.random_string(15)}@gmail.com'
    headers['X-Context-Properties'] = base64.b64encode('{"location":"Register"}'.encode()).decode()
    response = session.get('https://discord.com/api/v9/experiments?with_guild_experiments=true', headers=headers, proxy=proxy)
    headers.pop('X-Context-Properties')
    fingerprint = response.json()['fingerprint']
    headers['X-Fingerprint'] = fingerprint
    response = session.get('https://discord.com/api/v9/auth/location-metadata', headers=headers, proxy=proxy)
    print(response.status_code, response.text)
    response = session.get(f'https://discord.com/api/v9/unique-username/username-suggestions-unauthed?global_name={username}', headers=headers, proxy=proxy)
    print(response.status_code, response.text)
    username = response.json()['username']
    birth_year = random.randint(1950, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)

    request_data = {
        "fingerprint":fingerprint,
        "email":email,
        "username":username,
        "global_name":username,
        "password":password,
        "invite":None,
        "consent":True,
        "date_of_birth":f"{birth_year}-{str(birth_month).zfill(2)}-{str(birth_day).zfill(2)}",
        "gift_code_sku_id":None,
        "promotional_email_opt_in":False,
    }

    token = ''
    response = session.post('https://discord.com/api/v9/auth/register', headers=headers, proxy=proxy, json=request_data)
    print(response.status_code, response.text)
    if response.status_code == 201:
        token = response.json()['token']
        print(f'[Created Account] {email}:{password}:{token}')
        headers['Authorization'] = token
    elif response.status_code == 400:
        captcha_sitekey = response.json()['captcha_sitekey']
        captcha_result = _utils.solve_captcha(captcha_sitekey, 'https://discord.com/register', headers['User-Agent'], proxy_detail=proxy_detail)
        if captcha_result:
            headers['X-Captcha-Key'] = captcha_result
            response = session.post('https://discord.com/api/v9/auth/register', headers=headers, proxy=proxy, json=request_data)
            print(response.status_code, response.text)
            if response.status_code == 200 or response.status_code == 201:
                token = response.json()['token']
                print(f'[Created Account] {email}:{password}:{token}')
                headers['Authorization'] = token
                headers.pop('X-Captcha-Key')
            else:
                return
        else:
            return

    headers.pop('X-Fingerprint')
    #ws = websocket.WebSocket()
    #ws.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream", header={'User-Agent':_utils.config['useragent']}, http_proxy_host=proxy_detail['host'], http_proxy_port=proxy_detail['port'], http_proxy_auth=(proxy_detail['username'], proxy_detail['password']))
    #ws.send(f'{{"op":2,"d":{{"token":"{token}","capabilities":16381,"properties":{{"os":"Windows","browser":"Chrome","device":"","system_locale":"ja-JP","browser_user_agent":"{_utils.config["useragent"]}","browser_version":"{_utils.config["chrome_version"]}","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":{_utils.config["client_build_number"]},"client_event_source":null}},"presence":{{"status":"unknown","since":0,"activities":[],"afk":false}},"compress":false,"client_state":{{"guild_versions":{{}},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1,"private_channels_version":"0","api_code_version":0}}}}}}')
    #ws.send('{"op":4,"d":{"guild_id":null,"channel_id":null,"self_mute":true,"self_deaf":false,"self_video":false,"flags":2}}')

    if email_verify:
        while True:
            response = poipoi_session.get(f'https://m.kuku.lu/recv._ajax.php?&q={email} メールアドレスを確認してください&csrf_token_check={poipoi_token}')
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find('span', attrs={'class':'view_listcnt'}).contents[0] == '1':
                break
            time.sleep(2)
        soup = BeautifulSoup(response.text, 'html.parser')
        mail_element = soup.find('div', attrs={'class':'main-content'}).find('div', attrs={'style':'z-index:99;'})
        script_element = mail_element.parent.find_all('script')[2]
        parsed_javascript = re.findall(r'\'.*\'', script_element.string)
        num = parsed_javascript[1].split(',')[0].replace('\'', '')
        key = parsed_javascript[1].split(',')[1].replace('\'', '').replace(' ', '')

        response = poipoi_session.post('https://m.kuku.lu/smphone.app.recv.view.php', data={'num':num, 'key':key})
        soup = BeautifulSoup(response.text, 'html.parser')
        verify_redirect_url = soup.find('a', text='\n            Verify Email\n          ').attrs['href']
        response = session.get(verify_redirect_url, headers=headers, proxy=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_element = soup.find('script')
        verify_url = script_element.contents[0].replace('\n', '').replace('\t', '').replace('setTimeout(function(){location.href = "', '').replace('";}, 1);', '')
        response = requests.get(verify_url, headers=headers, proxies=proxy)
        verify_token = response.request.url.replace('https://discord.com/verify#token=', '')
        request_data = {"token": verify_token}
        response = session.post('https://discord.com/api/v9/auth/verify', headers=headers, proxy=proxy, json=request_data)
        print(response.status_code, response.text)
        if response.status_code == 200:
            token = response.json()['token']
            print(f'[Email Verified] {email}:{password}:{token}')
            headers['Authorization'] = token
        elif response.status_code == 400:
            if 'captcha_sitekey' in response.json().keys():
                captcha_sitekey = response.json()['captcha_sitekey']
                captcha_result = _utils.solve_captcha(captcha_sitekey, 'https://discord.com/verify', headers['User-Agent'], proxy_detail=proxy_detail)
                if captcha_result:
                    headers['X-Captcha-Key'] = captcha_result
                    response = session.post('https://discord.com/api/v9/auth/verify', headers=headers, json=request_data, proxy=proxy)
                    print(response.status_code, response.text)
                    if response.status_code == 200 or response.status_code == 201:
                        print(f'[Email Verified] {email}:{password}:{token}')
                        token = response.json()['token']
                        headers['Authorization'] = token
                        headers.pop('X-Captcha-Key')
                    else:
                        return
                else:
                    return
            else:
                return

    if 'Authorization' in headers.keys():

        response = session.get('https://discord.com/api/v9/users/@me/affinities/users', headers=headers, proxy=proxy)
        print(response.status_code, response.text)

        response = session.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, proxy=proxy)
        print(response.status_code, response.text)

        response = session.get('https://discord.com/api/v9/users/@me/billing/country-code', headers=headers, proxy=proxy)
        print(response.status_code, response.text)

        response = session.get('https://discord.com/api/v9/users/@me/survey?disable_auto_seen=true', headers=headers, proxy=proxy)
        print(response.status_code, response.text)

        response = session.get('https://discord.com/api/v9/users/@me/affinities/guilds', headers=headers, proxy=proxy)
        print(response.status_code, response.text)

        response = session.get('https://discord.com/api/v9/user-profile-effects', headers=headers, proxy=proxy)
        print(response.status_code, response.text)

        response = session.patch('https://discord.com/api/v9/users/@me/settings-proto/1', headers=headers, proxy=proxy, json={"settings":"IikKJwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYA=="})
        print(response.status_code, response.text)
        #if response.status_code == 200:
        if True:
            tokens += f'{email}:{password}:{token}\n'
            caches.append({'login_information': {'email': email, 'password': password, 'token': token}, 'headers': headers, 'proxy': proxy, 'proxy_detail': proxy_detail})

def start(email_verify):
    global module_status, tokens, caches
    threading.Thread(target=playsound.playsound, args=('./resources/se/1.mp3',)).start()
    module_status = True

    # alert(document.cookie.split("; ").find((row) => row.startsWith("cookie_csrf_token")).split("=")[1])
    # alert(document.cookie.split("; ").find((row) => row.startsWith("cookie_sessionhash")).split("=")[1])
    poipoi_token = _utils.config['poipoi']['token']
    poipoi_sessionhash = _utils.config['poipoi']['sessionhash']

    poipoi_session = requests.session()
    poipoi_session.cookies.set('cookie_csrf_token', poipoi_token)
    poipoi_session.cookies.set('cookie_sessionhash', poipoi_sessionhash)

    created_tokens = 0

    while module_status:
        generate(poipoi_session, poipoi_token, email_verify)
        if len(caches) != 0:
            with open('./data/tokens.txt', mode='a', encoding='utf-8') as f:
                _utils.tokens += tokens.split('\n')
                f.write(tokens)

        created_tokens += 1
        tokens = ''
        caches = []

    print(f'Created {created_tokens}Tokens')
    created_tokens = 0

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    email_verify = tkinter.BooleanVar()

    tkinter.Checkbutton(master=module_frame, text='Email Verify', variable=email_verify, foreground='#ffffff', background='#2c2f33', selectcolor='black').pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(email_verify.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Token Generator',
    'description':'Tokenを作成します ※今は動きません'
}