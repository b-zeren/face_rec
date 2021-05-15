#-*- coding: UTF-8-*-
import cv2
from cv2 import face
from time import sleep
import sqlite3
import numpy as np
import smtplib
from PIL import Image

def getImage():                    
      images=[]
      labels=[]
      
      cur.execute('''SELECT ogrno, profil, profil2, profil3 FROM bilgiler ''')
      c=cur.fetchall()
      for row in c:
       (n,rb,ri,ru)=row
       
       rb=np.array(rb,"uint8")
       
       labels.append(n)
       images.append(rb)
       rb=np.array(ri,"uint8")
       
       labels.append(n)
       images.append(ri)
       rb=np.array(ru,"uint8")
       
       labels.append(n)
       images.append(ru)
      
       
      return images,np.array(labels)  

		
		
def egitim():
  
     resimler,nolar=getImage()
     rec = cv2.createLBPHFaceRecognizer()
     rec.train(resimler,nolar)
     print "oldu"
  
        


def gecis():
    sec=raw_input("Yoklama almak iÃ§in enter tuÅŸuna, yeni Ã¶ÄŸrenci eklemek iÃ§in y tuÅŸuna basÄ±nÄ±z")
    if(len(sec)<1):
        egitim()
        yoklama()
        onay=raw_input("YoklamayÄ± onaylÄ±yorsanÄ±z enter tuÅŸuna basarak gÃ¶nderin, tekrar yoklama almak istiyorsanÄ±z y tuÅŸuna basÄ±n")
        if(len(onay)<1):
            gonder(a,s,d,f,g,h)
            print "Yoklama baÅŸarÄ±yla alÄ±ndÄ±"
        else:
            egitim()
            yoklama()
    else:
        yenikullan()
     
def yoklama():                          
    nolar=unique(nolar)
    
    i=0
    while(i<=16):
        cam=cv.VideoCapture(1)                                         
        ret,img=cam.read()
        foto=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                     
     
        faceDetect= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces=faceDetect.detectMultiScale(foto,1.3,5)                    
     
        for x,y,w,h in faces:
            cv2.rectangle(foto,(x,y),(x+w,y+h),(255,0,0),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])                    
            if id in nolar:                                           
                nolar.remove(id)
                continue
        time.sleep(100)
        i=i+1                                                         
       
    sayi=0
    mgs=""
    for person in nolar:
        cur.execute('''SELECT ogrno, isim, soyad FROM bilgiler WHERE ogrno=?''',(person, ))
        bbb= cur.fetchone()
        print bbb[0], bbb[1], bbb[2], "bulunamadÄ±"
        mgs=mgs + bbb[0] + " " + bbb[1] + " " + bbb[2]+ "/n" #olmayan kiÅŸilerin adÄ±nÄ± mesaja ekliyor
        sayi=sayi+1                                    #olmayan kiÅŸileri sayÄ±yor
    edit= str(sayi) + "kiÅŸi bulunamadÄ±"
    mgs=mgs+edit
    return mgs   


def gonder(sender,receiver,usrname,password,mgs):  #mÃ¼dÃ¼r yardÄ±mcÄ±sÄ±na mail gÃ¶nderiyor

     fromaddr = sender    #gÃ¶nderici adres
     toaddrs  = receiver  #mÃ¼dÃ¼r yardÄ±mcÄ±sÄ± adresi

     username = usrname   #gÃ¶nderici adresin ÅŸifresi
     password = password
     
     try:
         server = smtplib.SMTP('smtp.gmail.com:587')
         server.starttls()
         server.login(username,password)
         server.sendmail(fromaddr, toaddrs, msg)
         server.quit()
     except SMTPException:
         print "Yoklama gÃ¶nderilemedi"	
		 
		 
		 
def yenikullan():                   
    no=raw_input("Ã–ÄŸrenci no giriniz:")
    isim= raw_input("Ä°sim giriniz:")
    soyad= raw_input("Soyisim giriniz:")
    print "Resimler iÃ§in kamera baÅŸlatÄ±lÄ±yor"
     
    c1=cv2.VideoCapture(1)
    f1,i1=c1.read()
    r1=cv2.cvtColor(i1,cv2.COLOR_BGR2GRAY)
    time.sleep(10)
     
    c2=cv2.VideoCapture(1)
    f2,i2=c2.read()
    r2=cv2.cvtColor(i2,cv2.COLOR_BGR2GRAY)
    time.sleep(10)
      
    c3=cv2.VideoCapture(1)
    f3,i3=c3.read()
    r3=cv2.cvtColor(i3,cv2.COLOR_BGR2GRAY)
    time.sleep(10)
     
    cv2.imshow(r1)
    cv2.imshow(r2)
    cv2.imshow(r3)
     
    cur.execute('''INSERT INTO bilgiler (ogrno,isim,soyad,profil,profil2,profil3) values(?,?,?,?,?,?)''',(no,isim,soyad,r1,r2,r3)) 
    cur.commit()
    cv2.destroyAllWindows()
    print "KullanÄ±cÄ± %s %s kaydedildi" %(isim,soyad)
    gecis()

	
conn=sqlite3.connect("database path")
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS bilgiler (ogrno INTEGER PRIMARY KEY UNIQUE, isim STRING, soyad STRING, profil BLOB, profil2 BLOB, profil3 BLOB)''')#veritabanÄ± yoksa yarat


print "Otomatik Yoklama"
gecis()


