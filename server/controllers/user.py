from datetime import timedelta, datetime
from jose import JWTError, jwt
from config import CONFIG


SECRET_CONFIG = CONFIG.get("secret", {})
SECRET_KEY = SECRET_CONFIG.get("secret_key", "")
ALGORITHM = SECRET_CONFIG.get("algorithm", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = SECRET_CONFIG.get("expire_time", 1440)


def create_access_token(data: dict) -> str:
    """
    生成access token
    :param data: 加密的内容
    :return: (str)access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


