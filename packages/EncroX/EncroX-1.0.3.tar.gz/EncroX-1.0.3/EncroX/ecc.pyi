from typing import Tuple, Union


def generate_ecc_keys(curve: str = '256') -> Tuple[str, str]:
    """
    使用选定的椭圆曲线生成ECC公钥和私钥对。

    Args:
        curve (str): 指定生成密钥对的椭圆曲线，可选值为 '256'、'384' 和 '521'，默认为 '256'。

    Returns:
        tuple: 一个包含私钥PEM和公钥PEM的元组。
    """
    ...


def ecc_encrypt(data: Union[str, bytes], public_key: str, private_key: str) -> Union[str, bytes]:
    """
    使用ECC公钥和私钥对数据进行加密。

    Args:
        data (str or bytes): 需要加密的数据，数据类型为字符串或字节。
        public_key (str): 对方的PEM格式ECC公钥。
        private_key (str): 自己的PEM格式ECC私钥。

    Returns:
        str or bytes: 加密后的数据，返回的类型与传入的数据类型相同。
    """
    ...


def ecc_decrypt(encrypted_data: Union[str, bytes], public_key: str, private_key: str) -> Union[str, bytes]:
    """
    使用ECC公钥和私钥解密数据。

    Args:
        encrypted_data (str or bytes): 需要解密的数据，数据类型为字符串或字节。
        public_key (str): 对方的PEM格式ECC公钥。
        private_key (str): 自己的PEM格式ECC私钥。

    Returns:
        str or bytes: 解密后的原始数据，返回的类型与传入的数据类型相同。
    """
    ...
