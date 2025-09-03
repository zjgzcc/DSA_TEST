# 登录操作封装模块
import pyautogui
import time
import logging
import csv
import random
from core.base_page import BasePage


class LoginOperations(BasePage):
    """登录操作封装类，采用Page Object模式"""

    def __init__(self, config):
        super().__init__(config)
        self.login_elements = {
            'username_field': 'resources/login_elements/field_username.png',
            'password_field': 'resources/login_elements/field_password.png',
            'login_button': 'resources/login_elements/button_login.png',
            'logout_button': 'resources/login_elements/button_logout.png',
            'remember_checkbox': 'resources/login_elements/checkbox_remember.png',
            'error_message': 'resources/login_elements/error_message.png'
        }

    def navigate_to_login(self):
        """导航到登录界面"""
        logging.info("导航到登录界面")
        # 实现导航到登录页面的具体操作
        # 可能包括点击登录链接或直接访问登录URL
        return True

    def enter_credentials(self, username, password):
        """输入用户名和密码[6,7](@ref)"""
        try:
            # 输入用户名
            if not self.click_element(self.login_elements['username_field']):
                return False
            pyautogui.hotkey('ctrl', 'a')  # 全选现有文本
            pyautogui.press('backspace')  # 删除现有文本
            pyautogui.write(username, interval=0.1)

            # 输入密码
            if not self.click_element(self.login_elements['password_field']):
                return False
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            pyautogui.write(password, interval=0.1)

            logging.info(f"已输入凭据 - 用户名: {username}, 密码: {'*' * len(password)}")
            return True
        except Exception as e:
            logging.error(f"输入凭据时出错: {str(e)}")
            return False

    def click_login(self):
        """点击登录按钮"""
        if self.click_element(self.login_elements['login_button']):
            logging.info("已点击登录按钮")
            return True
        return False

    def toggle_remember_me(self, enable=True):
        """切换'记住我'复选框状态"""
        if self.click_element(self.login_elements['remember_checkbox']):
            status = "启用" if enable else "禁用"
            logging.info(f"已{status}'记住我'功能")
            return True
        return False

    def is_logged_in(self, timeout=10):
        """检查是否成功登录[7](@ref)"""
        try:
            # 方法1: 检查登出按钮是否存在
            if self.wait_for_element(self.login_elements['logout_button'], timeout):
                logging.info("登录成功检测: 找到登出按钮")
                return True

            # 方法2: 检查URL是否跳转到主界面
            # 方法3: 检查用户头像或欢迎信息

            logging.warning("登录成功验证失败")
            return False
        except Exception as e:
            logging.error(f"登录验证时出错: {str(e)}")
            return False

    def is_error_message_displayed(self, expected_text=None):
        """检查错误消息是否显示[1,2](@ref)"""
        try:
            if self.wait_for_element(self.login_elements['error_message'], timeout=5):
                # 可选: 使用OCR读取错误消息文本并与预期比较
                logging.info("检测到错误消息")
                return True
            return False
        except Exception as e:
            logging.error(f"检查错误消息时出错: {str(e)}")
            return False

    def perform_logout(self):
        """执行退出登录操作"""
        if self.click_element(self.login_elements['logout_button']):
            logging.info("已退出登录")
            return True
        return False

    def get_test_users(self, csv_file):
        """从CSV文件获取测试用户数据[2](@ref)"""
        test_users = []
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    test_users.append({
                        'username': row['username'],
                        'password': row['password'],
                        'expected_result': row['expected_result'],
                        'test_type': row['test_type']
                    })
            logging.info(f"从 {csv_file} 加载了 {len(test_users)} 个测试用户")
        except Exception as e:
            logging.error(f"读取测试用户数据时出错: {str(e)}")
        return test_users

    def execute_login_test(self, username, password, expected_result):
        """执行完整的登录测试流程"""
        test_result = {
            'username': username,
            'password': password,
            'expected_result': expected_result,
            'actual_result': 'FAIL',
            'error_message': ''
        }

        try:
            # 导航到登录页面
            if not self.navigate_to_login():
                raise Exception("无法导航到登录页面")

            # 输入凭据
            if not self.enter_credentials(username, password):
                raise Exception("无法输入凭据")

            # 点击登录
            if not self.click_login():
                raise Exception("无法点击登录按钮")

            # 等待并验证结果
            time.sleep(3)  # 等待登录处理

            if expected_result == "success":
                if self.is_logged_in():
                    test_result['actual_result'] = 'PASS'
                else:
                    test_result['error_message'] = "预期成功但实际失败"
            else:
                if self.is_error_message_displayed():
                    test_result['actual_result'] = 'PASS'
                else:
                    test_result['error_message'] = "预期失败但实际成功或无错误消息"

        except Exception as e:
            test_result['error_message'] = str(e)

        return test_result