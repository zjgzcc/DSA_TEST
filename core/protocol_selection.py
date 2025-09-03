# 检查协议选择模块
import logging
from core.base_page import BasePage
import time


class ProtocolSelection(BasePage):
    def __init__(self, config):
        super().__init__(config)
        self.protocol_dropdown = "resources/dropdown_protocol.png"
        self.search_protocol_field = "resources/field_search_protocol.png"

    def select_protocol(self, protocol_name):
        """选择检查协议"""
        logging.info(f"选择协议: {protocol_name}")

        # 点击协议下拉框
        if not self.click_element(self.protocol_dropdown):
            return False

        # 搜索协议（如果系统支持）
        if self.click_element(self.search_protocol_field):
            pyautogui.write(protocol_name)
            time.sleep(1)  # 等待搜索结果

        # 选择特定协议
        protocol_image = f"resources/protocol_{protocol_name.lower()}.png"
        if not self.click_element(protocol_image):
            logging.error(f"找不到协议: {protocol_name}")
            return False

        logging.info(f"协议 {protocol_name} 选择成功")
        return True

    def verify_protocol_selected(self, protocol_name):
        """验证协议已正确选择"""
        expected_indicator = f"resources/indicator_{protocol_name.lower()}.png"
        if self.wait_for_element(expected_indicator, timeout=10):
            logging.info(f"验证成功: 协议 {protocol_name} 已选择")
            return True
        else:
            logging.error(f"验证失败: 协议 {protocol_name} 未正确选择")
            return False


# 使用示例
# protocol_selector = ProtocolSelection(config)
# protocol_selector.select_protocol("Cardiac_Angiography")
# protocol_selector.verify_protocol_selected("Cardiac_Angiography")