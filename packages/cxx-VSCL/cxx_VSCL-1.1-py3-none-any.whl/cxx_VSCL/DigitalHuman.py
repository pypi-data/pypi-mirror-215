from cxx_VSCL.core import MyWS

# 数字人
class DigtalHuman():
    name='安琪拉'
    age=18
    sex=False #性别 true：男 ，false：女
    build=[]  #体型
    complexion=[]  #肤色
    voice=[]    #声音
    volume=1.0  #音量
    appearance=[] #容貌
    clothingList=['西装男','西装女','古装男','古装女'] #服装
    expression=[] #表情
    head_action=[] #头部动作
    hand_action=[] #手部动作
    Legsandtorso_action=[] #腿和躯干动作
    default_action=[] #默认动作无法定制


    def setName(self,name:str):
        """
        设置数字人名字
        :param name:
        :return: bool返回操作成功或失败
        """
        self.name=name
        result=MyWS.doAwait({'type': 'szr', 'commond': 'setName'})
        return  result["result"]


    def getInteractiveObjectInSence(self):
        """
        获取当前场景可交互元素
        :return: 返回元素字典
        """
        result = MyWS.doAwait({'type': 'sence', 'commond': 'getInteractiveObjectInSence'})
        return


def createDigtalHuman():
    """
    创建一个数字人
    :return: 返回唯一数字人对象
    """
    digtalHuman = DigtalHuman()
    return digtalHuman