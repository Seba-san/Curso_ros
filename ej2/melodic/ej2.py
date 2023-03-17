import rospy
from std_msgs.msg import String,Bool,Int16,Float32
import random


class EJ2:
    def __init__(self):
        self.f = open('archivo','r')
        self.escondido=self.f.readlines()
        #print(self.escondido)
        self.f.close()
        self.sub_4=rospy.Subscriber('paso_3', String,self.paso_3)
        self.sub_3=rospy.Subscriber('paso_2', Float32,self.paso_2)
        self.sub_2=rospy.Subscriber('paso_1', Int16,self.paso_1)
        self.sub_1=rospy.Subscriber('tu_nombre_paso_0', String,self.paso_0)
        self.pub = rospy.Publisher('respuesta', String, queue_size=10)
        rospy.init_node('ej2', anonymous=True)
        self.rate = rospy.Rate(10) # 10hz
       
        self.bandera=False
        self.msg=String()
        msg='Iniciando el ejercicio 2. Para comenzar debes publicar en el topic correcto tu nombre en minusculas.'
        rospy.loginfo(msg)
        self.msg.data=msg
        self.run()
        
    
    def run(self):
        while not rospy.is_shutdown():  
            if self.bandera:
                self.bandera=False                       
                self.pub.publish(self.msg)
                self.rate.sleep()
        

    def paso_3(self,data):
        idx=2
        self.bandera=True    
        cc=self.decript(self.escondido[idx][0:-1])
        dd=data.data
        if type(dd)==float:
            dd=round(dd,2)
        if type(dd)!=str:
            dd=str(dd)

        pos=cc.find(dd)
        if pos>-1:
            self.msg.data='Ejercicio finalizado!. Recuerda que cuando te pregunten tu clave es: '+dd         
        else:
            self.msg.data='codigo incorrecto'

    def paso_2(self,data):
        idx=2
        self.process_(data,idx)


    def paso_1(self,data):
        idx=1
        self.process_(data,idx)


    def paso_0(self,data):
        idx=0
        self.process_(data,idx)

    def process_(self,data,idx):
        self.bandera=True    
        cc=self.decript(self.escondido[idx][0:-1])
        dd=data.data
        if type(dd)==float:
            dd=round(dd,2)
        if type(dd)!=str:
            dd=str(dd)

        pos=cc.find(dd)
        if pos>-1:
            nn=len(dd)
            txt=cc[pos+nn:].split()
            self.msg.data=txt[0]            
        else:
            self.msg.data='codigo incorrecto'

    def decript(self,data):
        in_=''
        for d_ in data:
            asd=ord(d_)+ord(data[0])-122
            in_=in_+chr(asd)
        return in_[1:]

    def encript(self,data):        
        d__=random.randint(97,122)
        in_=''        
        in_=in_+chr(d__)
        for d_ in data:
            asd=ord(d_)-ord(in_[0])+122
            in_=in_+chr(asd)                
        return in_

        
    

if __name__=='__main__':
    try:
        ej=EJ2()
        ej.f.close()
    except rospy.ROSInterruptException:
        pass
        
    
    