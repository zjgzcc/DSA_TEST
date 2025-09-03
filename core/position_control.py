# 系统位置控制模块
import time
import logging
from core.base_page import BasePage


class PositionControl(BasePage):
    def __init__(self, config):
        super().__init__(config)
        self.move_up_button = "resources/button_move_up.png"
        self.move_down_button = "resources/button_move_down.png"
        self.position_indicator = "resources/indicator_position.png"

    def move_to_position(self, target_position, tolerance=0.5):
        """移动系统到指定位置"""
        logging.info(f"移动到位置: {target_position}")

        # 获取当前位置
        current_pos = self.get_current_position()
        if current_pos is None:
            logging.error("无法获取当前位置")
            return False

        # 计算移动方向和距离
        direction = self._calculate_direction(current_pos, target_position)
        distance = abs(target_position - current_pos)

        # 执行移动
        self._execute_movement(direction, distance)

        # 验证最终位置
        final_pos = self.get_current_position()
        if final_pos is not None and abs(final_pos - target_position) <= tolerance:
            logging.info(f"位置移动成功: {final_pos}")
            return True
        else:
            logging.error(f"位置移动失败，当前位置: {final_pos}")
            return False

    def get_current_position(self):
        """获取当前位置"""
        try:
            # 使用OCR或图像识别读取位置指示器
            position_text = self._read_position_indicator()
            if position_text:
                return float(position_text)
            return None
        except Exception as e:
            logging.error(f"获取当前位置失败: {str(e)}")
            return None

    def _execute_movement(self, direction, distance):
        """执行移动操作（内部方法）"""
        move_button = self.move_up_button if direction == 'up' else self.move_down_button

        # 根据距离计算需要按住按钮的时间
        move_time = distance * 0.1  # 假设每单位距离需要0.1秒

        # 按下移动按钮
        pyautogui.mouseDown(move_button)
        time.sleep(move_time)
        pyautogui.mouseUp()

        # 等待系统稳定
        time.sleep(2)


# 使用示例
# position_ctrl = PositionControl(config)
# position_ctrl.move_to_position(123.5)