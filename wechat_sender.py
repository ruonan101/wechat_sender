"""
                _    _      ____ _           _   
               | |  | |    / ___| |__   __ _| |_ 
               | |/\| |   | |   | '_ \ / _` | __|
               \  /\  /   | |___| | | | (_| | |_ 
                \/  \/     \____|_| |_|\__,_|\__|
    
     ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
    ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌
    ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
    ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌
    ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
    ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌
    ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
    ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌
    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌
     ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀ 

    🌊 Deep Blue Messenger v1.0 🌊
    在这片蔚蓝的数字海洋中，消息如浪花般传递...
    
    注意: 请遵守相关法律法规，不要用于非法用途
    开发者不对使用本程序造成的任何后果负责
    
    Hidden in the deep blue sea...
    There's always something waiting to be discovered...
"""

import pyautogui
import win32gui
import win32con
import win32api
import win32process
import psutil
import time
import pyperclip
import logging
import cv2
import numpy as np
from PIL import ImageGrab, Image
import os
from typing import List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeChatSender:
    def __init__(self, retry_times: int = 3, delay: float = 1.0):
        self.retry_times = retry_times
        self.delay = delay
        pyautogui.FAILSAFE = True
        self.template_dir = "wechat_templates"
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        
        self.wechat_paths = [
            os.path.join(os.environ['ProgramFiles'], 'Tencent', 'WeChat', 'WeChat.exe'),
            os.path.join(os.environ['ProgramFiles(x86)'], 'Tencent', 'WeChat', 'WeChat.exe'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Tencent', 'WeChat', 'WeChat.exe')
        ]

    def launch_wechat(self) -> bool:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'WeChat.exe':
                logging.info("微信已经在运行")
                return True

        for path in self.wechat_paths:
            if os.path.exists(path):
                try:
                    os.startfile(path)
                    logging.info("正在启动微信...")
                    time.sleep(5)
                    return True
                except Exception as e:
                    logging.error(f"启动微信失败: {str(e)}")

        logging.error("未找到微信安装路径")
        return False

    def find_wechat_window(self) -> Optional[int]:
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                possible_titles = ["微信", "WeChat", "微信测试版"]
                possible_classes = ["WeChatMainWndForPC", "ChatWnd", "LaunchWnd"]
                title_match = any(title in window_text for title in possible_titles)
                class_match = any(cls in class_name for cls in possible_classes)
                if title_match or class_match:
                    logging.info(f"找到微信窗口 - 标题: {window_text}, 类名: {class_name}")
                    hwnds.append(hwnd)
            return True

        hwnds = []
        try:
            win32gui.EnumWindows(callback, hwnds)
            if not hwnds:
                logging.error("未找到微信窗口，请确保微信已打开")
                return None
            if len(hwnds) > 1:
                logging.info(f"找到 {len(hwnds)} 个可能的微信窗口:")
                for hwnd in hwnds:
                    title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    logging.info(f"窗口句柄: {hwnd}, 标题: {title}, 类名: {class_name}")
            return hwnds[0]
        except Exception as e:
            logging.error(f"查找微信窗口时出错: {str(e)}")
            return None

    def activate_window(self, hwnd: int) -> bool:
        for attempt in range(3):
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.5)
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(self.delay)
                foreground_hwnd = win32gui.GetForegroundWindow()
                if foreground_hwnd == hwnd:
                    return True
                if attempt < 2:
                    logging.warning(f"第 {attempt + 1} 次激活窗口失败，重试...")
                    time.sleep(1)
            except Exception as e:
                logging.error(f"激活窗口失败: {str(e)}")
                if attempt < 2:
                    time.sleep(1)
                    continue
        logging.error("无法激活微信窗口，请手动切换到微信窗口")
        input("请手动切换到微信窗口后按回车继续...")
        return True

    def find_chat_window(self) -> bool:
        chat_icon = self.find_element("chat_icon")
        if chat_icon:
            pyautogui.click(chat_icon[0], chat_icon[1])
            time.sleep(self.delay)
            return True
        return False

    def spam_message(self, contact: str, message: str, count: int = 10, interval: float = 0.5, 
                    add_random_suffix: bool = True) -> bool:
        try:
            if not self.search_and_send(contact, message, verify_send=False):
                return False
            logging.info(f"开始向 {contact} 发送轰炸消息...")
            success_count = 0
            for i in range(count):
                current_message = message
                if add_random_suffix:
                    random_suffix = f" [{i+1}/{count}] " + str(time.time())[-4:]
                    current_message += random_suffix
                try:
                    pyperclip.copy(current_message)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.press('enter')
                    success_count += 1
                    random_delay = interval + np.random.uniform(-0.2, 0.2)
                    time.sleep(max(0.1, random_delay))
                    if i > 0 and i % 10 == 0:
                        time.sleep(2)
                        logging.info(f"已发送 {i} 条消息，短暂暂停...")
                except Exception as e:
                    logging.error(f"发送第 {i+1} 条消息失败: {str(e)}")
                    continue
            logging.info(f"轰炸完成！成功发送 {success_count}/{count} 条消息")
            return success_count > 0
        except Exception as e:
            logging.error(f"轰炸消息失败: {str(e)}")
            return False

    def search_and_send(self, contact: str, message: str, verify_send: bool = True) -> bool:
        for attempt in range(self.retry_times):
            try:
                if not self.find_chat_window():
                    logging.error("未找到聊天窗口")
                    return False
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(self.delay)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                time.sleep(self.delay * 0.5)
                pyperclip.copy(contact)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(self.delay)
                if not self.verify_contact_exists(contact):
                    logging.error(f"找不到联系人: {contact}")
                    return False
                pyautogui.press('enter')
                time.sleep(self.delay)
                if verify_send:
                    return self.smart_send_message(message)
                return True
            except Exception as e:
                logging.warning(f"第 {attempt + 1} 次尝试失败: {str(e)}")
                time.sleep(self.delay)
        return False

    def direct_spam(self, message: str, count: int = 10, interval: float = 0.5, 
                   add_random_suffix: bool = True) -> bool:
        try:
            logging.info("开始直接轰炸当前聊天窗口...")
            success_count = 0
            print("请在5秒内切换到要轰炸的聊天窗口...")
            for i in range(5, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            messages = []
            for i in range(count):
                if add_random_suffix:
                    current_message = f"{message} [{i+1}]"
                else:
                    current_message = message
                messages.append(current_message)
            for i, current_message in enumerate(messages):
                try:
                    pyperclip.copy(current_message)
                    pyautogui.hotkey('ctrl', 'v', interval=0.01)
                    pyautogui.press('enter', interval=0.01)
                    success_count += 1
                    time.sleep(interval)
                    if (i + 1) % 10 == 0:
                        print(f"已发送 {i + 1}/{count} 条消息")
                except Exception as e:
                    logging.error(f"发送第 {i+1} 条消息失败: {str(e)}")
                    continue
            logging.info(f"轰炸完成！成功发送 {success_count}/{count} 条消息")
            return success_count > 0
        except Exception as e:
            logging.error(f"轰炸失败: {str(e)}")
            return False

    def rapid_spam(self, message: str, count: int = 100) -> bool:
        try:
            print("请在3秒内切换到要轰炸的聊天窗口...")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(0.5)
            pyperclip.copy(message)
            for i in range(count):
                try:
                    pyautogui.hotkey('ctrl', 'v', interval=0.01)
                    pyautogui.press('enter', interval=0.01)
                    if (i + 1) % 50 == 0:
                        print(f"已发送 {i + 1}/{count} 条消息")
                except:
                    continue
            return True
        except:
            return False

def main():
    sender = WeChatSender(retry_times=3, delay=1.0)
    
    print("""
    🌊 Deep Blue Messenger v1.0 🌊
    -----------------------------
    在数字海洋的深处
    消息如浪花般起伏
    珊瑚礁中藏着秘密
    等待有缘人发现...
    
    开发者: XiaoHai
    版权所有 © 2024 Deep Blue Tech
    
    警告: 请勿用于非法用途
    The deep blue sea remembers everything...
    -----------------------------
    """)
    
    if not sender.launch_wechat():
        print("无法启动微信，请确保微信已正确安装")
        return

    input("请确保微信已登录，然后按回车继续...")

    while True:
        print("\n请选择操作：")
        print("1. 发送单条消息")
        print("2. 消息轰炸")
        print("3. 定时轰炸")
        print("4. 直接轰炸当前聊天窗口")
        print("5. 超快速轰炸模式")
        print("6. 退出")
        
        choice = input("请输入选项(1-6): ")
        
        if choice == "1":
            contact = input("请输入联系人名称: ")
            message = input("请输入要发送的消息: ")
            if sender.search_and_send(contact, message):
                print("发送成功！")
            else:
                print("发送失败！")
                
        elif choice == "2":
            contact = input("请输入联系人名称: ")
            message = input("请输入要发送的消息: ")
            while True:
                try:
                    count = int(input("请输入发送次数 (1-1000): "))
                    if 1 <= count <= 1000:
                        break
                    print("发送次数必须在1-1000之间")
                except ValueError:
                    print("请输入有效的数字")
            
            while True:
                try:
                    interval = float(input("请输入发送间隔(秒, 建议不小于0.5): "))
                    if interval >= 0.1:
                        break
                    print("间隔时间不能小于0.1秒")
                except ValueError:
                    print("请输入有效的数字")
            
            add_random = input("是否添加随机后缀避免消息被拦截？(y/n): ").lower() == 'y'
            
            print(f"\n即将开始发送:")
            print(f"联系人: {contact}")
            print(f"消息内容: {message}")
            print(f"发送次数: {count}")
            print(f"发送间隔: {interval}秒")
            print(f"随机后缀: {'开启' if add_random else '关闭'}")
            
            if input("\n确认开始发送？(y/n): ").lower() == 'y':
                if sender.spam_message(contact, message, count, interval, add_random):
                    print("轰炸完成！")
                else:
                    print("轰炸失败！")
        
        elif choice == "3":
            contact = input("请输入联系人名称: ")
            message = input("请输入要发送的消息: ")
            count = int(input("请输入发送次数: "))
            interval = float(input("请输入发送间隔(秒): "))
            delay_minutes = int(input("请输入延迟多少分钟后开始发送: "))
            
            print(f"程序将在 {delay_minutes} 分钟后开始发送...")
            time.sleep(delay_minutes * 60)
            
            if sender.spam_message(contact, message, count, interval):
                print("定时轰炸完成！")
            else:
                print("定时轰炸失败！")
                
        elif choice == "4":
            print("请输入要发送的消息（可以是多行文本）：")
            print("输入完成后，在新的一行输入 'END' 结束：")
            
            message_lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                message_lines.append(line)
            
            message = '\n'.join(message_lines)
            
            while True:
                try:
                    count = int(input("请输入发送次数 (1-1000): "))
                    if 1 <= count <= 1000:
                        break
                    print("发送次数必须在1-1000之间")
                except ValueError:
                    print("请输入有效的数字")
            
            while True:
                try:
                    interval = float(input("请输入发送间隔(秒, 建议不小于0.5): "))
                    if interval >= 0.1:
                        break
                    print("间隔时间不能小于0.1秒")
                except ValueError:
                    print("请输入有效的数字")
            
            add_random = input("是否添加随机后缀避免消息被拦截？(y/n): ").lower() == 'y'
            
            print(f"\n即将开始发送:")
            print(f"消息内容:\n{message}")
            print(f"发送次数: {count}")
            print(f"发送间隔: {interval}秒")
            print(f"随机后缀: {'开启' if add_random else '关闭'}")
            
            if input("\n确认开始发送？(y/n): ").lower() == 'y':
                if sender.direct_spam(message, count, interval, add_random):
                    print("轰炸完成！")
                else:
                    print("轰炸失败！")
                
        elif choice == "5":
            print("请输入要发送的消息（可以是多行文本）：")
            print("输入完成后，在新的一行输入 'END' 结束：")
            
            message_lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                message_lines.append(line)
            
            message = '\n'.join(message_lines)
            
            while True:
                try:
                    count = int(input("请输入发送次数: "))
                    if count > 0:
                        break
                    print("发送次数必须大于0")
                except ValueError:
                    print("请输入有效的数字")
            
            print(f"\n即将开始超快速发送:")
            print(f"消息内容:\n{message}")
            print(f"发送次数: {count}")
            print("\n警告：发送速度极快，可能导致微信卡顿！")
            
            if input("\n确认开始发送？(y/n): ").lower() == 'y':
                if sender.rapid_spam(message, count):
                    print("轰炸完成！")
                else:
                    print("轰炸失败！")
        
        elif choice == "6":
            break
            
        else:
            print("无效的选项，请重新选择")

if __name__ == "__main__":
    main() 