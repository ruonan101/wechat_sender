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
    
    作者: XiaoHai
    版权所有 © 2024 XiaoHai's Deep Blue Tech
    
    注意: 请遵守相关法律法规，不要用于非法用途
    开发者不对使用本程序造成的任何后果负责
    
    Hidden in the deep blue sea...
    There's always something waiting to be discovered...
    
    当深海的波涛遇见月光
    每一条消息都是一颗珍珠
    在这片蔚蓝中悄然闪耀...
"""

import subprocess
import sys
import os
import time
import platform
import urllib.request
import ssl

def check_package_installed(package_name):
    try:
        __import__(package_name.replace('-', '_'))
        return True
    except ImportError:
        return False

def pip_install(package):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except:
        return False

def pip_install_alternative(package):
    mirrors = [
        'https://pypi.tuna.tsinghua.edu.cn/simple',
        'https://mirrors.aliyun.com/pypi/simple',
        'https://pypi.doubanio.com/simple',
        'https://pypi.mirrors.ustc.edu.cn/simple'
    ]
    
    for mirror in mirrors:
        try:
            print(f"尝试使用镜像源: {mirror}")
            subprocess.check_call([
                sys.executable, 
                '-m', 
                'pip', 
                'install', 
                '-i', 
                mirror, 
                package
            ])
            return True
        except:
            continue
    return False

def download_wheel_manually(package):
    try:
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        base_url = "https://pypi.tuna.tsinghua.edu.cn/packages/wheel"
        wheel_name = f"{package}-latest-{py_version}-{system}_{machine}.whl"
        url = f"{base_url}/{wheel_name}"
        
        ssl._create_default_https_context = ssl._create_unverified_context
        wheel_path = os.path.join('temp', wheel_name)
        urllib.request.urlretrieve(url, wheel_path)
        
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_path])
        return True
    except:
        return False
    finally:
        if os.path.exists('temp'):
            import shutil
            shutil.rmtree('temp')

def install_package(package):
    print(f"正在安装 {package}...")
    
    if check_package_installed(package):
        print(f"{package} 已经安装！")
        return True
    
    print("尝试方法1：直接pip安装...")
    if pip_install(package):
        print(f"{package} 安装成功！")
        return True
    
    print("尝试方法2：使用国内镜像源安装...")
    if pip_install_alternative(package):
        print(f"{package} 安装成功！")
        return True
    
    print("尝试方法3：手动下载安装...")
    if download_wheel_manually(package):
        print(f"{package} 安装成功！")
        return True
    
    print(f"{package} 安装失败！")
    return False

def install_requirements():
    requirements = [
        'pyautogui',
        'pywin32',
        'psutil',
        'pillow',
        'opencv-python',
        'numpy',
        'pyperclip'
    ]
    
    success_count = 0
    failed_packages = []
    
    print("正在检查并安装必要的包...")
    for package in requirements:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    if failed_packages:
        print("\n以下包安装失败：")
        for package in failed_packages:
            print(f"- {package}")
        print("\n您可以尝试手动安装这些包，或者继续运行程序（可能会出现错误）")
    
    return success_count == len(requirements)

def check_python_version():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("错误：需要Python 3.6或更高版本！")
        print(f"当前Python版本: {sys.version}")
        return False
    return True

def main():
    print("微信轰炸器安装程序")
    print("==================")
    
    if not check_python_version():
        input("按回车键退出...")
        return
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except:
        print("错误：未检测到pip")
        print("尝试安装pip...")
        try:
            url = "https://bootstrap.pypa.io/get-pip.py"
            print("下载pip安装脚本...")
            urllib.request.urlretrieve(url, "get-pip.py")
            
            print("安装pip...")
            subprocess.check_call([sys.executable, "get-pip.py"])
            print("pip安装成功！")
        except Exception as e:
            print(f"安装pip失败: {str(e)}")
            print("请手动安装pip后重试")
            input("按回车键退出...")
            return
        finally:
            if os.path.exists("get-pip.py"):
                os.remove("get-pip.py")
    
    if not install_requirements():
        print("\n警告：某些包安装失败！")
        if input("是否继续运行程序？(y/n): ").lower() != 'y':
            return
    
    print("\n所有准备工作已完成！")
    print("3秒后启动主程序...")
    time.sleep(3)
    
    try:
        if os.path.exists('wechat_sender.py'):
            subprocess.run([sys.executable, 'wechat_sender.py'])
        else:
            print("错误：未找到 wechat_sender.py 文件！")
            print("请确保 setup_and_run.py 和 wechat_sender.py 在同一目录下")
    except Exception as e:
        print(f"运行主程序时出错: {str(e)}")
    
    input("\n程序结束，按回车键退出...")

if __name__ == "__main__":
    main() 