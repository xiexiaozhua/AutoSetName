import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
import re
from autosetname import open_edge_with_selenium_inprivate as login
from startgui import create_custom_window
import threading
from autosetname import generate_random_string as sb_random

banben = 1.0
key_yanzheng = sb_random(48,prefix="Antibot_")
print("为了防止人机所以请通过验证")
time.sleep(0.3)
print("你的验证卡密为: " + key_yanzheng)
time.sleep(0.3)
key_sb = input("请输入你的验证卡密:")
if key_sb != key_yanzheng:
    print("操你妈人机")
    time.sleep(3)
    sys.exit(1)
print("恭喜您通过了人机验证 欢迎使用XGP Auto Set Name")
time.sleep(0.5)
print("版本号: " + str(banben))
time.sleep(0.5)
print("尊贵的用户: Admin")
time.sleep(0.5)
sb = 0
create_custom_window(image_path = "yujiangjun.jpg")
print("儿子，妈妈什么都不要求，你别整天抱着你那手机拍你那脚了，也别闻莫名其妙的药水了，你看你肛门都大到要做手术了，\n都能塞苹果了，还有啊，别在网络上惹别人了，妈妈上抖音都看到咱们全家大头照满天飞了，你这是又惹谁了，你的锁妈妈帮你洗了洗，放在你床上了，以后飞机杯别乱丢了，\n也别花钱找人穿白袜，篮球鞋踩你了，有啥事跟妈说，明天要下暴雨就别全国飞到别人床上和别人乱搞了，\n在家里呆着哦，面条下好了，你看你瘦的脖子都被你金主用项圈勒出印子了，每天在家性瘾发作，你弟弟都要被你搞出精神衰弱了，你小时候很乖的，会帮妈妈洗衣做饭，现在这样子了呢，为什么会变成同性恋？\n宝贝告诉妈妈，是不是因为在手机上看到不好的东西了？是不是因为手机？是不是？为什么不回答我？你怎么会变成同性恋？\n妈妈辛辛苦苦把你养的这么大，你为什么要当同性恋？")
class CustomWindow:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.frame.pack(pady=20)

        # Add prefix input field and label
        self.prefix_var = tk.StringVar()
        self.prefix_label = ttk.Label(self.frame, text="前缀:")
        self.prefix_entry = ttk.Entry(self.frame, textvariable=self.prefix_var, width=30)

        # Existing code for other widgets...

        # Place the new widgets on the grid
        self.prefix_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.prefix_entry.grid(row=3, column=1, padx=5, pady=5)

        # ... (rest of your existing initialization code remains unchanged)

        # Label for input entry (now placed before the input field)
        self.input_label = ttk.Label(self.frame, text="卡密:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        # Input field for key or email
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(self.frame, textvariable=self.input_var, width=30)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        # Second input field for password (hidden by default)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.frame, textvariable=self.password_var, width=30, show="*")
        self.password_label = ttk.Label(self.frame, text="密码:")

        # Switch between key mode and email mode (placed at the bottom left corner)
        self.mode_var = tk.IntVar(value=0)  # 0 for key mode, 1 for email mode
        self.mode_switch = ttk.Checkbutton(
            self.frame,
            text="切换到邮箱登录模式(卡密模式\n支持路人和大海卡网\n 直接复制就行)",
            variable=self.mode_var,
            command=self.toggle_mode
        )
        self.mode_switch.grid(row=2, column=0, columnspan=2, sticky='w', pady=(10, 0))

        # Add "设置" button
        self.settings_button = ttk.Button(self.frame, text="设置", command=self.handle_settings)
        self.settings_button.grid(row=2, column=1, sticky='e', pady=(10, 0))

        # Initially hide the password entry and label
        self.toggle_mode()

    def toggle_mode(self):
        if self.mode_var.get() == 1:  # Email mode
            self.input_label.config(text="邮箱:")
            self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
            self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        else:  # Key mode
            self.input_label.config(text="卡密:")
            self.password_label.grid_remove()
            self.password_entry.grid_remove()

    def handle_settings(self):
        def login_with_credentials(email, password,randomnamee):
            login(email, password,randomnamee)
        input_value = self.input_var.get().strip()
        password_value = self.password_var.get().strip()
        prefix_value = self.prefix_var.get().strip()  # Get the prefix value

        if not input_value:
            messagebox.showwarning("警告", "请输入邮箱或卡密。")
            return

        if self.mode_var.get() == 0:  # Key mode
            # Combine input and password into a single string for extraction
            combined_input = f"{input_value}----{password_value}" if password_value else input_value
            extracted_credentials = self.extract_credentials([combined_input])
        else:  # Email mode
            if not password_value:
                messagebox.showwarning("警告", "请输入密码。")
                return
            extracted_credentials = [{'email': input_value, 'password': password_value}]

        print("Extracted Credentials:")
        for cred in extracted_credentials:
            print(f"Email: {cred['email']}, Password: {cred['password']}")

        # Optionally, you can also display this information to the user via a messagebox
        def threaded_login(extracted_credentials):
            if extracted_credentials:
                credentials = extracted_credentials[0]
                # 创建一个新线程来运行登录函数
                threading.Thread(target=login_with_credentials,
                                 args=(credentials['email'], credentials['password'], prefix_value)).start()
        if extracted_credentials:
            threaded_login(extracted_credentials)
        else:
            # 因为这是一个GUI应用，所以警告框应该在主线程中调用
            messagebox.showwarning("警告", "未能提取任何凭据，请检查输入格式。")

    def extract_credentials(self, credentials_list):
        pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(?::|----)([a-zA-Z0-9]+)'
        extracted = []
        for cred in credentials_list:
            match = re.search(pattern, cred)
            if match:
                extracted.append({
                    'email': match.group(1),
                    'password': match.group(2)
                })
        return extracted

def create_custom_window():
    root = tk.Tk()
    root.title("XGP Auto Set Name By Mr.zhange's Brain")
    root.geometry("400x200")

    app = CustomWindow(root)

    root.mainloop()

if __name__ == "__main__":
    create_custom_window()