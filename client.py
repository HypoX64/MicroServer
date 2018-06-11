from socket import *
# address='127.0.0.1'   #服务器的ip地址 127.0.0.1是本机 0.0.0.0是整个网络
address='39.108.224.145'   #服务器的ip地址

#注册json格式：
#{"mod":"register","account":"hypo","password":"123456"}
#登录json格式：：
#{"mod":"login","account":"hypo","password":"123456"}

port=20000           #服务器的端口号
buffsize=1024        #接收数据的缓存大小
s=socket(AF_INET, SOCK_STREAM)
s.connect((address,port))
while True:
    senddata=input('想要发送的数据：')
    if senddata=='exit':
        break
    s.send(senddata.encode())
    recvdata=s.recv(buffsize).decode('utf-8')
    print(recvdata)
s.close()