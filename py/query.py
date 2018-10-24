from pyquery import PyQuery as pq
import json
import requests
import socket
import socks

doc = pq('http://sse.tongji.edu.cn/Data/List/bkstz')

def validDate(date):
    file = open('./py/date.txt', 'r+')
    default_date = int(file.read())
    d = int(str(date))
    return d >= default_date

def sendToBot(jsonData):
    request = 'https://api.telegram.org/bot797393360:AAEHOlWqDxZUPXD4jT-dpRiLdsPAXV514WM/sendMessage'
    headers = {'content-type' : 'application/json'}
    # proxies = {"http":"http://127.0.0.1:1086", "https":"https://127.0.0.1:1086"}
    data = json.dumps(jsonData)
    r = requests.post(request, data=data, headers=headers, timeout=5)
    if r.ok:
        return True
    else:
        file = open('./py/log.txt','a')
        title = jsonData['text'].split('\n')[0]
        line = title + ': bad request, ' + str(r.status_code) + '\n'
        file.write(line)
        file.close
        return False

chat_id = 438673072
validMessage = []

for data in doc('.data-list>li').items():
    link = data('a')
    href = link.attr('href')
    url = 'http://sse.tongji.edu.cn' + href
    cnt = pq(url)
    title = link.text()
    date = href.split('/')[3]
    html_content = cnt('.view-cnt').text()
    text = "**" + title + "**\n" + html_content
    
    if validDate(date):
        jsonData = {
                        "chat_id": chat_id,        
                        "text": text,             
                        "reply_markup": {             
                            "inline_keyboard": [[{     
                                "text":"Link",             
                                "url":url
                            }]]
                        },
                        "parse_mode":"MarkDown"   
                    }
        validMessage.append(jsonData)

print (validMessage)
SOCKS5_PROXY_HOST = '127.0.0.1'		 # socks 代理IP地址
SOCKS5_PROXY_PORT = 1086       # socks 代理本地端口
default_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
socket.socket = socks.socksocket

for m in validMessage:
    sendToBot(m)
        


    
    













 


