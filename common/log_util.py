# 日志配置模块
import logging
import os
from datetime import datetime


def setup_logging(log_level=logging.INFO, log_dir="outputs/logs"):
    """配置日志系统"""
    try:
        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 生成带时间戳的日志文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"dsa_test_{timestamp}.log")

        # 配置日志格式和处理器
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        # 文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 根日志记录器配置
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        return root_logger
    except Exception as e:
        print(f"日志配置失败: {str(e)}")
        raise


# 使用示例
# logger = setup_logging()
# logger.info("日志系统初始化完成")