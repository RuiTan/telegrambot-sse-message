from pyquery import PyQuery as pq
import json
import requests
import socket
import socks
import time
from telegraph import Telegraph

'''
    验证当前通知是否已阅读过
'''
def validDate(date):
    print("finish validDate()\n")
    file = open('./py/date.txt', 'r')
    text = file.read()
    if text != "":
        default_date = int(text)
    else:
        default_date = 0
    file.close
    d = int(str(date))
    return d > default_date

'''
    将URL中最大date填入文件，为验证下次通知服务
'''
def redefDate(date):
    print("finish redefDate()\n")
    file = open('./py/date.txt', 'w')
    file.write(str(date))
    file.close

'''
    写日志文件
'''
def writeLog(line):
    print("finish writeLog()\n")
    file = open('./py/log.txt','a')
    file.write(line)
    file.close

def shLog():
    print("finish shLog()\n")
    file = open('./py/log.txt','a')
    line = '\n' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' : 脚本执行...' + '\n'
    file.write(line)
    file.close

'''
    使用Telegram给RuiRuiBot发通知
'''
def sendToBot(jsonData):
    print("finish sendToBot()\n")
    request = 'https://api.telegram.org/bot797393360:AAEHOlWqDxZUPXD4jT-dpRiLdsPAXV514WM/sendMessage'
    headers = {'content-type' : 'application/json'}
    # data = json.dumps(jsonData)
    # title = jsonData['text'].split('\n')[0].replace('*', '')
    tele_url = jsonData["tele_url"]
    url = jsonData["url"]
    data = {
        "chat_id": chat_id,        
        "text": tele_url,             
        "reply_markup": {             
            "inline_keyboard": [[{     
            "text":"Go",             
            "url": url
        }]]
        },
        "parse_mode":"Markdown"   
    }
    try:
        r = requests.post(request, data=json.dumps(data), headers=headers, timeout=5)
        if r.ok:
            return True 
        else:
            line = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' : ' + title + ': bad request, ' + str(r.status_code) + '\n'
            writeLog(line)
            return False
    except requests.exceptions.ReadTimeout:
        line = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' : ' + title + ': time out error\n'
        writeLog(line)
    
'''
    根据通知生成telegraph界面
'''
def getTelegraph(teleData, telegraph):
    print("finish getTelegraph()\n")
    response = telegraph.create_page(title=teleData["title"],
                         html_content=teleData["content"],
                         author_name=teleData["author"],
                         author_url=teleData["author_url"])
    url = 'https://telegra.ph/{}'.format(response['path'])
    print(url)
    return url # 生成的文章链接

'''
    主函数
'''
if __name__ == '__main__':
    shLog()

    doc = pq('http://sse.tongji.edu.cn/Data/List/bkstz')
    chat_id = 438673072
    validMessage = []
    maxDate = 0
    telegraph = Telegraph()
    telegraph.create_account(short_name='Tanrui')
    print("finish read message from sse\n")
    for data in (doc('.data-list>li').items()):
        link = data('a')
        href = link.attr('href')
        url = 'http://sse.tongji.edu.cn' + href
        cnt = pq(url)
        title = link.text()
        date = href.split('/')[3]
        if maxDate <= int(date):
            maxDate = int(date)
        html_content = cnt('.view-cnt').text()
        text = "**" + title + "**\n" + html_content
        
        if validDate(date):
            teleData = {
                "title" : title,
                "author" : "SSE Message Bot —— RuiRui",
                "author_url": "https://guitoubing.top",
                "content" : html_content
            }
            tele_url = getTelegraph(teleData, telegraph)
            validMessage.append({
                "tele_url": tele_url,
                "url" : url
            })

    print (validMessage)
    SOCKS5_PROXY_HOST = '127.0.0.1'		 # socks 代理IP地址
    SOCKS5_PROXY_PORT = 1086       # socks 代理本地端口
    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
    socket.socket = socks.socksocket

    for m in validMessage:
        sendToBot(m)

    redefDate(maxDate)