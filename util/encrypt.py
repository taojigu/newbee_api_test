
import hashlib

class Encrypt:
    @staticmethod
    def md5_encrypt(password:str) -> str:
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        return md5_hash


if __name__ == "__main__":
    password = "123456"
    encrypted_password = Encrypt.md5_encrypt(password)
    print(f"Encrypted password: {encrypted_password}")
