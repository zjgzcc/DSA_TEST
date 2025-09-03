# 系统开关机操作模块
import time
import logging
from core.base_page import BasePage


class SystemOperations(BasePage):
    def __init__(self, config):
        super().__init__(config)
        self.power_button = "resources/button_power.png"
        self.shutdown_button = "resources/button_shutdown.png"
        self.startup_complete_indicator = "resources/system_ready.png"

    def startup_system(self):
        """启动DSA系统"""
        logging.info("开始系统启动流程")

        # 点击电源按钮
        if not self.click_element(self.power_button):
            return False

        # 等待系统启动完成
        if not self.wait_for_element(self.startup_complete_indicator, timeout=120):
            logging.error("系统启动超时")
            return False

        logging.info("系统启动成功")
        return True

    def shutdown_system(self):
        """关闭DSA系统"""
        logging.info("开始系统关闭流程")

        # 点击关机按钮
        if not self.click_element(self.shutdown_button):
            return False

        # 等待系统完全关闭
        time.sleep(60)  # 根据实际系统调整等待时间
        logging.info("系统关闭成功")
        return True

    def restart_system(self):
        """重启系统"""
        if self.shutdown_system() and self.startup_system():
            logging.info("系统重启成功")
            return True
        return False


# 使用示例
# system_ops = SystemOperations(config)
# system_ops.startup_system()