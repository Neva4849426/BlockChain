# import hashlib
# import json
# import string
from time import time
from hashlib import sha256
import json

# 需要注意两点：
# 1.商品信息编号从1开始
# 2.len(self.chain)会比记录的区块数多一，多存了一个初始时无data基础信息的编号为0的区块


class Blockchain(object):
    def __init__(self):
        """
        构造函数
        current_information 记录现在加进来的区块的data基础信息
        chain记录区块链
        new_block即为新区块:
        1.新建区块加入时，计算出5个满足与data相乘可得前两位为‘00’条件哈希值的随机数，5记为proof
        2.若中间修改区块，修改成功后将30记为proof
        """
        self.current_information = []
        self.chain = []
        # Create the genesis block55
        self.new_block(proof=5)

    def new_block(self, proof):
        # Creates a new Block and adds it to the chain
        """
        生成新块(插入区块时）
        新块中包含的基础信息包括：
        nb:区块序号；timest:时间戳（保存时间）；
        information:区块基础信息data;proof:加入区块时进行工作量证明机制的计算次数；
        previous_hash:前链，前一区块的哈希值；hash:由基础信息计算得的哈希值
        :param proof: <int> The proof given by the Proof of Work algorithm
        # :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'nb': len(self.chain),
            'timest': time(),
            'information': self.current_information,
            'proof': proof,
            'previous_hash': self.pre_hash(),
            'hash': self.hash_tr,
        }
        # Reset the current list of information
        self.current_information = []
        self.chain.append(block)
        return block

    def new_information(self, product_id, date, address, character, contact_info, description):
        # Adds a new informationto the list of information
        """
        生成新交易信息，信息将加入到下一个待挖的区块中
        :param product_id: The ID of the product(also is the ID of the blockchain)
        :param date: The time when the character edit the information
        :param address: The information of address
        :param character: The user's identity
        :param contact_info: The contact information of the user
        :param description: The description of the product
        :return: New block( The chain added 1)
        """
        self.current_information.append({
            'id': product_id,
            'time': date,
            'address': address,
            'character': character,
            'contact_info': contact_info,
            'description': description,
        })
        return self.last_block['nb'] + 1

    def get_information(self):
        return self.current_information

    @property
    def last_block(self):
        """
        获取区块链末尾区块
        :return:区块链末尾区块
        """
        # Returns the last Block in the chain
        return self.chain[-1]

    def pre_hash(self):
        """
        获得前链哈希值
        1.当区块链长度大于等于1时，返回已有区块链的末尾区块的哈希值
        2.当区块链长度为0时，返回初始第一个区块的前链哈希值为1111
        :return: 前链哈希值
        """
        if len(self.chain) >= 2:
            pre_block = self.chain[-1]
            pr_hash = pre_block['hash']
            return pr_hash
        else:
            return 1111

    # 设置为static的啦
    @staticmethod
    def proof_of_work_new(data):
        """
        工作量证明机制算法（新建区块时使用）
        用于检验是否可以新增
        返回值为True时可以新增
        :param data: The transition of basic data in the block(before using, encode the string type data of block)
        :return: When finds 100 nbs which can lead to the result with [:4] "0000",return the boolean type value true
        """
        num = 0
        y = -1
        while num != 5:
            y += 1
            while sha256(f'{data*y}'.encode()).hexdigest()[:2] != "00":
                y += 1
            print(sha256(f'{data*y}'.encode()).hexdigest())
            print(y)
            print(num)
            num += 1
        return True

    # 设置为static的啦
    @staticmethod
    def proof_of_work_edit(data):
        """
        工作量证明机制算法（编辑区块/篡改时使用）
        用于检验是否可以篡改
        返回值为True时可以篡改
        :param data: The transition of basic data in the block(before using, encode the string type data of block)
        :return: When finds 100 nbs which can lead to the result with [:4] "0000",return the boolean type value true
        """
        num = 0
        y = -1
        while num != 100:
            y += 1
            while sha256(f'{data*y}'.encode()).hexdigest()[:4] != "0000":
                y += 1
            print(sha256(f'{data*y}'.encode()).hexdigest())
            print(y)
            print(num)
            num += 1
        return True

    @staticmethod
    def hash_bl(block):
        # Hashes a Block
        """
        计算生成块内信息的 SHA-256 hash值(读取本地文件连成区块链时使用）
        利用block中的information量，首先将其变为一个将block内data各类型信息整合，以\t分隔的字符串，再对字符串进行哈希编码
        :return: <str>哈希值
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        data_hs = block['information']
        hash_val = sha256(f'{data_hs}'.encode()).hexdigest()
        return hash_val

    @property
    def hash_tr(self):
        # Hashes a Block
        """
        计算生成块内信息的 SHA-256 hash值（新建区块时使用，直接利用current_information计算)
        利用block中的information量，首先将其变为一个将block内data各类型信息整合，以\t分隔的字符串，再对字符串进行哈希编码
        :return: <str>哈希值
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        data_hs = self.current_information
        hash_val = sha256(f'{data_hs}'.encode()).hexdigest()
        return hash_val

    def inspect_hash(self, hash_mysql):
        """
        逐个检验数据库中的哈希值数组中的哈希值是否与区块链中各区块的哈希值相同
        :param hash_mysql: 数据库中记录的区块链哈希值数组（类型为字符串数组）
        :return:返回是否相同，若相同返回True，若其中任一不相同,则返回False
        """
        length = len(hash_mysql)
        i = 0
        while i < length:
            if self.chain[i + 1]['hash'] != hash_mysql[i]:
                return False
            i += 1
        return True

    def inspect_chain_form(self):
        """
        检验是否成链
        :return:布尔值:若对比中有任一区块的哈希值与下一区块的前链值不同，则返回False,都相同则返回True
        """
        length = len(self.chain)
        i = 1
        while i < length - 1:
            if self.chain[i + 1]['previous_hash'] != self.chain[i]['hash']:
                return False
            i += 1
        return True

    def rebuild_block(self, timest, proof, previous_hash, hash):
        # Creates a new Block and adds it to the chain
        """
        重建区块（从客户端获取区块信息重建区块链时使用）
        区块中包含的基础信息包括：
        nb:区块序号；timest:时间戳（保存时间）；
        information:区块基础信息data;proof:加入区块时进行工作量证明机制的计算次数；
        previous_hash:前链，前一区块的哈希值；hash:区块的哈希值
        :param timest: 客户端存储的时间戳
        :param proof: 客户端存储的工作量证明复杂度
        :param previous_hash: 客户端存储的区块前链哈希值
        :param hash: 客户端存储的区块哈希值
        :return: 重建区块
        """
        block = {
            'nb': len(self.chain),
            'timest': timest,
            'information': self.current_information,
            'proof': proof,
            'previous_hash': previous_hash,
            'hash': hash,
        }
        # Reset the current list of information
        self.current_information = []
        self.chain.append(block)
        return block

    def check_info_and_hash(self, message):
        """
        客户端比较商品信息与哈希值是否对应
        注：需要新建一个区块链再进行使用
        :param message:
        :return:
        """
        json_messages = message.split('\8')
        i = 1
        length = len(json_messages)
        while i < length - 1:
            if json_messages[i] != '':

                block = json.loads(json_messages[i].replace("'", '"'))
                bi = str(block['information'])
                bp = str(block['previous_hash'])
                data_hs = bi+bp
                hash_val = sha256(f'{data_hs}'.encode()).hexdigest()
                if block['hash'] != hash_val:
                    block['hash'] = hash_val
                self.chain.append(block)
            i += 1

    def get_chain(self,ID):                                                     #通过ID打开相应链文件，重建链
        path = "D:/configFiles/chain" + ID + ".json"
        # path = "static/blockAndChain/Chain1.json"
        block = {
            'nb': len(self.chain),
            'timest': timest,
            'information': self.current_information,
            'proof': proof,
            'previous_hash': previous_hash,
            'hash': hash,
        }
        # Reset the current list of information
        self.current_information = []
        self.chain.append(block)
        with open(path, 'r') as f:
            for line in f:
                if line != '' and line != '\n':
                    block = json.loads(line)
                    self.chain.append(block)
        self.current_information = []
        f.close()

    def getGoodID(self):
        """
        获取商品id
        已成链情况下
        :return:
        """
        block = self.chain[1]
        tr = block['information']
        id_of_good = tr[0]['id']
        return id_of_good