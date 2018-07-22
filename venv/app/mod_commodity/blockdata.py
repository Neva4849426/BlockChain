class BlockData:
    number = '00000'
    def __init__(self,number,blockList,position,person,tel,note):
        self.number = number              #商品编号
        self.blockList = blockList        #区块链信息
        self.position = position          #地点
        self.person = person              #人物
        self.tel = tel                    #联系方式
        self.note = note                  #备注
