# 患者注册模块
import pandas as pd
import logging
from core.base_page import BasePage


class PatientRegistration(BasePage):
    def __init__(self, config):
        super().__init__(config)
        self.new_patient_button = "resources/button_new_patient.png"
        self.patient_id_field = "resources/field_patient_id.png"
        self.save_button = "resources/button_save.png"

    def register_new_patient(self, patient_data):
        """注册新患者"""
        logging.info(f"开始注册患者: {patient_data['name']}")

        # 点击新建患者按钮
        if not self.click_element(self.new_patient_button):
            return False

        # 填写患者信息
        self._fill_patient_data(patient_data)

        # 保存患者信息
        if not self.click_element(self.save_button):
            return False

        logging.info(f"患者 {patient_data['name']} 注册成功")
        return True

    def _fill_patient_data(self, patient_data):
        """填写患者数据（内部方法）"""
        try:
            # 点击患者ID字段并输入
            self.click_element(self.patient_id_field)
            pyautogui.write(patient_data['id'])

            # Tab键切换到下一个字段
            pyautogui.press('tab')
            pyautogui.write(patient_data['name'])

            # 继续填写其他字段...
            pyautogui.press('tab')
            pyautogui.write(patient_data['age'])

        except Exception as e:
            logging.error(f"填写患者数据失败: {str(e)}")
            raise

    def batch_register_patients(self, csv_file_path):
        """批量注册患者"""
        try:
            patients_df = pd.read_csv(csv_file_path)
            results = []

            for index, row in patients_df.iterrows():
                success = self.register_new_patient(row)
                results.append({
                    'patient_id': row['id'],
                    'name': row['name'],
                    'success': success
                })

            return results
        except Exception as e:
            logging.error(f"批量注册患者失败: {str(e)}")
            return []


# 使用示例
# patient_reg = PatientRegistration(config)
# patient_data = {'id': 'PT2025001', 'name': '张三', 'age': '45'}
# patient_reg.register_new_patient(patient_data)