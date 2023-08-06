# Copyright 2023 by Abner. All rights reserved.
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64


# 生成ECC公钥和私钥
def generate_ecc_keys(curve='256'):
    """
    使用选定的椭圆曲线生成ECC公钥和私钥对。

    Args:
        curve (str): 指定生成密钥对的椭圆曲线，可选值为 '256'、'384' 和 '521'，默认为 '256'。

    Returns:
        tuple: 一个包含私钥PEM和公钥PEM的元组。
    """
    # 定义不同的椭圆曲线参数
    curve_dict = {
        '256': ec.SECP256R1(),
        '384': ec.SECP384R1(),
        '521': ec.SECP521R1()
    }
    # 根据传入的曲线参数来选择使用的椭圆曲线
    curve = curve_dict.get(curve, ec.SECP256R1())
    # 生成ECC私钥
    private_key = ec.generate_private_key(curve)
    # 从私钥中获取ECC公钥
    public_key = private_key.public_key()

    # 将私钥转化为PEM格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 将公钥转化为PEM格式
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 返回PEM格式的公钥和私钥
    return str(private_pem, encoding="utf-8"), str(public_pem, encoding="utf-8")

# ECC加密
def ecc_encrypt(data, public_key, private_key):
    """
    使用ECC公钥和私钥对数据进行加密。

    Args:
        data (str or bytes): 需要加密的数据，数据类型为字符串或字节。
        public_key (str): 对方的PEM格式ECC公钥。
        private_key (str): 自己的PEM格式ECC私钥。

    Returns:
        str or bytes: 加密后的数据，返回的类型与传入的数据类型相同。
    """
    private_key = serialization.load_pem_private_key(
        private_key.encode(),
        password=None,
        backend=default_backend()
    )

    public_key = serialization.load_pem_public_key(
        public_key.encode(),
        backend=default_backend()
    )

    # 检查 data 类型并进行必要的转换
    if isinstance(data, str):
        data = data.encode()
        data_str = True
    else:
        data_str = False

    shared_key = private_key.exchange(ec.ECDH(), public_key)

    # Hash the shared key to get a 32-byte (256-bit) key
    shared_key_hash = hashes.Hash(hashes.SHA256())
    shared_key_hash.update(shared_key)
    derived_key = base64.urlsafe_b64encode(shared_key_hash.finalize())

    f = Fernet(derived_key)
    encrypted_data = f.encrypt(data)
    # 如果 data 为 str 则返回 str密文 ，否则返回 bytes
    return encrypted_data.decode('utf-8') if data_str else encrypted_data

# ECC解密
def ecc_decrypt(encrypted_data, public_key, private_key):
    """
    使用ECC公钥和私钥解密数据。

    Args:
        encrypted_data (str or bytes): 需要解密的数据，数据类型为字符串或字节。
        public_key (str): 对方的PEM格式ECC公钥。
        private_key (str): 自己的PEM格式ECC私钥。

    Returns:
        str or bytes: 解密后的原始数据，返回的类型与传入的数据类型相同。
    """
    private_key = serialization.load_pem_private_key(
        private_key.encode(),
        password=None,
        backend=default_backend()
    )

    public_key = serialization.load_pem_public_key(
        public_key.encode(),
        backend=default_backend()
    )

    # 检查 data 类型并进行必要的转换
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode()
        data_str = True
    else:
        data_str = False

    try:
        shared_key = private_key.exchange(ec.ECDH(), public_key)

        # Hash the shared key to get a 32-byte (256-bit) key
        shared_key_hash = hashes.Hash(hashes.SHA256())
        shared_key_hash.update(shared_key)
        derived_key = base64.urlsafe_b64encode(shared_key_hash.finalize())

        f = Fernet(derived_key)
        decrypted_data = f.decrypt(encrypted_data)
    except:
        raise Exception("无效的加密密钥或损坏的数据")

    # 如果 data 为 str 则返回 str明文 ，否则返回 bytes
    return str(decrypted_data, encoding="utf-8") if data_str else decrypted_data
