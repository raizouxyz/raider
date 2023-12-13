import time
import tkinter
import requests
import threading
from modules import _utils

module_status = False

report_types = {
    'スパム': [3, 45],
    '私または他人に対する言葉での嫌がらせ': [3, 23, 48],
    '無礼、卑猥、または攻撃的な言葉遣い': [3, 23, 49],
    'アイデンティティや弱みを理由としたヘイトを助長している': [3, 28, 42, 53],
    'ゴア（流血）、動物虐待、他者にショックを与えることを意図した暴力的なコンテンツ': [3, 23, 33, 54],
    '成人を描いた、望んでいない性的 画像': [3, 23, 33, 55],
    '成人を描いた侮辱的なポルノ': [3, 23, 33, 56],
    'リベンジポルノ、またはリベンジポルノを共有するという脅し': [3, 23, 33, 57],
    '未成年者を性的に扱うイラスト（「ロリコン」、「ショタコン」、「幼獣ポルノ」など）': [3, 23, 35, 58],
    '未成年者について性的な話をしている人物がいる': [3, 23, 35, 59],
    '未成年者に性的 な示唆を含む、または性的なメッセージを送っている人物がいる': [3, 23, 35, 60],
    '未成年者が性的なメッセージを投稿または送信している': [3, 23, 35, 61],
    '現実の子どもに 対する性的虐待の写真または動画': [3, 23, 35, 62],
    '別の Discord サーバーを攻撃すると脅している': [3, 28, 41, 75],
    '現行のレイドを宣言または奨励している': [3, 28, 41, 76],
    'BAN されているにもかかわらず再度サーバーに参加した': [3, 28, 41, 77],
    'ブロックしたにもかかわらずメッセージを送ってきている': [3, 28, 41, 78],
    '私または他の誰かを物理的に傷つけるという脅迫': [3, 23, 37, 63],
    '暴力行為を賛美または美化している': [3, 28, 42, 64],
    '自分または知人について悪口を言っている': [3, 28, 42, 48],
    'フェイクニュースや有害な陰謀論を広めている': [3, 28, 42, 79],
    'はい、このメッセージ内で年齢を宣言しています': [3, 28, 38, 73],
    'なりすまし、欺瞞、詐欺': [3, 28, 66],
    '盗まれたアカウントやクレジットカードを配っている': [3, 28, 69],
    'ドラッグやその他の禁制品を販売している': [3, 28, 70],
    'ハック、チート、フィッシング、またはその他の 悪意あるリンク': [3, 28, 72]
}

def report(cache, channel_id, message_id, report_type):
    request_data = {
        "version":"1.0",
        "variant":"3",
        "language":"en",
        "breadcrumbs":report_type,
        "elements":{},
        "name":"message",
        "channel_id":channel_id,
        "message_id":message_id
    }
    response = requests.post(f'https://discord.com/api/v9/reporting/message', headers=cache['headers'], proxies=cache['proxy'], json=request_data)
    print(response.status_code, response.text)

def start(channel_id, message_id, report_type):
    global module_status
    module_status = True

    for cache in _utils.caches:
        if module_status:
            threading.Thread(target=report, args=(cache, channel_id, message_id, list(report_types.values())[report_type])).start()
            time.sleep(_utils.config['delay'])
            pass
        else:
            break

def stop():
    global module_status
    module_status = False

def draw_module(module_frame):
    channel_id = tkinter.StringVar()
    message_id = tkinter.StringVar()
    report_type = tkinter.StringVar()

    tkinter.Label(master=module_frame, text='Channel ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=channel_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Message ID', foreground='#ffffff', background='#2c2f33').pack()
    tkinter.Entry(master=module_frame, textvariable=message_id, width=50).pack()
    tkinter.Label(master=module_frame, text='Report Type', foreground='#ffffff', background='#2c2f33').pack()
    listbox = tkinter.Listbox(master=module_frame, listvariable=report_type, font=(None, 10), width=64, height=16, justify='center', foreground='#ffffff', background='#2c2f33')
    for report_type in report_types.keys():
        listbox.insert(tkinter.END, report_type)
    listbox.pack()
    tkinter.Button(master=module_frame, text='Start', width=10, foreground='#ffffff', background='#2c2f33', command=lambda:threading.Thread(target=start, args=(channel_id.get(),message_id.get(),listbox.curselection()[0])).start()).pack()
    tkinter.Button(master=module_frame, text='Stop', width=10, foreground='#ffffff', background='#2c2f33', command=stop).pack()

module = {
    'name':'Message Reporter',
    'description':'メッセージを通報します'
}