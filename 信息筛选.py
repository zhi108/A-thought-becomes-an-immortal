import time
import pyautogui
from pynput.keyboard import Controller
import re
import pyperclip

# 设置发送间隔时间（秒）
interval = 5

# 创建键盘控制器
keyboard_controller = Controller()

# 定义药材品阶
grades = ["九品药材", "八品药材", "七品药材"]#, "六品药材", "五品药材", "四品药材", "三品药材", "二品药材", "一品药材"]

# 等待几秒钟以便你有时间切换到QQ聊天窗口
time.sleep(5)


def send_message_and_get_response(message):
    # 点击聊天框
    pyautogui.click(x=542, y=805)
    # 输入@一念
    keyboard_controller.type("@")
    time.sleep(1)
    pyautogui.click(x=812, y=761)
    # 输入消息
    for char in message:
        keyboard_controller.type(char)
        time.sleep(0.05)  # 添加一个小的延迟来模拟真实的打字速度

    # 回车发送
    pyautogui.press('enter')
    pyautogui.press('enter')

    # 等待响应返回
    time.sleep(3)
    pyautogui.click(x=594, y=703)
    # 复制返回的背包信息
    # pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # 从剪贴板获取返回的背包信息
    response = pyperclip.paste()
    return response


def extract_herb_names(text):
    # 正则表达式匹配所有品阶的药材名称
    pattern = r'(?:一品药材|二品药材|三品药材|四品药材|五品药材|六品药材|七品药材|八品药材|九品药材) (\S+)\s+数量:\d+'
    matches = re.findall(pattern, text)
    return matches


def extract_prices(text):
    # 正则表达式匹配价格信息
    pattern = r'价格:(\d+\.\d+)万'
    matches = re.findall(pattern, text)
    prices = [float(price) for price in matches]
    return prices


def send_refresh_message(herb_name):
    # 点击聊天框
    pyautogui.click(x=542, y=805)
    # 输入@一念
    keyboard_controller.type("@")
    time.sleep(0.5)
    pyautogui.click(x=812, y=761)
    message = f"坊市刷新 {herb_name}"
    # 发送刷新消息并获取返回信息
    response = send_message_and_get_response(message)
    return response


def list_herb(herb_name, price):
    # 将价格从万转化为具体数字
    numeric_price = int(price * 10000 - 200000)
    for _ in range(3):  # 每种药材上架三次
        message = f"坊市上架 {herb_name} {numeric_price}"
        send_message_and_get_response(message)
        # 检查剪贴板内容是否包含"每人只可上架十五个物品！"
        clipboard_content = pyperclip.paste()
        if "每人只可上架十五个物品！" in clipboard_content:
            print("已达到上架限制，停止运行。")
            return


# 主循环
all_items = []

for grade in grades:
    message = f"{grade}背包"
    response = send_message_and_get_response(message)
    time.sleep(0.05)
    herb_names = extract_herb_names(response)
    print(f"筛选出来的{grade}名字：")
    for name in herb_names:
        print(name)
        refresh_response = send_refresh_message(name)
        prices = extract_prices(refresh_response)
        for price in prices:
            all_items.append((name, price))

# 将价格从高到低进行排序并输出
sorted_items = sorted(all_items, key=lambda x: x[1], reverse=True)
print("从高到低排序的价格：")
for item in sorted_items:
    print(f"{item[0]}: {item[1]}万")
    list_herb(item[0], item[1])  # 上架药材
time.sleep(interval)



