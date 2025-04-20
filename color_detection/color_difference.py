import numpy as np
from PIL import Image
from typing import Tuple, List, Optional
import cv2
from utils.math_util import get_center_point
from collections import defaultdict

class ColorDifferenceDetector:
    def __init__(self, threshold: float = 10.0):
        """
        初始化颜色差异检测器
        :param threshold: 颜色差异阈值，默认10.0
        """
        self.threshold = threshold
        self.contours = []
        self.squares = []
        self.img_width = 0
        self.img_height = 0
        self.colors = defaultdict(list)


    def sort_contours(cnts, rows=8, cols=8):
        """
        排序轮廓（从上到下、左到右）
        :param cnts: 轮廓列表
        :param rows: 行数
        :param cols: 列数
        :return: 排序后的轮廓列表
        """
        cnts = sorted(cnts, key=lambda c: cv2.boundingRect(c)[1])  # 先按Y排
        result = []
        for i in range(rows):
            row = cnts[i*cols:(i+1)*cols]
            row = sorted(row, key=lambda c: cv2.boundingRect(c)[0])  # 再按X排
            result.extend(row)
        return result
    
    def get_squares(self,contours:List[np.ndarray]) -> List[Tuple[int, int, int, int]]:
        """
        获取轮廓列表中的方块
        :param contours: 轮廓列表
        :return: 方块列表
        """
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > (self.img_width * 2/3):
                continue
            if w < (self.img_width*0.05):
                continue
            self.squares.append((x,y,w,h))

    
    def find_different_color_position(self,image,squares):        
        for x,y,w,h in squares:
            center_x,center_y = get_center_point(x,y,w,h)
            color = tuple(image[center_y, center_x])
            self.colors[color].append((center_x,center_y))
        
        for color,positions in self.colors.items():
            if len(positions) == 1:
                return positions[0]


    def find_different_block(self, screenshot: Image.Image) -> Optional[Tuple[int, int]]:
        """
        找出颜色不同的方块
        :param screenshot: 游戏区域截图
        :return: 不同方块的位置(x, y)，如果未找到返回None
        """
        # 重置状态
        self.contours = []
        self.squares = []
        self.colors = defaultdict(list)
        
        # 直接转换为OpenCV格式，减少一次转换
        img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        self.img_width, self.img_height = img_cv.shape[:2]
        
        # 将图像转换为灰度图像
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        # 增强对比度（直方图均衡）
        equalized = cv2.equalizeHist(gray)
        # 二值化处理
        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            3,  # 邻域大小
            3    # 常数差值
        )
        # 使用形态学操作来清理图像
        kernel = np.ones((3,3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        # 使用膨胀操作来填补空隙
        binary = cv2.dilate(binary, np.ones((7,7), np.uint8), iterations=1)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # 查找轮廓
        self.contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # sorted_contours = self.sort_contours(contours)

        # 遍历轮廓，获取有效方块
        if len(self.contours) > 0:
            self.get_squares(self.contours)
        # 找出颜色不同的position
        if len(self.squares) > 0:
            position = self.find_different_color_position(img_cv,self.squares)
            return position
        return None
