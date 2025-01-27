from tkinter import Tk, Canvas
from PIL import Image, ImageTk
import tkinter as tk

def center_window(root, width=960, height=530):
    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算 (x, y) 坐标以使窗口居中
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def create_custom_window(image_path):
    # 创建无边框窗口
    root = Tk()
    root.overrideredirect(True)  # 去除窗口边框和标题栏

    # 设置窗口尺寸并居中
    center_window(root)

    # 打开图像文件并调整大小以适应窗口
    img = Image.open(image_path)
    img = img.resize((960, 530), Image.LANCZOS)  # 使用LANCZOS滤镜保持图像质量
    img_tk = ImageTk.PhotoImage(img)

    # 创建画布并添加图像到画布上
    canvas = Canvas(root, width=960, height=530)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_tk, anchor='nw')

    # 保存对img_tk的引用，防止被垃圾回收机制清除
    canvas.image = img_tk

    # 置顶窗口
    root.attributes("-topmost", True)

    # 定时器，在2秒后关闭窗口
    root.after(2000, root.destroy)  # 2000 毫秒 = 2 秒

    # 显示窗口
    root.mainloop()

if __name__ == "__main__":
    image_path = "yujiangjun.jpg"
    create_custom_window(image_path)