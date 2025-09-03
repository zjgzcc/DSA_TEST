# 配置文件模块
import yaml
import logging
import os


class ConfigLoader:
    def __init__(self):
        self.config_data = {}

    def load_config(self, config_file_path):
        """加载YAML配置文件"""
        try:
            with open(config_file_path, 'r') as file:
                self.config_data = yaml.safe_load(file)
            self._set_defaults()  # 设置默认值
        except Exception as e:
            logging.error(f"加载配置文件失败: {str(e)}")
            raise

    def _set_defaults(self):
        """设置配置默认值"""
        defaults = {
            'timeout': 30,
            'confidence_threshold': 0.9,
            'retry_attempts': 3
        }
        for key, value in defaults.items():
            if key not in self.config_data:
                self.config_data[key] = value

    def get(self, key, default=None):
        """获取配置值"""
        return self.config_data.get(key, default)


# 使用示例
# config = ConfigLoader()
# config.load_config('config/device_config.yaml')
# TIMEOUT = config.get('timeout')
# CONFIDENCE = config.get('confidence_threshold')