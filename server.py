# -*- coding:utf-8 -*-
import socket
import sys
import numpy
import cv2
import base64
import shutil
import os
import pickle
from face_detector import detect
from bokeh_calculator import BokehDetector

ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print ip
serversock.bind((ip,1234)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

cpath = "C:\\Users\\120350181\\Desktop\\"
dbpath = "{}{}".format(cpath,"demo\\tmp\\test.ldb")

def getImageFromServer():
    print 'Waiting for connections...'
    clientsock, client_address = serversock.accept() #接続されればデータを格納

    recvlen=100
    buffer=''
    
    while recvlen>0:
        rcvmsg=clientsock.recv(1024*8)
        recvlen=len(rcvmsg)
        buffer +=rcvmsg
    #print buffer
    if buffer.find('Name:') == 0:
        name = buffer.strip("Name:")
        print "name is"
        print name
        
        if not os.path.isfile(dbpath):
            counter = 0
            appendix = {counter:name}
            with open(dbpath, 'wb') as f:
                pickle.dump(appendix, f)
            print('new data:\n'+str(appendix))
        else:
            with open(dbpath, 'rb') as f:
                data = load_dumps(f)
            print('load data:\n'+str(data))
        
            counter = len(data)
            appendix = {counter:name}
            # try append
            with open(dbpath, 'ab') as f:
                pickle.dump(appendix, f)
            print('appendix:\n'+str(appendix))
        
        with open(dbpath, 'rb') as f:
            data = load_dumps(f)
        print('pickle data:\n'+str(data))
        print("ueda:"+str(data[counter])) 
        dir = "{}demo\\{}".format(cpath,counter)
        print "dir is"
        print dir
        if not os.path.isdir(dir):
            os.makedirs(dir)
        shutil.move("{}{}".format(cpath,"demo\\tmp\\tmp.jpg"), "{}\\tmp.jpg".format(dir))
        return None
    else:
        imgdata = base64.b64decode(buffer)
        filename = "{}{}".format(cpath,"demo\\tmp\\tmp.jpg")  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print "ok"
        decimg = cv2.imread(filename)
        return decimg
        
def load_dumps(f):
    obj = {}
    while 1:
        try:
            obj.update(pickle.load(f))
        except:
            break
    return obj
  
while 1:
    img=getImageFromServer()
    if not img is None:
        detect(img)
        bokeh = BokehDetector()
        print bokeh.getValue(img)
        #cv2.imshow('Capture',img)
        #key=cv2.waitKey(100)
        #if(int(key)>27): break
    img=''
