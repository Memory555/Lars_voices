# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment

def compress_mp3(input_path, output_path, target_bitrate="12k", channels=1, sample_rate=22050):
    try:
        audio = AudioSegment.from_file(input_path, format="mp3")
        audio = audio.set_channels(channels)
        audio = audio.set_frame_rate(sample_rate)
        audio.export(output_path, format="mp3", bitrate=target_bitrate)
        return True
    except Exception as e:
        print(f"压缩失败 ({input_path}): {e}")
        return False

def batch_compress(input_folder, output_folder, target_bitrate, channels, sample_rate):
    if not os.path.isdir(input_folder):
        messagebox.showerror("错误", "输入路径不是有效的文件夹")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = os.listdir(input_folder)
    mp3_files = [f for f in file_list if f.lower().endswith(".mp3")]

    if not mp3_files:
        messagebox.showinfo("提示", "文件夹中没有 .mp3 文件")
        return

    success_count = 0
    for file_name in mp3_files:
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + "_compressed.mp3")
        if compress_mp3(input_file, output_file, target_bitrate, channels, sample_rate):
            success_count += 1

    messagebox.showinfo("完成", f"压缩完成，共成功处理 {success_count} 个文件。")

# GUI 界面部分
def choose_input_folder():
    path = filedialog.askdirectory()
    if path:
        input_var.set(path)
        # 如果输出路径未设置，自动补充默认输出路径
        if not output_var.get():
            default_output = os.path.join(os.path.dirname(path), "MP3压缩")
            output_var.set(default_output)

def choose_output_folder():
    path = filedialog.askdirectory()
    if path:
        output_var.set(path)

def start_compression():
    input_folder = input_var.get()
    output_folder = output_var.get()
    bitrate = bitrate_var.get()
    channels = 1 if channel_var.get() == "单声道" else 2
    try:
        sample_rate = int(sample_rate_var.get())
    except ValueError:
        messagebox.showerror("错误", "采样率必须为整数")
        return

    if not input_folder:
        messagebox.showwarning("警告", "请输入输入文件夹路径")
        return

    # 如果输出路径为空，使用默认输出路径
    if not output_folder:
        output_folder = os.path.join(os.path.dirname(input_folder), "MP3压缩")
        output_var.set(output_folder)

    batch_compress(input_folder, output_folder, bitrate, channels, sample_rate)

# 创建主窗口
root = tk.Tk()
root.title("MP3 压缩工具（支持声道/采样率/比特率设置）")
root.geometry("550x500")

input_var = tk.StringVar()
output_var = tk.StringVar()
channel_var = tk.StringVar(value="单声道")
sample_rate_var = tk.StringVar(value="22050")
bitrate_var = tk.StringVar(value="12k")

# 输入输出路径
tk.Label(root, text="输入文件夹：").pack(pady=(10, 0))
tk.Entry(root, textvariable=input_var, width=65).pack()
tk.Button(root, text="选择输入文件夹", command=choose_input_folder).pack(pady=5)

tk.Label(root, text="输出文件夹（可选）：").pack(pady=(10, 0))
tk.Entry(root, textvariable=output_var, width=65).pack()
tk.Button(root, text="选择输出文件夹", command=choose_output_folder).pack(pady=5)

# 参数设置部分
tk.Label(root, text="声道类型：").pack(pady=(10, 0))
tk.OptionMenu(root, channel_var, "单声道", "立体声").pack()

tk.Label(root, text="采样率 (Hz)：").pack(pady=(10, 0))
tk.Entry(root, textvariable=sample_rate_var, width=20).pack()

tk.Label(root, text="比特率 (如 8k, 12k, 96k)：").pack(pady=(10, 0))
tk.Entry(root, textvariable=bitrate_var, width=20).pack()

# 执行按钮
tk.Button(root, text="开始压缩", command=start_compression, bg="green", fg="white", height=2, width=20).pack(pady=20)

root.mainloop()
