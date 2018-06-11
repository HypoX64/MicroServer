from socket import *
import json

address='172.16.252.183'     #监听哪些网络  127.0.0.1是监听本机 0.0.0.0是监听整个网络
port=20000           #监听自己的哪个端口
buffsize=1024          #接收从客户端发来的数据的缓存区大小
user = {'hypo':'123456'}


def loadjson(recvjsonData):
    replyData={}
    try:
        recvdata=json.loads(recvjsonData)
        # print(recvdata)
        # print(recvdata["password"])

        if recvdata['mod']=='register':
            if recvdata['account'] in user:
                replyData['reply']='account has exised'
            else :
                user[recvdata['account']]=recvdata['password']
                replyData['reply']='register succeed'

        if recvdata['mod']=='login':
            if recvdata['account'] in user:
                if user[recvdata['account']]==recvdata['password']:
                    replyData['reply']='login succeed'
                else:
                    replyData['reply']='password wrong'
            else:
                replyData['reply']='account not exise'


        return(replyData)

    except Exception as e:
        print('error:',e)

print("run!")
s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
s.listen(1)     #最大连接数
while True:
    try:
        clientsock,clientaddress=s.accept()
        print('connect from:',clientaddress)
    #传输数据都利用clientsock，和s无关
        while True:  
            recvdata=clientsock.recv(buffsize).decode('utf-8')
            if recvdata=='exit' or not recvdata:
                break
            senddata=json.dumps(loadjson(recvdata))
            clientsock.send(senddata.encode())
        clientsock.close()
    except Exception as e:
        print('error:',e)
s.close()