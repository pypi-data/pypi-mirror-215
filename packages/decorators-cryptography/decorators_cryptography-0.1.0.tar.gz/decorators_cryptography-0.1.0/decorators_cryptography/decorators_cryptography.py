import base64
import binascii

from cryptography.fernet import Fernet

from .exceptions import KeyInvalid


def validate_key(key):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                key64 = base64.urlsafe_b64decode(key)
            except binascii.Error as exc:
                raise KeyInvalid("Key decoding error: binascii.Error") from exc
            if len(key64) != 32:
                raise KeyInvalid("Wrong key length: ValueError")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def encrypt(key: str):
    def decorator(func):
        @validate_key(key)
        def wrapper(*args, **kwargs):
            fernet = Fernet(key)
            result = func(*args, **kwargs)
            return fernet.encrypt(result.encode()).decode()

        return wrapper

    return decorator


def decrypt(key: str):
    def decorator(func):
        @validate_key(key)
        def wrapper(*args, **kwargs):
            fernet = Fernet(key)
            result = func(*args, **kwargs)
            return fernet.decrypt(result.encode()).decode()

        return wrapper

    return decorator
