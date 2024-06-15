import datetime
import logging
import os
from config import DEBUG, CONFIG, CURRENT_PATH


LOG_CONFIG = CONFIG.get("log", {})

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)  # 将日志输出至屏幕


if LOG_CONFIG.get("save_log", False):
    LOG_DIR = os.path.join(CURRENT_PATH, str(LOG_CONFIG.get("save_dir", "logs")))
    LOG_PATH = os.path.join(LOG_DIR, "%s.log" % str(datetime.date.today()))
    os.makedirs(LOG_DIR, exist_ok=True)
    fh = logging.FileHandler(filename=LOG_PATH, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 将日志输出至文件

logger.debug("日志初始化成功")
