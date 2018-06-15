#encoding = utf-8#
from socket import *
import json
import threading
import datetime

address='172.16.252.183'  
# address='192.168.191.137'     #监听哪些网络  127.0.0.1是监听本机 0.0.0.0是监听整个网络
port=20000           #监听自己的哪个端口
buffsize=1024          #接收从客户端发来的数据的缓存区大小
database = './database'
logpath = './log'
senddata = './senddata'
user = {}

s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
s.listen(10)     #最大连接数

def LoadSenddata(path):
    line=open(path).readline()
    line=line.strip()
    return line

def LoadDatabase(path):
    data={}
    for line in open(path):
        line=line.strip()
        data=json.loads(line)
    return data

def writelog(log):
    f = open(logpath,"a+")
    f.write(log+'\n')
    print(log)

def loadjson(recvjsonData):
    global user
    replydata={}
    try:
        recvdata=json.loads(recvjsonData)

        #register
        if recvdata['mod']=='register':
            if recvdata['account'] in user:
                replydata['reply']='account has existed'
            else :
                user[recvdata['account']]=recvdata['password']
                f = open(database,"w+")
                f.write(str(json.dumps(user)))
                replydata['reply']='ok'
            writelog(recvdata['mod']+': '+recvdata['account']+': '+replydata['reply'])

        #login
        elif recvdata['mod']=='login':
            if recvdata['account'] in user:
                if user[recvdata['account']]==recvdata['password']:
                    replydata['reply']='ok'
                else:
                    replydata['reply']='wrong password'
            else:
                replydata['reply']='account not exist'
            writelog(recvdata['mod']+': '+recvdata['account']+': '+replydata['reply'])

        elif recvdata['mod']=='change':
            if recvdata['account'] in user:
                if user[recvdata['account']]==recvdata['oldpassword']:
                    user[recvdata['account']]=recvdata['newpassword']
                    f = open(database,"w+")
                    f.write(str(json.dumps(user)))
                    replydata['reply']='ok'
                else:
                    replydata['reply']='wrong password'
            else:
                replydata['reply']='account not exist'
            writelog(recvdata['mod']+': '+recvdata['account']+': '+replydata['reply'])
        
        #data analysis
        elif recvdata['mod']=='data':
            replydata['reply']=LoadSenddata(senddata)
            writelog(recvdata['mod']+': '+'data sent!')

        #error
        else:
            replydata['reply']='error: please send data as example'

        return replydata

    except Exception as e:
        writelog('error:'+str(e))
        # print(datetime.datetime.now(),'error:',e)
        replydata['reply']='error: please send as example'
        return replydata 


def tcplink(clientsock):
    # while True: 
    recvdata=clientsock.recv(buffsize).decode('utf-8')
    writelog('receiver: '+str(recvdata))
    if recvdata=='exit' or not recvdata:
        clientsock.close()
        return
    senddata=json.dumps(loadjson(recvdata))
    clientsock.send(senddata.encode())
    clientsock.close()

def main(): 
    global user
    user=LoadDatabase(database)
    writelog('\n'+str(datetime.datetime.now())+"\nserver run!")
    while True:
        try:
            clientsock,clientaddress=s.accept()
            writelog(str(datetime.datetime.now())+' connect from:'+str(clientaddress))
            # print(datetime.datetime.now(),'connect from:',clientaddress)
            t=threading.Thread(target=tcplink,args=(clientsock,))  #t为新创建的线程
            t.start()
        except Exception as e:
            writelog(str(datetime.datetime.now())+' error:'+str(e))
            # print(datetime.datetime.now(),'error:',e)
    s.close()

if __name__ == '__main__':
    main()