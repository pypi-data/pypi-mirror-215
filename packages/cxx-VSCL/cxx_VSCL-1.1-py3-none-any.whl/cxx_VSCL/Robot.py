from cxx_VSCL.core import MyWS

# 机器人
class Robot():
    name='阿尔法狗'
    breastpieceInfo='编号2210' #胸牌信息
    color='#ff00ff'

    def __init__(self):
        pass

    def setName(self,name:str):
        self.name=name
        result = MyWS.doAwait({'type': 'jqr', 'commond': 'setName'})
        return result["result"]


def createRobot():
    """
    创建一个机器人
    :return: 返回一个机器人对象
    """
    robot=Robot()
    return robot
