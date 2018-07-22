from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import padding

# 定义辅助函数，用于打印16进制数据
def dump_hex(buffer, sep=' ', indent=0, line_size=16):
    """
    辅助函数，将bytes数组以如下格式打印输出：
    0000: 40 71 37 d0 80 32 7f 04 d9 6d fb fc f7 6a 7d d4
    0010: 48 ad 75 79 7a 0d 6c 55 01 ed 45 d5 1e 75 33 a6
    :param buffer: 待打印数据
    :param sep: 各16进制数据之间的分隔符，默认用空格' '分隔
    :param indent: 打印输出前是否需要缩进，默认不缩进
    :param line_size: 每行输出16进制的数量，默认1行输出16个
    :return: 无返回值
    """
    # 计算缩进空格数
    leading = '%s' % ' '*indent
    # 循环打印每行16进制数据
    for x in range(0, len(buffer), line_size):
        # 打印缩进字符和当前行数据的起始地址
        print('%s%04X: ' % (leading, x), end='')
        # 将当前行数据制作成列表list，并打印
        line = ['%02x' % i for i in buffer[x:x+line_size]]
        print(*line, sep=sep, end='\n')


# 加密函数
def encrypt(src_file_name, dst_file_name, public_key_file_name):
    """
    对原始数据文件使用指定的公钥进行加密，并将加密输出到目标文件中
    :param src_file_name: 原始数据文件
    :param dst_file_name: 加密输出文件
    :param public_key_file_name: 用于加密的公钥
    :return: 加密结果的bytes数组
    """
    # 读取原始数据
    data_file = open(src_file_name, 'rb')
    data = data_file.read()
    data_file.close()

    # 读取公钥数据
    key_file = open(public_key_file_name, 'rb')
    key_data = key_file.read()
    key_file.close()

    # 从公钥数据中加载公钥
    public_key = serialization.load_pem_public_key(
        key_data,
        backend=default_backend()
        )

    # 使用公钥对原始数据进行加密，使用PKCS#1 v1.5的填充方式
    out_data = public_key.encrypt(
        data,
        padding.PKCS1v15()
    )

    # 将加密结果输出到目标文件中
    # write encrypted data
    out_data_file = open(dst_file_name, 'wb')
    out_data_file.write(out_data)
    out_data_file.close()

    # 返回加密结果
    return out_data


# 解密函数
def decrypt(src_file_name, dst_file_name, private_key_file_name):
    """
    对原始数据文件使用指定的私钥进行解密，并将结果输出到目标文件中
    :param src_file_name: 原始数据文件
    :param dst_file_name: 解密输出文件
    :param private_key_file_name: 用于解密的私钥
    :return: 解密结果的bytes数组
    """
    # 读取原始数据
    data_file = open(src_file_name, 'rb')
    data = data_file.read()
    data_file.close()

    # 读取私钥数据
    key_file = open(private_key_file_name, 'rb')
    key_data = key_file.read()
    key_file.close()
    code_p = '123456'
    # 从私钥数据中加载私钥
    private_key = serialization.load_pem_private_key(
        key_data,

        password=code_p.encode(),
        backend=default_backend()
    )

    # 使用私钥对数据进行解密，使用PKCS#1 v1.5的填充方式
    out_data = private_key.decrypt(
        data,
        padding.PKCS1v15()
    )

    # 将解密结果输出到目标文件中
    out_data_file = open(dst_file_name, 'wb')
    out_data_file.write(out_data)
    out_data_file.close()

    # 返回解密结果
    return out_data

"""
if __name__ == "__main__":
    data_file_name = r'C:\demos\message\msg.bin'
    encrypted_file_name = r'C:\demos\message\msg.bin.encrypted'
    decrypted_file_name = r'C:\demos\message\msg.bin.decrypted'

    private_key_file_name = r'C:\demos\private\Key.pem'
    public_key_file_name = r'C:\demos\private\Key_pub.pem'

    # 先对数据加密
    data = encrypt(data_file_name, encrypted_file_name, public_key_file_name)
    # 打印加密结果
    print("encrypted data:")
    dump_hex(data)

    # 对数据进行解密
    data = decrypt(encrypted_file_name, decrypted_file_name, private_key_file_name)
    # 打印解密结果
    print("decrypted data:")
    dump_hex(data)

"""
