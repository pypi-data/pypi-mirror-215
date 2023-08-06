from typing import Union

def aes_encrypt(key: Union[str, bytes], data: Union[str, bytes]) -> Union[str, bytes]:
    """
    使用 AES 密钥对数据进行加密。

    Args:
        key (str or bytes): AES 密钥，当 key 的类型为 bytes 时，长度必须为 16、24 或 32 字节。
        data (str or bytes): 需要加密的数据。

    Returns:
        str or bytes: 加密后的数据。
    """
    ...

def aes_decrypt(key: Union[str, bytes], encrypted_data: Union[str, bytes]) -> Union[str, bytes]:
    """
    使用 AES 密钥解密数据。

    Args:
        key (str or bytes): AES 密钥，当 key 的类型为 bytes 时，长度必须为 16、24 或 32 字节。
        encrypted_data (str or bytes): 需要解密的数据。

    Returns:
        str or bytes: 解密后的原始数据。
    """
    ...
