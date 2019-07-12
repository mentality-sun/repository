# """
# 简易客户端
# """
#
# import socket
#
# HOST = '10.232.8.227'     #获取本地主机名
# PORT = 15                #设置端口号
# ADDR = (HOST,PORT)
#
# web = socket.socket()
#
# web.connect(ADDR)           #请求与服务器建立连接
# web.send(str.encode("this is client..."))   #向服务器发送信息
#
# data = web.recv(1024)       #接收数据
# print(data)                 #打印出接受到的数据
#
# web.close()
import socket
HOST="10.232.8.227"
port=15
ADDR=(HOST,port)
web=socket.socket()
web.connect(ADDR)
web.send(str.encode("I am a client"))
data=web.recv(1024)
print(data)
