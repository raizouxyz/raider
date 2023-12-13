import os
import time
import tkinter
import modules
import requests
import threading
import pypresence
from PIL import ImageTk
from modules import _utils
from modules import _config
from tkinter import messagebox

def reload_status(threading_counter_label, caches_counter_label, proxy_counter_label):
    try:
        while True:
            threading_counter_label['text'] = f'Active Threads: {threading.active_count()}'
            caches_counter_label['text'] = f'Caches: {len(_utils.caches)}'
            proxy_counter_label['text'] = f'Proxies: {len(_utils.proxies)}'
            time.sleep(1)
    except RuntimeError:
        pass

version = '2.2'

try:
    response = requests.get('https://raizou-zap.github.io/thunder/presence_id.txt')
    response.encoding = 'utf-8'
    presence_id = response.text.replace('\n','')
    presence = pypresence.Presence(client_id=presence_id)
    presence.connect()
    presence.update(start=int(time.time()), large_image='teamzap', large_text='Thunder', small_image='discord', small_text='for Discord', buttons=[{'label':'Buy Thunder', 'url':'https://teamzap.cc/thunder/'}, {'label':'#TeamZap', 'url':'https://teamzap.cc/'}])
except:
    pass

def change_module(event):
    if len(listbox.curselection()) != 0:
        module_number = listbox.curselection()[0]
        children = module_frame.winfo_children()
        for child in children:
            child.destroy()
        tkinter.Label(master=module_frame, text=modules._modules[module_number].module['name'], font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()
        tkinter.Label(master=module_frame, text=modules._modules[module_number].module['description'], font=(None, 10), foreground='#ffffff', background='#2c2f33').pack()
        modules._modules[module_number].draw_module(module_frame)

def config_menu():
    children = module_frame.winfo_children()
    for child in children:
        child.destroy()
    tkinter.Label(master=module_frame, text=_config.module['name'], font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()
    _config.draw_module(module_frame)

def about_menu():
    children = module_frame.winfo_children()
    for child in children:
        child.destroy()
    tkinter.Label(master=module_frame, text=f'Thunder Raider v{version}', font=(None, 20), foreground='yellow', background='#2c2f33').pack()
    tkinter.Label(master=module_frame, image=icon).pack()
    tkinter.Label(master=module_frame, text='Created by #TeamZap\nhttps://teamzap.cc/\n\n', font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Label(master=module_frame, text=_utils.message, font=(None, 20), foreground='#ffffff', background='#2c2f33').pack()

print(f'Thunder v{version}')
print('Created by #TeamZap\n')

root = tkinter.Tk()
icon = ImageTk.PhotoImage(file=os.path.dirname(__file__)+'/icon.ico')  
root.iconphoto(False, icon)
root.title(f'Thunder v{version}')
root.geometry('800x500')
root.resizable(False, False)

header_frame = tkinter.Frame(master=root, width=200, height=500, background='#2c2f33')
header_frame.propagate(False)
module_frame = tkinter.Frame(master=root, width=600, height=500, background='#2c2f33')
module_frame.propagate(False)

tkinter.Label(master=header_frame, text='Thunder', font=(None, 30), foreground='yellow', background='#2c2f33').pack()
tkinter.Label(master=header_frame, text=f'Version:{version}', font=(None, 15), foreground='#ffffff', background='#2c2f33').pack()
tkinter.Label(master=header_frame, text='Modules', foreground='#ffffff', background='#2c2f33').pack()

listbox = tkinter.Listbox(master=header_frame, font=(None, 12), width=24, height=16, justify='center', foreground='#ffffff', background='#2c2f33')
listbox.bind('<<ListboxSelect>>', change_module)
for module in modules._modules:
    listbox.insert(tkinter.END, module.module['name'])
listbox.pack()

threading_counter_label = tkinter.Label(master=header_frame, foreground='#ffffff', background='#2c2f33')
threading_counter_label.pack()
caches_counter_label = tkinter.Label(master=header_frame, foreground='#ffffff', background='#2c2f33')
caches_counter_label.pack()
proxy_counter_label = tkinter.Label(master=header_frame, foreground='#ffffff', background='#2c2f33')
proxy_counter_label.pack()

tkinter.Button(master=header_frame, text='Config Menu', foreground='#ffffff', background='#2c2f33', command=config_menu).pack()
tkinter.Button(master=header_frame, text='About Thunder', foreground='#ffffff', background='#2c2f33', command=about_menu).pack()

config_menu()

header_frame.pack(side=tkinter.LEFT)
module_frame.pack(side=tkinter.LEFT)

if sorted([version, _utils.update_version]).index(_utils.update_version) != 0:
    messagebox.showinfo('Information', message=f'新しいバージョンがリリースされました\n使用しているバージョン:{version}\n最新のバージョン:{_utils.update_version}\n更新内容:{_utils.update_contents}')
if len(_utils.caches) == 0:
    messagebox.showinfo('Information', message='caches.jsonにデータが入っていません\nConfig MenuからRefresh Cachesをしてください')

threading.Thread(target=reload_status, args=(threading_counter_label,caches_counter_label,proxy_counter_label)).start()
root.mainloop()