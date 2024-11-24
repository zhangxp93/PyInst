"""
日志处理
"""
import logging
import os
from logging.handlers import RotatingFileHandler
import colorlog  # 导入 colorlog
def setup_logging(log_file=None, log_level=logging.INFO, max_bytes=1 * 1024 * 1024, backup_count=5):
    """
    配置日志记录，包括日志轮换和控制台输出，支持彩色日志
    :param log_file: 日志文件路径，如果为None则使用默认路径
    :param log_level: 日志等级
    :param max_bytes: 单个日志文件的最大字节数，默认为1MB
    :param backup_count: 保留的日志文件备份数
    """
    if log_file is None:
        log_file = os.getenv('LOG_FILE_PATH', 'docs/log/test.log')

    # 确保日志文件夹存在
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建根记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # 清除已有的处理器，避免重复添加
    if logger.hasHandlers():
        logger.handlers.clear()

    # 创建文件处理器，支持日志轮换
    file_handler = RotatingFileHandler(log_file, mode='w', maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(log_level)

    # 创建控制台处理器，日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 定义日志格式
    log_format = '%(asctime)s - %(levelname)-8s - %(message)-60s - [%(filename)-15s:%(lineno)-4d]'
    color_format = "%(log_color)s" + log_format

    # 设置文件处理器的格式
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)

    # 设置控制台处理器的彩色格式
    color_formatter = colorlog.ColoredFormatter(
        color_format,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(color_formatter)

    # 将处理器添加到记录器中
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 添加日志分隔符
    logger.info("=" * 60)
    logger.info("新日志开始".center(60, ' '))
    logger.info("=" * 60)


def log_data(data):
    """
    记录数据的日志
    """
    logging.info(f"数据记录: {data}")


# 通用异常处理装饰器
def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"{func.__name__} 执行时发生错误", exc_info=True)
            raise e

    return wrapper

# 示例：调用日志设置
if __name__ == "__main__":
    setup_logging(log_file='/Users/zhangxianping/Desktop/pythonProject/SiCore_ChipTest/docs/log//test.log', log_level=logging.DEBUG)
    log_data("这是一个测试数据记录")
    logging.debug("这是一条调试信息")
    logging.warning("这是一条警告信息")
    logging.error("这是一条错误信息")
    logging.critical("这是一条严重错误信息")