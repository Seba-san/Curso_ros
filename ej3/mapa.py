
import rospy
from geometry_msgs.msg import Twist as robot_velocity_msg
from sensor_msgs.msg import LaserEcho as sensor_rango_msg
from std_srvs.srv import Trigger as velocidad_extra
from std_srvs.srv import Empty as saltar_caja__
from std_srvs.srv import SetBool as teletransportacion__
import random


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
        while not rospy.is_shutdown():
            msg=self.get_obstacles()
            self.pub.publish(self.laser_process(msg))
            rate.sleep()
            
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
            
    def crear_mapa(self):
        self.mapa=[[],[],[],[],[]]
        
        lista=[0,1,2,3]
        random.shuffle(lista)
        if lista[0]==0:
            self.mapa[0]=['pllp','plpl','plll','plpl','pppl']
            self.mapa[1]=['lplp','pllp','llcl','plll','pppl']
            self.mapa[2]=['lppi','lclp','kaja','lppc','pslp']
            self.mapa[3]=['pllp','llll','clcl','ppll','lplp']
            self.mapa[4]=['llpp','lcpl','kaja','llpl','lppl']
            self.pose_robot=[2,0]
            self.ganaste=[2,4]

        if lista[0]==1:
            self.mapa[0]=['pllp','ppll','ilpp','plpl','ppll']
            self.mapa[1]=['llcp','llll','plcl','ppll','lplp']
            self.mapa[2]=['kaja','lclc','kaja','lllc','lpll']
            self.mapa[3]=['cllp','lppl','clpp','lpll','lplp']
            self.mapa[4]=['llpp','plpl','ppsl','lppp','lppp']
            self.pose_robot=[0,2]
            self.ganaste=[4,2]
            
        if lista[0]==2:
            self.mapa[0]=['pllp','pcll','kaja','pllc','ppll']
            self.mapa[1]=['lplp','llpp','clcl','llll','lppl']
            self.mapa[2]=['lpps','pclp','kaja','lplc','pilp']
            self.mapa[3]=['plpp','llpl','clll','lppl','lplp']
            self.mapa[4]=['plpp','plpl','llpl','plpl','lppl']
            self.pose_robot=[2,4]
            self.ganaste=[2,0]
            
        if lista[0]==3:
            self.mapa[0]=['pplp','pplp','slpp','plpl','ppll']
            self.mapa[1]=['lplp','lllp','ppcl','pllp','lpcl']
            self.mapa[2]=['lllp','lcll','kaja','lclc','kaja']
            self.mapa[3]=['lplp','llpp','clpl','llll','cpll']
            self.mapa[4]=['llpp','plpl','ppil','llpp','lppl']
            self.pose_robot=[4,2]
            self.ganaste=[0,2]
        
    def get_obstacles(self):
        msg=self.mapa[self.pose_robot[0]][self.pose_robot[1]]
        return msg
    
    def check_pose(self):
        #print(self.pose_robot)
        if self.pose_robot[0]<0:
            self.pose_robot[0]=0
            rospy.logwarn('saliste del mapa')
        if self.pose_robot[1]<0:
            self.pose_robot[1]=0
            rospy.logwarn('saliste del mapa')
        if self.pose_robot[1]>4:
            self.pose_robot[1]=4
            rospy.logwarn('saliste del mapa')
        if self.pose_robot[0]>4:
            self.pose_robot[1]=4
            rospy.logwarn('saliste del mapa')
            
        if self.pose_robot==self.ganaste:
            rospy.logwarn('Felicitaciones completaste el mapa!!')
            print('Lo hiciste en '+str(self.cuenta)+' pasos')
            
    
    def move_robot(self,data=[]):
        #check if data is correct
        sum=data[0]+data[1]+data[2]+data[3]
        if sum!=1 and type(sum)==int:
            rospy.logwarn('el movimiento enviado no tiene el formato adecuado')
            
        msg=self.get_obstacles()
        #print(msg)
        idx=data.index(1)
        if msg[idx]=='l' or (self.teletrans and msg[idx]=='p'):
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
            rospy.logwarn('no puedes moverte hacia esa direccion. Hay un obstaculo')


def comenzar():
    pass

if __name__=='__main__':
    
    map=Mapa()
    map.run()
   
    #import pdb; pdb.set_trace()
    #print(map.mapa)
    
    
  