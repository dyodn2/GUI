import tkinter as tk
from tkinter import messagebox
import json

import cv2
from PIL import Image, ImageTk

# 定义一个函数来保存用户信息到JSON文件
def save_user_info_to_json(user_info, filename):
    with open(filename, 'w') as file:
        json.dump(user_info, file)

# 定义一个函数来加载JSON文件中的用户信息
def load_user_info_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # 如果文件不存在，返回一个空字典

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Main Application")
        self.geometry("900x500")
        self.center_window()

        self.logged_in = False
        self.users = load_user_info_from_json('user_info.json')  # 存储用户名和密码的字典

        # 设置功能菜单
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.exit_application)
        self.menu_bar.add_cascade(label="Setting", menu=self.file_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about_dialog)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.show_login_frame()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 900
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def show_login_frame(self):
        self.clear_main_frame()
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(
            self.login_frame, text="Login", command=self.login,
            activebackground="blue", activeforeground="white"
        )
        self.login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.register_button = tk.Button(
            self.login_frame, text="Register", command=self.show_register_frame,
            activebackground="blue", activeforeground="white"
        )
        self.register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def show_register_frame(self):
        self.clear_main_frame()
        self.register_frame = tk.Frame(self)
        self.register_frame.pack(pady=20)

        self.new_username_label = tk.Label(self.register_frame, text="New Username:")
        self.new_username_label.grid(row=0, column=0, padx=5, pady=5)
        self.new_username_entry = tk.Entry(self.register_frame)
        self.new_username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.new_password_label = tk.Label(self.register_frame, text="New Password:")
        self.new_password_label.grid(row=1, column=0, padx=5, pady=5)
        self.new_password_entry = tk.Entry(self.register_frame, show="*")
        self.new_password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.confirm_password_label = tk.Label(self.register_frame, text="Confirm Password:")
        self.confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
        self.confirm_password_entry = tk.Entry(self.register_frame, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.register_button = tk.Button(
            self.register_frame, text="Register", command=self.register_user,
            activebackground="blue", activeforeground="white"
        )
        self.register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.back_button = tk.Button(
            self.register_frame, text="Back", command=self.show_login_frame,
            activebackground="blue", activeforeground="white"
        )
        self.back_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if new_username and new_password and new_password == confirm_password:
            if not self.check_duplicate_username(new_username):
                self.users[new_username] = new_password  # 将新用户信息存入字典中
                save_user_info_to_json(self.users, 'user_info.json')
                messagebox.showinfo("Success", "Successfully registered!")
                self.show_login_frame()
            else:
                messagebox.showerror("Error", "Username already exists!")
        else:
            messagebox.showerror("Error", "Password mismatch or empty fields!")

    def check_duplicate_username(self, new_username):
        # 检查用户名是否已经存在
        return new_username in self.users

    def clear_main_frame(self):
        for widget in self.winfo_children():
            if widget != self.menu_bar:
                widget.destroy()

    def show_main_frame(self):
        self.geometry("900x500")
        self.title("Main Application - Logged In")
        self.logged_in = True
        self.menu_bar.delete(2)  # 删除 Help 菜单
        self.menu_bar.add_command(label="Logout", command=self.logout)

        # 加载背景图片
        self.background_image = tk.PhotoImage(file="background_image.png")

        # 创建一个标签作为背景
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 创建两个按钮
        self.move_to_origin_button = tk.Button(
            self, text="归位", command=self.move_to_origin,
            bg="#228B22", fg="white",  # 使用浅绿色作为背景，白色作为前景
            relief="raised", borderwidth=3,
            padx=10, pady=5, font=("Arial", 12, "bold"),
            activebackground="lightgreen", activeforeground="white"  # 按压时的背景颜色
        )

        self.grab_button = tk.Button(
            self, text="抓取", command=self.grab,
            bg="#228B22", fg="white",  # 使用浅绿色作为背景，白色作为前景
            relief="raised", borderwidth=3,
            padx=10, pady=5, font=("Arial", 12, "bold"),
            activebackground="lightgreen", activeforeground="white"  # 按压时的背景颜色
        )

        # 计算窗口的中央位置
        window_center_x = self.winfo_width() / 2

        # 计算按钮的位置，使其在窗口中央
        button_width = 100  # 按钮的宽度
        x_offset = window_center_x - (button_width + 20) / 2 - 10

        # 将按钮放置在窗口中央一行
        self.move_to_origin_button.place(x=x_offset, y=200)
        self.grab_button.place(x=x_offset + button_width + 20, y=200)

    def move_to_origin(self):
        messagebox.showinfo("归位", "执行归位操作")

    def grab(self):
        # 创建小窗口
        grab_window = tk.Toplevel(self)
        grab_window.title("抓取任务")
        grab_window.geometry("640x480")

        # 设置摄像头
        cap = cv2.VideoCapture(0)

        def update_video_stream():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                video_label.configure(image=frame)
                video_label.image = frame
                video_label.after(10, update_video_stream)

        # 显示视频流
        video_label = tk.Label(grab_window)
        video_label.pack()

        update_video_stream()

        # 定义关闭窗口和释放摄像头资源的函数
        def close_grab_window():
            cap.release()  # 释放摄像头资源
            grab_window.destroy()  # 关闭窗口

        # 绑定窗口关闭事件，使其调用关闭窗口和释放摄像头资源的函数
        grab_window.protocol("WM_DELETE_WINDOW", close_grab_window)

        # 显示确定按钮，并绑定关闭窗口的函数
        ok_button = tk.Button(grab_window, text="确定", command=close_grab_window)
        ok_button.pack()


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.show_main_frame()
            self.login_frame.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def logout(self):
        self.logged_in = False
        self.menu_bar.delete(2)  # 删除 Logout 菜单
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.move_to_origin_button.destroy()
        self.grab_button.destroy()
        self.show_login_frame()

    def exit_application(self):
        self.destroy()

    def show_about_dialog(self):
        messagebox.showinfo("About", "This is a simple GUI application using Tkinter.")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
