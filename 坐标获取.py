import pyautogui
import time

# 等待5秒钟，让你有时间移动鼠标到目标位置
time.sleep(5)

# 获取并打印当前鼠标位置
print(pyautogui.position())
