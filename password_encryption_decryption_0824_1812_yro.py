# 代码生成时间: 2025-08-24 18:12:16
import os
from celery import Celery
from cryptography.fernet import Fernet

# 创建Celery应用
app = Celery('password_tools', broker='pyamqp://guest@localhost//')

# 生成密钥
def generate_key():
    return Fernet.generate_key()

# 加密密码
@app.task
def encrypt_password(password, key):
    try:
        # 确保密钥是bytes类型
        if not isinstance(key, bytes):
            key = key.encode()

        # 创建Fernet实例
        cipher_suite = Fernet(key)

        # 加密密码
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password
    except Exception as e:
        return str(e)

# 解密密码
@app.task
def decrypt_password(encrypted_password, key):
    try:
        # 确保密钥是bytes类型
        if not isinstance(key, bytes):
            key = key.encode()

        # 创建Fernet实例
        cipher_suite = Fernet(key)

        # 解密密码
        decrypted_password = cipher_suite.decrypt(encrypted_password)
        return decrypted_password.decode()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # 生成密钥
    key = generate_key()

    # 加密示例密码
    encrypted = encrypt_password.delay('password123', key)
    print(f'Encrypted: {encrypted.get().decode()}')

    # 解密示例密码
    decrypted = decrypt_password.delay(encrypted.get(), key)
    print(f'Decrypted: {decrypted.get()}')