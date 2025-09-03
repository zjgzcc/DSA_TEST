# 基础页面对象模块
import pyautogui
import random
import time
import logging
from common.image_utils import ImageUtils


class BasePage:
    def __init__(self, config):
        self.config = config
        self.image_utils = ImageUtils(config.get('confidence_threshold'))
        self.timeout = config.get('timeout')
        self.retry_attempts = config.get('retry_attempts')

    def click_element(self, image_path, retries=None):
        """点击屏幕上的元素"""
        retries = retries or self.retry_attempts

        for attempt in range(retries):
            try:
                location = self.image_utils.find_element_on_screen(image_path)
                if location:
                    center = pyautogui.center(location)
                    # 添加随机偏移模拟人类操作
                    offset_x = random.randint(-3, 3)
                    offset_y = random.randint(-3, 3)
                    pyautogui.click(center.x + offset_x, center.y + offset_y)
                    logging.info(f"成功点击元素: {image_path}")
                    return True
                else:
                    logging.warning(f"未找到元素: {image_path}, 尝试 {attempt + 1}/{retries}")
                    time.sleep(1)
            except Exception as e:
                logging.error(f"点击元素时出错: {str(e)}")

        logging.error(f"所有尝试失败，无法点击元素: {image_path}")
        return False

    def wait_for_element(self, image_path, timeout=None):
        """等待元素出现在屏幕上"""
        timeout = timeout or self.timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            location = self.image_utils.find_element_on_screen(image_path)
            if location:
                return location
            time.sleep(0.5)

        logging.error(f"等待元素超时: {image_path}")
        return None


# 使用示例
# base_page = BasePage(config)
# base_page.click_element("resources/button_power.png")