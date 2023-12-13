import copy
import json
import time
import base64
import tkinter
import requests
import threading
import websocket
from modules import _utils

module_status = False

def join(cache, invite_code, guild_id, channel_id, onboarding, member_verification):
    headers = copy.deepcopy(cache['headers'])
    properties = f'{{"location":"Accept Invite Page","location_guild_id":"{guild_id}","location_channel_id":"{channel_id}","location_channel_type":0}}'
    headers['X-Context-Properties'] = base64.b64encode(properties.encode()).decode()
    response = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers=headers, proxies=cache['proxy'], json={"session_id":None})
    print(response.status_code, response.text)
    if response.status_code == 200:
        if onboarding != None:
            response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses', headers=cache['headers'], proxies=cache['proxy'], json=onboarding)
            print(response.status_code, response.text)
        if member_verification != None:
            response = requests.put(f'https://discord.com/api/v9/guilds/{guild_id}/requests/@me', headers=cache['headers'], proxies=cache['proxy'], json=member_verification)
            print(response.status_code, response.text)
    elif response.status_code == 400:
        captcha_sitekey = response.json()['captcha_sitekey']
        captcha_result = _utils.solve_captcha(captcha_sitekey, f'https://discord.com/invite/{invite_code}', headers['User-Agent'])
        if captcha_result:
            headers['X-Captcha-Key'] = captcha_result
            headers['X-Captcha-Rqtoken'] = response.json()['captcha_rqtoken']
            response = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers=headers, proxies=cache['proxy'], json={"session_id":None})
            print(response.status_code, response.text)

def start(invite_code):
    global module_status
    module_status = True

    invite_code = _utils.remove_string(invite_code, ['http://', 'https://', 'discord.gg/'])

    guild_id = None
    channel_id = None
    response = None
    onboarding_response = None
    member_verification = None
    for cache in _utils.caches:
        response = requests.get(f'https://discord.com/api/v9/invites/{invite_code}', headers=cache['headers'], proxies=cache['proxy'])
        print(response.status_code, response.text)
        if response.status_code == 200:
            guild_id = response.json()['guild']['id']
            channel_id = response.json()['channel']['id']
            headers = copy.deepcopy(cache['headers'])
            properties = f'{{"location":"Accept Invite Page","location_guild_id":"{guild_id}","location_channel_id":"{channel_id}","location_channel_type":0}}'
            headers['X-Context-Properties'] = base64.b64encode(properties.encode()).decode()
            response = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers=headers, proxies=cache['proxy'], json={"session_id":None})
            print(response.status_code, response.text)
            if response.status_code == 200:
                member_verification = None
                onboarding_response = None
                if 'GUILD_ONBOARDING_HAS_PROMPTS' in response.json()['guild']['features']:
                    _response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/onboarding', headers=headers, proxies=cache['proxy'])
                    print(_response.status_code, _response.text)
                    if _response.status_code == 200:
                        onboarding = json.loads(_response.text)
                        now_timestamp = int(time.time())
                        onboarding_response = {'onboarding_responses':[],'onboarding_prompts_seen':{},'onboarding_responses_seen':{}}
                        for prompt in onboarding['prompts']:
                            onboarding_response['onboarding_prompts_seen'][prompt['id']] = now_timestamp
                            if prompt['single_select'] == True or len(prompt['options']) == 1:
                                onboarding_response['onboarding_responses'].append(prompt['options'][0]['id'])
                                onboarding_response['onboarding_responses_seen'][prompt['options'][0]['id']] = now_timestamp
                            else:
                                for option in prompt['options']:
                                    onboarding_response['onboarding_responses'].append(option['id'])
                                    onboarding_response['onboarding_responses_seen'][option['id']] = now_timestamp
                if 'MEMBER_VERIFICATION_GATE_ENABLED' in response.json()['guild']['features']:
                    member_verification = {}
                    _response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/member-verification', headers=headers, proxies=cache['proxy'])
                    print(_response.status_code, _response.text)
                    member_verification['version'] = _response.json()['version']
                    member_verification['form_fields'] = _response.json()['form_fields']
                for cache in _utils.caches:
                    if module_status:
                        threading.Thread(target=join, args=(cache, invite_code, guild_id, channel_id, onboarding_response, member_verification)).start()
                        time.sleep(_utils.config['delay'])
                    else:
                        break
                break
            elif response.status_code == 400:
                captcha_sitekey = response.json()['captcha_sitekey']
                captcha_result = _utils.solve_captcha(captcha_sitekey, f'https://discord.com/invite/{invite_code}', headers['User-Agent'], True, response.json()['captcha_rqdata'])
                if captcha_result:
                    headers['X-Captcha-Key'] = captcha_result
                    headers['X-Captcha-Rqtoken'] = response.json()['captcha_rqtoken']
                    response = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers=headers, proxies=cache['proxy'], json={"session_id":None})
                    print(response.status_code, response.text)
                    if response.status_code == 400:
                        captcha_sitekey = response.json()['captcha_sitekey']
                        captcha_result = _utils.solve_captcha(captcha_sitekey, f'https://discord.com/invite/{invite_code}', headers['User-Agent'], True ,response.json()['captcha_rqdata'])
                        if captcha_result:
                            headers['X-Captcha-Key'] = captcha_result
                            headers['X-Captcha-Rqtoken'] = response.json()['captcha_rqtoken']
                            response = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers=headers, proxies=cache['proxy'], json={"session_id":None})
                            print(response.status_code, response.text)

def stop():
    global is_stop
    is_stop = True

def draw_module(module_frame):
    invite_code = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Invite Code', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=invite_code, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(invite_code.get(),)).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Guild Joiner',
    'description':'サーバーに入室します'
}