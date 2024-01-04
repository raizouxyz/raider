import copy
import time
import json
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def bump(cache, guild_id, channel_id, command, option_number=None):
    global module_status
    while module_status:
        headers = copy.deepcopy(cache['headers'])
        headers.pop('Content-Type')
        if option_number == None:
            request_data = {'payload_json': f'{{"type":2,"application_id":"{command["application_id"]}","guild_id":"{guild_id}","channel_id":"{channel_id}","session_id":"{_utils.random_string(32)}","data":{{"version":"{command["version"]}","id":"{command["id"]}","name":"{command["name"]}","type":1,"options":[],"application_command":{json.dumps(command).replace(", ", ",").replace(": ", ":")},"attachments":[]}}}}'}
        else:
            request_data = {'payload_json': f'{{"type":2,"application_id":"{command["application_id"]}","guild_id":"{guild_id}","channel_id":"{channel_id}","session_id":"{_utils.random_string(32)}","data":{{"version":"{command["version"]}","id":"{command["id"]}","name":"{command["name"]}","type":1,"options":[{{"type":1,"name":"{command["options"][option_number]["name"]}","options":[]}}],"application_command":{json.dumps(command).replace(", ", ",").replace(": ", ":")},"attachments":[]}}}}'}
        response = requests.post('https://discord.com/api/v9/interactions', headers=headers, proxies=cache['proxy'], data=request_data, files={(None, None)})
        print(response.text)
        response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=10', headers=cache['headers'], proxies=cache['proxy'])
        print(response.text)
        #if command['application_id'] == '302050872383242240':
        #    for message in response.json():
        #        if message['author']['id'] == '302050872383242240':
        #            print(message)
        #            print(message['embeds'][0]['description'])
        #            break
        if command['application_id'] == '761562078095867916':
            for message in response.json():
                if message['author']['id'] == '761562078095867916':
                    print(message['embeds'][0]['fields'][0]['value'])
                    wait_minutes = int(message['embeds'][0]['fields'][0]['value'].replace('間隔をあけてください(', '').replace('分)', ''))+1
                    print(wait_minutes)
                    time.sleep(wait_minutes*60)
                    break
        elif command['application_id'] == '903541413298450462':
            for message in response.json():
                if message['author']['id'] == '903541413298450462':
                    print(message['content'])
                    wait_minutes = int(message['content'].replace('分残りました。', ''))+1
                    time.sleep(wait_minutes*60)
                    break

def start(guild_id, channel_id):
    global module_status
    module_status = True
    #disboard
    response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&query=bump&limit=1&include_applications=true&application_id=302050872383242240', headers=_utils.caches[0]['headers'], proxies=_utils.caches[0]['proxy'])
    print(response.text)
    for command in response.json()['application_commands']:
        if command['name'] == 'bump':
            threading.Thread(target=bump, args=(_utils.get_random_cache(), guild_id, channel_id, command)).start()

    #dissoku
    response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&query=dissoku&limit=1&include_applications=true&application_id=761562078095867916', headers=_utils.caches[0]['headers'], proxies=_utils.caches[0]['proxy'])
    print(response.text)
    for command in response.json()['application_commands']:
        if command['name'] == 'dissoku':
            option_number = 0
            for option in command['options']:
                if option['type'] == 1 and option['name'] == 'up':
                    threading.Thread(target=bump, args=(_utils.get_random_cache(), guild_id, channel_id, command, option_number)).start()
                option_number += 1
    
    #dicoall
    response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&query=up&limit=1&include_applications=true&application_id=903541413298450462', headers=_utils.caches[0]['headers'], proxies=_utils.caches[0]['proxy'])
    print(response.text)
    for command in response.json()['application_commands']:
        if command['name'] == 'up':
            threading.Thread(target=bump, args=(_utils.get_random_cache(), guild_id, channel_id, command)).start()

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    channel_id = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(), channel_id.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Auto Bumper',
    'description':'自動でBumpします'
}