# RaizouRaider

![Screenshot1](https://raw.githubusercontent.com/raizou-zap/raider/main/screenshots/screenshot1.png)
![Screenshot2](https://raw.githubusercontent.com/raizou-zap/raider/main/screenshots/screenshot2.png)

## Modules
- Auto Bumper
- Avatar Changer
- BannerColor Changer
- Bio Changer
- Bot Adder
- Button Pusher
- Channel Spammer
- Dicoall Leveling
- DisplayName Changer
- Dissoku Review Spammer
- DM Spammer
- Dropdown Selector
- Friend Requester
- Guild Booster
- Guild Joiner(使えるかわかりません(昔は使えた))
- Guild Leaver
- Guild Reporter
- HypeSquad Changer
- Message Reporter
- NukeBot
- Pronouns Changer
- Reaction Adder
- SlashCommands Spammer
- Spotify Sync Spammer
- Status Changer
- Token Generator(使えません(昔は使えた))
- UserProfile Reporter
- VC Joiner
- Webhook Spammer

### その他機能
- マルコフ連鎖スパム(<MARKOV>)
- Tokenみたいな文字列スパム(<RANDOM_TOKEN>)
- ランダム文字列スパム(<RANDOM_STRING>)
- ランダムメンション(<RANDOM_MENTION>)
- Token Checker
- Proxy Checker

## フォーマット
tokens.txtは以下の形式で入力してください  
```
<Token>
or
<Email>:<Password>:<Token>
```
proxies.txtは以下の形式で入力してください
```
フリープロキシの場合:
<Hostname>
パスワードなど詳しい設定が必要な場合:
<Protocol>://<Username>:<Password>@<Hostname>:<Port>
```

## マルコフ連鎖機能の使用方法
[MeCab](https://github.com/ikegami-yukino/mecab/releases)をインストール  
data/markov.txtにマルコフ連鎖のデータを入れます  
Config MenuにてMarkov ChainがEnabledになっていたら使用できます

## リンク集
[ツイッター](https://twitter.com/raizou_zap)  

## TLS Client Shared Library
https://github.com/FlorianREGAZ/Python-Tls-Client/raw/master/tls_client/dependencies/tls-client-64.dll

## メルアドぽいぽい
token:
```alert(document.cookie.split("; ").find((row) => row.startsWith("cookie_csrf_token")).split("=")[1])```  
session_hash:
```alert(document.cookie.split("; ").find((row) => row.startsWith("cookie_sessionhash")).split("=")[1])```
