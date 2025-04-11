# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment

SUPPORTED_FORMATS = ['.m4a', '.wav', '.flac', '.aac']  # 可转换的格式

def convert_audio_to_mp3(input_path, output_path):
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3")
        return True
    except Exception as e:
        print(f"转换失败 ({input_path}): {e}")
        return False

def copy_mp3(input_path, output_path):
    try:
        shutil.copy2(input_path, output_path)
        return True
    except Exception as e:
        print(f"拷贝失败 ({input_path}): {e}")
        return False

def batch_convert(input_folder, output_folder):
    if not os.path.isdir(input_folder):
        messagebox.showerror("错误", "输入路径不是有效的文件夹")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(input_folder)
    processed_count = 0

    for file_name in files:
        ext = os.path.splitext(file_name)[1].lower()
        input_file = os.path.join(input_folder, file_name)

        if ext in SUPPORTED_FORMATS:
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".mp3")
            if convert_audio_to_mp3(input_file, output_file):
                processed_count += 1
        elif ext == ".mp3":
            output_file = os.path.join(output_folder, file_name)
            if copy_mp3(input_file, output_file):
                processed_count += 1

    messagebox.showinfo("完成", f"处理完成，共处理 {processed_count} 个音频文件。")

# Tkinter GUI
def choose_input_folder():
    path = filedialog.askdirectory()
    if path:
        input_var.set(path)
        # 若未设置输出路径，则自动填写默认输出路径
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
        messagebox.showwarning("警告", "请先选择输入文件夹。")
        return

    # 设置默认输出路径
    if not output_folder:
        output_folder = os.path.join(os.path.dirname(input_folder), "MP3转换")
        output_var.set(output_folder)

    batch_convert(input_folder, output_folder)

# 界面设置
root = tk.Tk()
root.title("音频批量转换工具（含 MP3 拷贝）")
root.geometry("500x250")

input_var = tk.StringVar()
output_var = tk.StringVar()

tk.Label(root, text="输入文件夹：").pack(pady=(10, 0))
tk.Entry(root, textvariable=input_var, width=60).pack()
tk.Button(root, text="选择输入文件夹", command=choose_input_folder).pack(pady=5)

tk.Label(root, text="输出文件夹（可留空，自动创建）").pack(pady=(10, 0))
tk.Entry(root, textvariable=output_var, width=60).pack()
tk.Button(root, text="选择输出文件夹", command=choose_output_folder).pack(pady=5)

tk.Button(root, text="开始转换", command=start_conversion, bg="green", fg="white", height=2).pack(pady=10)

root.mainloop()
