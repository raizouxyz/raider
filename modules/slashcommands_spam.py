import time
import copy
import json
import tkinter
import requests
import threading
from modules import _utils
from tkinter import messagebox

module_status = False

def spam(cache, guild_id, channel_id, command, option_number=None):
    headers = copy.deepcopy(cache['headers'])
    headers.pop('Content-Type')
    if option_number == None:
        request_data = {'payload_json': f'{{"type":2,"application_id":"{command["application_id"]}","guild_id":"{guild_id}","channel_id":"{channel_id}","session_id":"{_utils.random_string(32)}","data":{{"version":"{command["version"]}","id":"{command["id"]}","name":"{command["name"]}","type":1,"options":[],"application_command":{json.dumps(command).replace(", ", ",").replace(": ", ":")},"attachments":[]}}}}'}
    else:
        request_data = {'payload_json': f'{{"type":2,"application_id":"{command["application_id"]}","guild_id":"{guild_id}","channel_id":"{channel_id}","session_id":"{_utils.random_string(32)}","data":{{"version":"{command["version"]}","id":"{command["id"]}","name":"{command["name"]}","type":1,"options":[{{"type":1,"name":"{command["options"][option_number]["name"]}","options":[]}}],"application_command":{json.dumps(command).replace(", ", ",").replace(": ", ":")},"attachments":[]}}}}'}
    response = requests.post('https://discord.com/api/v9/interactions', headers=headers, proxies=cache['proxy'], data=request_data, files={(None, None)})
    print(response.status_code, response.text)

def start(guild_id, channel_id, application_id, command_name, subcommand_name):
    global module_status
    module_status = True

    cache = _utils.caches[0]
    response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&query={command_name}&limit=1&include_applications=true&application_id={application_id}', headers=cache['headers'], proxies=cache['proxy'])
    if len(response.json()['application_commands']) == 0:
        messagebox.showerror(title='Error', message='該当するスラッシュコマンドが見つかりません')
    for command in response.json()['application_commands']:
        if command['name'] == command_name:
            if subcommand_name != '':
                option_number = 0
                for option in command['options']:
                    if option['type'] == 1 and option['name'] == subcommand_name:
                        while module_status:
                            threading.Thread(target=spam, args=(_utils.get_random_cache(), guild_id, channel_id, command, option_number)).start()
                            time.sleep(_utils.config['delay'])
                    option_number += 1
            else:
                while module_status:
                    threading.Thread(target=spam, args=(_utils.get_random_cache(), guild_id, channel_id, command)).start()
                    time.sleep(_utils.config['delay'])
    
def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    guild_id = tkinter.StringVar()
    channel_id = tkinter.StringVar()
    application_id = tkinter.StringVar()
    command_name = tkinter.StringVar()
    subcommand_name = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Application ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=application_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Command Name', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=command_name, width=50).pack()
    tkinter.Label(master=module_frame, text='SubCommand Name', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=subcommand_name, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(guild_id.get(),channel_id.get(),application_id.get(),command_name.get(),subcommand_name.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'SlashCommands Spammer',
    'description':'スラッシュコマンドをスパムします'
}