# -*- coding:utf-8 -*-
import socket
import sys
import numpy
import cv2
import base64
import shutil
from face_detector import detect
from bokeh_calculator import BokehDetector

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind(([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1],80)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

cpath = "C:\\Users\\120350181\\Desktop\\"

def getImageFromServer():
    print 'Waiting for connections...'
    clientsock, client_address = serversock.accept() #接続されればデータを格納
    recvlen=100
    buffer=''
    while recvlen>0:
        rcvmsg=clientsock.recv(1024*8)
        recvlen=len(rcvmsg)
        buffer +=rcvmsg
    if buffer.find('Name:') == 0:
        name = buffer.strip("Name:")
        dir = "{}demo\\{}".format(cpath,name)
        count = 1
        while true:
            if not os.path.isdir(dir):
                os.makedirs(dir)
                break
            else:
                count = count + 1 
                dir = "{}{}".format(dir,count)
        shutil.move("{}{}".format(cpath,"demo\\tmp\\tmp.jpg"), "{\\tmp.jpg}".format(dir))
        return None
    else:
        imgdata = base64.b64decode(buffer)
        filename = "{}{}".format(cpath,"demo\\tmp\\tmp.jpg")  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print "ok"
        decimg = cv2.imread(filename)
        return decimg
  
while 1:
    img=getImageFromServer()
    if img != None:
        detect(img)
        bokeh = BokehDetector()
        print bokeh.getValue(img)
        cv2.imshow('Capture',img)
        key=cv2.waitKey(100)
        if(int(key)>27): break
    img=''
