
import rospy
from geometry_msgs.msg import Twist as robot_velocity_msg
from sensor_msgs.msg import LaserEcho as sensor_rango_msg
from std_srvs.srv import Trigger as velocidad_extra
from std_srvs.srv import Empty as saltar_caja__
from std_srvs.srv import SetBool as teletransportacion__
import random
import sys
import numpy as np


class Mapa:
    def __init__(self):
        self.crear_mapa()
       
        self.pub=rospy.Publisher('/sensor',sensor_rango_msg,queue_size=1)
        self.sub=rospy.Subscriber('/robot_velocity',robot_velocity_msg,self.pose_process,queue_size=1)
        self.service_velocidad=rospy.Service('/velocidad',velocidad_extra,self.set_extra_velocidad)
        self.service_saltar_caja=rospy.Service('/saltar_caja',saltar_caja__,self.set_saltar_caja)
        #self.service_teletransportarse=rospy.Service('/teletransportacion',teletransportacion__,self.teletransportarse)
        self.service_paredes=rospy.Service('/pasar_paredes',teletransportacion__,self.pasar_paredes)
        self.service_ayuda=rospy.Service('/ayuda',teletransportacion__,self.ayuda)
        self.cuenta=0
        self.ayuda_veces=1
        self.vel_extra=1
        self.teletrans=False
        self.saltar_caja=False
        self.fin=False
        
    def ayuda(self,data=teletransportacion__._request_class()):
        if self.ayuda_veces==0:
            msg=teletransportacion__._response_class()
            msg.success=False
            msg.message="Ya consumiste todas las ayudas"
            return msg
            
        self.ayuda_veces= self.ayuda_veces-1  
        self.saltar_paredes=True
        msg=teletransportacion__._response_class()
        msg.success=True
        msg.message="el siguiente movimiento no cuenta"
        self.cuenta=self.cuenta-1
        return msg
    
    def pasar_paredes(self,data=teletransportacion__._request_class()):
        self.teletrans=True
        msg=teletransportacion__._response_class()
        msg.success=True
        msg.message="En el proximo movimiento podras saltar las paredes cercanas "
        return msg
    
    def teletransportarse(self,data=teletransportacion__._request_class()):
        self.teletrans=True
        msg=teletransportacion__._response_class()
        msg.success=True
        msg.message="En el proximo movimiento podras moverte a cualquier espacio libre en cualquier direccion"
        return msg
    
    def set_saltar_caja(self,data=saltar_caja__._request_class()):
        self.saltar_caja=True
        msg=saltar_caja__._response_class()
        return msg
        
    def set_extra_velocidad(self,data=velocidad_extra._request_class()):
        self.vel_extra=2
        msg=velocidad_extra._response_class()
        msg.success=True
        msg.message="Obtienes +1 en el proximo movimiento"
        return msg
    
    def run(self):
        rospy.init_node('map_gestor')
        rate=rospy.Rate(1)
        rospy.loginfo('Mapa del laberinto listo')
        while not rospy.is_shutdown() and not self.fin:
            msg=self.get_obstacles()
            self.pub.publish(self.laser_process(msg))
            rate.sleep()
        
        rospy.loginfo('mapa terminado')
            
    def laser_process(self,msg):
        # Transforma desde la codificacion del mapa a un arreglo de float
        D={'l':0.0,'p':1.0,'c':0.5,'s':1000.0,'i':-1.0}
        data=sensor_rango_msg()
        for i in msg:
            data.echoes.append(D[i])
        
        return data
            
    def pose_process(self,data=robot_velocity_msg):
        # Transforma desde la velocidad a una lista
        self.cuenta=self.cuenta+1
        x=int(data.linear.x)
        y=int(data.linear.y)
        for i in range( self.vel_extra):
            if x!=0:
                if x>0:
                    self.move_robot([0,1,0,0])
                else:
                    self.move_robot([0,0,0,1])
            else:
                if y>0:                
                    self.move_robot([1,0,0,0])
                else:
                    self.move_robot([0,0,1,0])
                    
        self.vel_extra=1
    
    def mapa_base(self):
        self.mapa=[[],[],[],[],[],[],[],[],[]]
        self.mapa[0]=['p','p','p','p','p','p','p','p','p']
        self.mapa[1]=['p','l','l','l','l','l','l','l','p']
        self.mapa[2]=['p','l','p','p','l','p','p','p','p']
        self.mapa[3]=['p','i','p','l','l','l','l','l','p']
        self.mapa[4]=['p','p','p','l','c','l','p','p','p']
        self.mapa[5]=['p','l','l','l','l','p','p','l','s']
        self.mapa[6]=['p','p','p','l','l','l','p','l','p']
        self.mapa[7]=['p','l','l','l','c','l','l','l','p']
        self.mapa[8]=['p','p','p','p','p','p','p','p','p']
        
        
    
    def crear_mapa(self):
        self.mapa_base()
        #import pdb; pdb.set_trace()
        np.array(self.mapa)
        lista=[0,1,2,3,4,5,6,7,8]
        random.shuffle(lista)
        if lista[0]==0:
            tmp=np.array(self.mapa)
            self.mapa=np.flip(tmp,axis=0).tolist()
        if lista[0]==1:
            tmp=np.array(self.mapa)
            self.mapa=np.flip(tmp,axis=1).tolist()
        if lista[0]==2:
            tmp=np.array(self.mapa)
            tmp=np.flip(tmp,axis=0)
            self.mapa=np.flip(tmp,axis=1).tolist()            
        if lista[0]==3:
            tmp=np.array(self.mapa)
            self.mapa=np.rot90(tmp).tolist() 
        if lista[0]==4:
            tmp=np.array(self.mapa)
            self.mapa=np.rot90(np.rot90(tmp)).tolist() 
        if lista[0]==5:
            tmp=np.array(self.mapa)
            self.mapa=np.rot90(np.rot90(np.rot90(tmp))).tolist() 
        if lista[0]==6:
            pass
        if lista[0]==7:
            tmp=np.array(self.mapa)
            self.mapa=np.flip(np.rot90(tmp),axis=0).tolist() 
        if lista[0]==8:
            tmp=np.array(self.mapa)
            self.mapa=np.flip(np.rot90(tmp),axis=1).tolist() 
        # Se puede hacer de forma sistematica una rotacion y un flip
            
        #print('mapa numero: '+ str(lista[0]))
        #import pdb; pdb.set_trace()
        k=0
        for i in self.mapa:
            if 'i' in i:
                a=i.index('i')
                break
            k=k+1
            
        self.pose_robot=[k,a]        
        return
        
    def get_obstacles(self):
        """
        n e s o
        """
        x=self.pose_robot[0];y=self.pose_robot[1]
        e=self.mapa[x][y+1]
        s=self.mapa[x+1][y]
        o=self.mapa[x][y-1]
        n=self.mapa[x-1][y]
        msg=n+e+s+o
        #print(msg)
        return msg
    
    def check_pose(self):
        #print(self.pose_robot)
        a=len(self.mapa[0])
        if self.pose_robot[0]<0:
            self.pose_robot[0]=0
            rospy.logwarn('saliste del mapa')
        if self.pose_robot[1]<0:
            self.pose_robot[1]=0
            rospy.logwarn('saliste del mapa')
        if self.pose_robot[1]>a:
            self.pose_robot[1]=a
            rospy.logwarn('saliste del mapa')
        if self.pose_robot[0]>a:
            self.pose_robot[0]=a
            rospy.logwarn('saliste del mapa')
        x=self.pose_robot[0];y=self.pose_robot[1]
        n=self.mapa[x][y]
        if 's'==n:
            rospy.logwarn('Felicitaciones completaste el mapa!!')
            print('Lo hiciste en '+str(self.cuenta)+' pasos')
            self.fin=True
            
    
    def move_robot(self,data=[]):
        #check if data is correct
        sum=data[0]+data[1]+data[2]+data[3]
        if sum!=1 and type(sum)==int:
            rospy.logwarn('el movimiento enviado no tiene el formato adecuado')
            
        msg=self.get_obstacles()
        #print(msg)
        idx=data.index(1)
        if msg[idx]=='l' or msg[idx]=='s' or(self.teletrans and msg[idx]=='p'):
            self.teletrans=False
            if idx==0:
                self.pose_robot[0]=self.pose_robot[0]-1
            if idx==1:
                self.pose_robot[1]=self.pose_robot[1]+1
            if idx==2:
                self.pose_robot[0]=self.pose_robot[0]+1
            if idx==3:
                self.pose_robot[1]=self.pose_robot[1]-1
            self.check_pose()
                
        elif msg[idx]=='c' and self.saltar_caja:
            self.saltar_caja=False
            if idx==0:
                self.pose_robot[0]=self.pose_robot[0]-2
            if idx==1:
                self.pose_robot[1]=self.pose_robot[1]+2
            if idx==2:
                self.pose_robot[0]=self.pose_robot[0]+2
            if idx==3:
                self.pose_robot[1]=self.pose_robot[1]-2
            self.check_pose()
                
            if self.pose_robot[0]==5 and self.pose_robot[1]==5:
                self.pose_robot=[3,2]
                rospy.logwarn('no puedes moverte hacia esa direccion. Saliste del mapa, vuelves a la posicion anterior')  
                 
        else:
            #import pdb; pdb.set_trace()
            rospy.logwarn('no puedes moverte hacia esa direccion. Hay un obstaculo')


def comenzar():
    pass

if __name__=='__main__':
    
    map=Mapa()
    map.run()
   
    #import pdb; pdb.set_trace()
    #print(map.mapa)
    
    
  