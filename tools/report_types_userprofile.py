import json
import requests

caches = []
with open('../data/caches.json', mode='r', encoding='utf-8') as f:
    filedata = f.read()
    if not filedata == '':
        caches = json.loads(filedata)

report_types = {}
if len(caches) != 0:
    response = requests.get('https://discord.com/api/v9/reporting/menu/user', headers=caches[0]['headers'], proxies=caches[0]['proxy'])
    root_node_id = response.json()['root_node_id']
    for child in response.json()['nodes'][str(root_node_id)]['children']:
        if response.json()['nodes'][str(child[1])]['header'] == '通報の内容':
            report_type = [3, child[1]]
            report_types[child[0]] = report_type
            continue
        else:
            type1 = child[1]
            for child in response.json()['nodes'][str(child[1])]['children']:
                if response.json()['nodes'][str(child[1])]['header'] == '通報の内容':
                    report_type = [3, type1, child[1]]
                    report_types[child[0]] = report_type
                    continue
                else:
                    type2 = child[1]
                    for child in response.json()['nodes'][str(child[1])]['children']:
                        if response.json()['nodes'][str(child[1])]['header'] == '通報の内容':
                            report_type = [3, type1, type2, child[1]]
                            report_types[child[0]] = report_type
                            continue
                        else:
                            type3 = child[1]
                            for child in response.json()['nodes'][str(child[1])]['children']:
                                report_type = [3, type1, type2, child[1]]
                                report_types[child[0]] = report_type
print(report_types)
a = input()