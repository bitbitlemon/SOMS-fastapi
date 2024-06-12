from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import MYSQL_CONFIG
from log import logger


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}".format(
    MYSQL_CONFIG.get("username", "root"),
    MYSQL_CONFIG.get("password", "root"),
    MYSQL_CONFIG.get("address", "127.0.0.1:3306"),
    MYSQL_CONFIG.get("database", "coms"),
)

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 声明基类
Base = declarative_base()

# 测试数据库连接
try:
    engine.connect()
    logger.debug("MySQL数据库连接成功!")
except Exception as e:
    logger.error(f'数据库连接失败! 请检查配置文件和数据库是否正确! error message: {e}')
    import sys
    sys.exit(0)



