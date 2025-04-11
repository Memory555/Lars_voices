# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import *

def convert_mp4_to_mp3(input_path, output_path):
    try:
        video = VideoFileClip(input_path)
        video.audio.write_audiofile(output_path)
        return True
    except Exception as e:
        print(f"转换失败 ({input_path}): {e}")
        return False

def batch_convert(input_folder, output_folder):
    if not os.path.isdir(input_folder):
        messagebox.showerror("错误", "输入路径无效")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    mp4_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".mp4")]

    if not mp4_files:
        messagebox.showinfo("提示", "未找到 .mp4 文件")
        return

    success_count = 0
    for file_name in mp4_files:
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".mp3")
        if convert_mp4_to_mp3(input_file, output_file):
            success_count += 1

    messagebox.showinfo("完成", f"转换完成，共成功转换 {success_count} 个文件。")

# Tkinter GUI 界面函数
def choose_input_folder():
    path = filedialog.askdirectory()
    if path:
        input_var.set(path)
        # 自动填充默认输出文件夹（若未手动指定）
        if not output_var.get():
            default_out = os.path.join(os.path.dirname(path), "MP3转换")
            output_var.set(default_out)

def choose_output_folder():
    path = filedialog.askdirectory()
    if path:
        output_var.set(path)

def start_conversion():
    input_folder = input_var.get()
    output_folder = output_var.get()

    if not input_folder:
        messagebox.showwarning("警告", "请先选择输入文件夹")
        return

    # 如果用户没有指定输出路径，则使用默认路径
    if not output_folder:
        output_folder = os.path.join(os.path.dirname(input_folder), "MP3转换")
        output_var.set(output_folder)

    batch_convert(input_folder, output_folder)

# 主界面
root = tk.Tk()
root.title("MP4 转 MP3 批量转换工具")
root.geometry("500x260")

input_var = tk.StringVar()
output_var = tk.StringVar()

tk.Label(root, text="输入文件夹：").pack(pady=(10, 0))
tk.Entry(root, textvariable=input_var, width=60).pack()
tk.Button(root, text="选择输入文件夹", command=choose_input_folder).pack(pady=5)

tk.Label(root, text="输出文件夹（可留空，将默认创建在同级目录中）").pack(pady=(10, 0))
tk.Entry(root, textvariable=output_var, width=60).pack()
tk.Button(root, text="选择输出文件夹", command=choose_output_folder).pack(pady=5)

tk.Button(root, text="开始转换", command=start_conversion, bg="blue", fg="white", height=2).pack(pady=10)

root.mainloop()
