# -*- coding:utf-8 -*-
import socket
import face_detector from detect
import bokeh_calculator from BokehDetector

if __name__ == "__main__":
    host = "xxx.xxx.xxx.xxx" #お使いのサーバーのホスト名を入れます
    port = xxxx #クライアントと同じPORTをしてあげます

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとPORTを指定してバインドします
    serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

    print 'Waiting for connections...'
    clientsock, client_address = serversock.accept() #接続されればデータを格納

    while True:
        rcvmsg = clientsock.recv(1024)
        print 'Received -> %s' % (rcvmsg)
        if rcvmsg == '':
            break
        print 'Type message...'
        s_msg = raw_input()
        if s_msg == '':
            break
        print 'Wait...'
        
        dets = detect(img)
        print len(dets)
        bd = BokehDetector()
        for j, d in enumerate(dets):
            print bd.getValue(img,d)
            break
            
        clientsock.sendall(s_msg) #メッセージを返します
    clientsock.close()