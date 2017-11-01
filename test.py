# -*- coding: utf-8 -*-
import socket
from tqdm import tqdm
f = open("ok.txt", "w")
for j in tqdm(range(1,254)):
    for i in range(1,254):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sk.settimeout(0.5)

        ip = "175.43."+str(j)+"."+str(i)
        try:
            sk.connect((ip,37777))
            
            f.write(ip +':'+'Server port 3777 OK!' + "\n")
            print ip +':'+'Server port 3777 OK!'
            
        except Exception:
            a=1
            #print "wait....."
            #print ip +':'+'Server port 3777 not connect!'
        sk.close()
f.close()