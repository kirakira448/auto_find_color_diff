from pynput import mouse

class MouseEvent:
    def __init__(self):
        self.clicks = []

    def on_click_two_points(self, x, y, button, pressed):
        if pressed:
            self.clicks.append((x, y))
            # 当获取到两个点后，停止监听
            if len(self.clicks) >= 2:
                return False

    def start_click_listen(self, on_click):
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def get_region(self):
        """
        获取用户选择的区域坐标
        :return: (left, top, right, bottom)
        """
        self.clicks = []  # 清空之前的点击记录
        print("请点击要选择区域的左上角和右下角...")
        self.start_click_listen(self.on_click_two_points)
        
        if len(self.clicks) == 2:
            # 确保返回的坐标是左上和右下的格式
            x1, y1 = self.clicks[0]
            x2, y2 = self.clicks[1]
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)
            return (left, top, right, bottom)
        return None

if __name__ == "__main__":
    mouse_event = MouseEvent()
    region = mouse_event.get_region()
    print(region)

