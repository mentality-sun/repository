# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import time
import os
import requests

class AIS(object):
    def ai(c):
        # 青云客智能机器人
        # url="http://api.qingyunke.com/api.php?key=free&appid=0&msg="+c
        # 茉莉机器人
        url="http://i.itpk.cn/api.php?question="+c+"&api_key=8292134104da2a7d6c0e88905fad9f01&api_secret=p6vvfhnpufz3"
        contents=requests.get(url)
        cont=contents.text
        return cont
class Handle(object):

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "weixin"

            list = [token, timestamp, nonce]
            list.sort()
            s = list[0] + list[1] + list[2]
            hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
            print( "handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except (Exception) as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is:\n", webData)
            #打印消息体日志
            recMsg = receive.parse_xml(webData)

            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content=AIS.ai(str(recMsg.Content))
                return self.render.reply_text(toUser, fromUser, int(time.time()), content)

            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'image':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                print('收到图片消息！')
                mediaId = recMsg.MediaId
                print('媒体id:' + mediaId)
                return self.render.reply_image(toUser, fromUser, int(time.time()), mediaId)
            else:
                print("不支持的消息类型：",recMsg.MsgType)
                return "success"
        except (Exception) as Argment:
            return Argment