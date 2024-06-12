import os
import yaml


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def load_config(config_path) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


# 加载配置文件
CONFIG = load_config(os.path.join(CURRENT_PATH, "config.yml"))
# 是否开启debug模式
DEBUG = CONFIG.get("debug", False)

MYSQL_CONFIG = CONFIG.get("mysql", {})
# 读取数据库环境变量
if MYSQL_CONFIG.get("use_env"):
    username = os.environ.get("MYSQL_USERNAME", 'root')
    password = os.environ.get("MYSQL_PASSWORD", 'root')
    db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
    MYSQL_CONFIG["username"] = username
    MYSQL_CONFIG["password"] = password
    MYSQL_CONFIG["address"] = db_address
