from hashlib import sha256

class Calculate(object):
    def proof_of_work_edit(self,transaction):
        """
        工作量证明机制算法（编辑区块/篡改时使用）
        用于检验是否可以篡改
        返回值为True时可以篡改
        :param data: The transition of basic data in the block(before using, encode the string type data of block)
        :return: When finds 100 numbers which can lead to the result with [:4] "0000",return the boolean type value true
        """
        num = 0
        y = 0
        data_t = str(transaction)
        while sha256(f'{data_t*y}'.encode()).hexdigest()[:7] != "0000000":
            y += 1
        hash_val = sha256(f'{data_t*y}'.encode()).hexdigest()
        proof_val = y
        return hash_val

    def proof_of_work_new(self,transaction):
        """v
        工作量证明机制算法（新建区块时使用）
        用于检验是否可以新增
        返回值为True时可以新增
        :param data: The transition of basic data in the block(before using, encode the string type data of block)
        :return: When finds 100 numbers which can lead to the result with [:4] "0000",return the boolean type value true
        """
        num = 0
        y = -1
        data_t = str(transaction)
        while num != 5:
            y += 1
            while sha256(f'{data_t*y}'.encode()).hexdigest()[:2] != "00":
                y += 1
            print(sha256(f'{data_t*y}'.encode()).hexdigest())
            print(y)
            print(num)
            num += 1
        return True

    def hash_bl(self, transactions):
        # Hashes a Block
        """
        计算生成块内信息的 SHA-256 hash值(读取本地文件连成区块链时使用）
        利用block中的transaction变量，首先将其变为一个将block内data各类型信息整合，以\t分隔的字符串，再对字符串进行哈希编码
        :return: <str>哈希值
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        y = 0
        data_t = str(transactions)
        while sha256(f'{data_t * y}'.encode()).hexdigest()[:2] != "00":
            y += 1
        hash_val = sha256(f'{data_t * y}'.encode()).hexdigest()
        proof_val = y
        ###################################### 咋整嘞，有两个值但是只能返回一个
        return hash_val