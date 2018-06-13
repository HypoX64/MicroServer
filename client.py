#encoding = utf-8#
from socket import *
# address='192.168.191.137'   #服务器的ip地址 127.0.0.1是本机 0.0.0.0是整个网络
address='39.108.224.145'   #服务器的ip地址
port=20000           #服务器的端口号
buffsize=1024        #接收数据的缓存大小


#注册json格式：
#{"mod":"register","account":"hypo","password":"123456"}
#登录json格式：
#{"mod":"login","account":"hypo","password":"123456"}
#数据发送：
#{"mod":"data"}

while True:
    try:
        senddata=input('data you want to send：')
        # if senddata=='exit':
        #     break
        if senddata!="":
            s=socket(AF_INET, SOCK_STREAM)
            s.connect((address,port))
            s.send(senddata.encode())
            recvdata=s.recv(buffsize).decode('utf-8')
            s.close()
            print(recvdata)
    except Exception as e:
        print(e)

s.close()