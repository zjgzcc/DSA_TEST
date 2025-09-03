# 图像处理工具模块
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import logging


class ImageUtils:
    def __init__(self, confidence_threshold=0.9):
        self.confidence_threshold = confidence_threshold

    def compare_images(self, image1_path, image2_path):
        """
        比较两张图像的相似度
        返回: (相似度百分比, 差异图像)
        """
        try:
            # 读取图像
            image1 = cv2.imread(image1_path)
            image2 = cv2.imread(image2_path)

            # 转换为灰度图
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

            # 计算SSIM（结构相似性指数）
            similarity, diff = ssim(gray1, gray2, full=True)
            similarity_percent = similarity * 100

            # 确保误差<5%（满足数据准确性要求）
            if similarity_percent < 95:
                logging.warning(f"图像相似度仅 {similarity_percent:.2f}%")

            return similarity_percent, diff
        except Exception as e:
            logging.error(f"图像比较失败: {str(e)}")
            return 0, None

    def find_element_on_screen(self, image_path, region=None):
        """
        在屏幕上查找元素
        返回: 元素坐标或None
        """
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=self.confidence_threshold,
                region=region
            )
            return location
        except Exception as e:
            logging.error(f"查找元素失败: {str(e)}")
            return None


# 使用示例
# image_utils = ImageUtils()
# similarity, diff = image_utils.compare_images("reference.png", "captured.png")