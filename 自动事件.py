import time
import keyboard
import pyautogui
import random
from pynput.keyboard import Controller

# 设置发送间隔时间（秒）
interval = 60

# 设置要发送的消息列表
messages = [" /修炼", " /修炼", " /修炼", " /修炼"," /修炼"," /修炼"," /修炼"," /直接突破"]#["双修 琉光拔"]#

# 创建键盘控制器
keyboard_controller = Controller()

# 等待几秒钟以便你有时间切换到QQ聊天窗口
time.sleep(5)

while True:
    # 随机选择一条消息
    message = random.choice(messages)
    keyboard_controller.type("@")
    time.sleep(0.5)
    pyautogui.click(x=812, y=761)
    # 输入消息
    for char in message:
        keyboard_controller.type(char)
        time.sleep(0.05)  # 添加一个小的延迟来模拟真实的打字速度
    # 按下回车键发送消息
    keyboard_controller.press('\n')
    keyboard_controller.release('\n')
    # 回车
    pyautogui.press('enter')
    pyautogui.press('enter')
    # 等待指定的间隔时间
    time.sleep(interval)


