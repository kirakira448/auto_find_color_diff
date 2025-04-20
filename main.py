import pyautogui
import time
from PIL import ImageGrab
import numpy as np
from color_detection.color_difference import ColorDifferenceDetector
from utils.mouse_event import MouseEvent
from pynput import keyboard

class ColorDifferenceGame:
    def __init__(self):
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0

        self.wait_time = 0.5
        # 初始化颜色差异检测器
        self.detector = ColorDifferenceDetector(threshold=10.0)
        self.mouse_event = MouseEvent()
        self.game_area = None
        self.running = True
        self.paused = False  # 添加暂停状态变量

    def select_game_area(self):
        self.game_area = self.mouse_event.get_region()
    
    def capture_game_area(self, area):
        """捕获游戏区域截图"""
        screenshot = ImageGrab.grab(bbox=area)
        return screenshot
    
    def find_color_difference(self, screenshot):
        """找出颜色不同的方块"""
        # 使用颜色差异检测器找出不同的方块
        position = self.detector.find_different_block(screenshot)
        if position:
            # 将相对位置转换为屏幕绝对位置
            x, y = position
            return (x + self.game_area[0], y + self.game_area[1])
        return None
    
    def click_different_block(self, position):
        """点击颜色不同的方块"""
        if position:
            pyautogui.click(position)
            return True
        return False
    
    def on_press(self, key):
        """按键处理函数"""
        try:
            if key.char == 'q':  # 当按下q键时
                self.running = False
                return False  # 停止监听
            elif key.char == 'w':  # 当按下空格键时
                self.paused = not self.paused  # 切换暂停状态
                print("游戏已" + ("暂停" if self.paused else "继续"))
        except AttributeError:
            pass
            
    def run(self):
        """运行游戏自动化"""
        print("开始自动找色差游戏...")
        print("按 'q' 键退出程序")
        print("按 '空格键' 暂停/继续程序")
        
        # 选择游戏区域
        self.select_game_area()
        print(f"游戏区域已选择: {self.game_area}")
        
        # 启动键盘监听
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        
        while self.running:
            if self.paused:  # 如果处于暂停状态，跳过主循环
                time.sleep(0.1)  # 暂停时小睡一下，避免CPU占用过高
                continue
                
            # 捕获游戏区域
            screenshot = self.capture_game_area(self.game_area)
            
            # 找出颜色不同的方块
            different_position = self.find_color_difference(screenshot)
            
            # 点击不同的方块
            if self.click_different_block(different_position):
                print("成功点击不同的方块")
            else:
                print("未找到不同的方块")
            
            # 等待下一题加载
            time.sleep(self.wait_time)
                
        
        print("\n程序已停止")

if __name__ == "__main__":
    game = ColorDifferenceGame()
    game.run() 