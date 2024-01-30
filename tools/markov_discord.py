import time
import requests

pages = 20
token = ''
guild_id = ''
author_id = ''
channel_id = ''

text = ''

headers = {
    'Authorization': token,
    'Sec-Ch-Ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-Debug-Options':'bugReporterEnabled',
    'X-Discord-Locale':'ja',
    'X-Discord-Timezone':'Asia/Tokyo',
    'X-Super-Properties':'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExOS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE5LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI0NTY0OCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
}

for i in range(pages):
    #response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/messages/search?author_id={author_id}&include_nsfw=true&offset={i*25}', headers=headers)
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/messages/search?channel_id={channel_id}&offset={i*25}', headers=headers)
    for message in response.json()['messages']:
        if message[0]['content'] != '':
            content = message[0]['content'].replace('\n', '')
            print(content)
            text += f'{content}\n'
    time.sleep(2)

with open('../data/markov.txt', mode='w', encoding='utf-8') as f:
    f.write(text)