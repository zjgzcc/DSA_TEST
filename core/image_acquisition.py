# 图像采集模块
import time
import logging
from core.base_page import BasePage
from common.image_utils import ImageUtils


class ImageAcquisition(BasePage):
    def __init__(self, config):
        super().__init__(config)
        self.exposure_button = "resources/button_exposure.png"
        self.image_utils = ImageUtils()
        self.acquisition_timeout = 300  # 5分钟超时

    def acquire_image(self, protocol_settings):
        """采集图像"""
        logging.info("开始图像采集流程")

        # 设置采集参数
        if not self._set_acquisition_parameters(protocol_settings):
            return False

        # 点击曝光按钮
        if not self.click_element(self.exposure_button):
            return False

        # 等待图像采集完成
        image_ready = self._wait_for_image_ready()
        if not image_ready:
            logging.error("图像采集超时")
            return False

        # 保存图像
        image_path = self._save_acquired_image()
        logging.info(f"图像采集完成: {image_path}")
        return image_path

    def _set_acquisition_parameters(self, protocol_settings):
        """设置采集参数（内部方法）"""
        try:
            # 设置KV值
            if 'kv' in protocol_settings:
                self._set_parameter('kv_setting.png', protocol_settings['kv'])

            # 设置MA值
            if 'ma' in protocol_settings:
                self._set_parameter('ma_setting.png', protocol_settings['ma'])

            # 设置其他参数...
            return True
        except Exception as e:
            logging.error(f"设置采集参数失败: {str(e)}")
            return False

    def _wait_for_image_ready(self):
        """等待图像就绪"""
        start_time = time.time()
        image_ready_indicator = "resources/indicator_image_ready.png"

        while time.time() - start_time < self.acquisition_timeout:
            if self.find_element_on_screen(image_ready_indicator):
                return True
            time.sleep(2)

        return False

    def _save_acquired_image(self):
        """保存采集的图像"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        image_path = f"outputs/images/acquired_image_{timestamp}.png"

        # 点击保存按钮
        self.click_element("resources/button_save_image.png")

        # 输入文件名
        self.click_element("resources/field_filename.png")
        pyautogui.write(image_path)
        pyautogui.press('enter')

        return image_path


# 使用示例
# image_acq = ImageAcquisition(config)
# protocol_settings = {'kv': 75, 'ma': 320}
# image_path = image_acq.acquire_image(protocol_settings)