from pynput import mouse
import pyautogui

clicks = []

def on_click(x, y, button, pressed):
    '''
    鼠标点击事件的回调函数
    
    :param x: 鼠标点击的x坐标
    :param y: 鼠标点击的y坐标
    :param button: 点击的鼠标按钮
    :param pressed: True表示按下，False表示释放
    
    :return: 当点击次数达到2次时返回False停止监听,否则返回None继续监听
    '''
    if pressed:
        print(f"点击位置: ({x}, {y})")
        clicks.append((x, y))  # 记录点击坐标
        if len(clicks) >= 2:
            return False  # 当收集到2个点击位置时停止监听

print("请点击左上角，然后点击右下角：")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

# 获取两个点
(x1, y1), (x2, y2) = clicks

# 规范化坐标（防止点击顺序相反）
left = min(x1, x2)
top = min(y1, y2)
width = abs(x2 - x1)
height = abs(y2 - y1)

print(f"选择区域：left={left}, top={top}, width={width}, height={height}")

# 示例：截图选中区域
screenshot = pyautogui.screenshot(region=(left, top, width, height))
screenshot.save("selected_region.png")
print("截图已保存为 selected_region.png")
