from cxx_VSCL.core import MyWS

Number=0

# 无人机
class UAV():
    #编号
    number=0
    #位置
    posx=0;
    posy=0;

    def __init__(self,point:[float,float]):
        """
        无人机构造函数
        :param point: 设置无人机生成位置
        """
        global Number
        Number+=1
        self.number=Number
        self.posx=point[0]
        self.posy=point[1]
        result=MyWS.doAwait({'type':'wrj','commond':'create','pos':point,'number':self.number})
        if(result['result']==1):
            print('创建成功:' + str(self.number));

    def start(self):
        """
        起飞
        """
        result = MyWS.doAwait({'type': 'wrj', 'commond': 'start','number':self.number})
        if(result['result']==1):
            print('启动成功:' +str(self.number))

    def stop(self):
        """
        关闭
        """
        result = MyWS.doAwait({'type': 'wrj', 'commond': 'stop', 'number': self.number})
        if(result['result']==1):
            print('关闭成功:' + str(self.number))

    def flyByDirection(self,direction:str,speed:float,time:float):
        """
        无人机朝一个方向，以一定速度飞行一定时间
        :param direction: 飞行方向，支持"forward","back","left,"right"
        :param speed: 飞行速度（米/秒）
        :param time: 飞行时间（秒）
        """
        result = MyWS.doAwait({'type': 'wrj', 'commond': 'flyByDirection', 'number': self.number, 'dir':direction, 'speed':speed, 'time':time})
        if(result['result']==1):
            print('飞行完成：' + str(self.number))



