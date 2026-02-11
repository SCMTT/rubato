"""
GUI界面模块

提供MIDI速度调整器的图形用户界面。
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional, Dict, Any


class GUI:
    """
    GUI类

    提供MIDI速度调整器的图形用户界面。
    """

    MIN_SPEED = 0.1
    MAX_SPEED = 3.0
    DEFAULT_SPEED = 1.0

    def __init__(self, processor):
        """
        初始化GUI

        参数:
            processor: MidiProcessor实例
        """
        self.processor = processor
        self.root = tk.Tk()
        self.root.title("MIDI速度调整器")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        self.input_file: Optional[str] = None
        self.output_file: Optional[str] = None
        self.current_speed: float = self.DEFAULT_SPEED
        self.is_processed: bool = False
        self._process_callback: Optional[Callable] = None

        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面布局"""
        self._create_title_frame()
        self._create_file_selection_frame()
        self._create_file_info_frame()
        self._create_speed_control_frame()
        self._create_button_frame()
        self._create_status_frame()

    def _create_title_frame(self):
        """创建标题区域"""
        title_frame = tk.Frame(self.root, pady=10)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="MIDI速度调整器",
            font=("Arial", 16, "bold")
        )
        title_label.pack()

    def _create_file_selection_frame(self):
        """创建文件选择区域"""
        file_frame = tk.LabelFrame(self.root, text="输入文件", padx=10, pady=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.file_path_var = tk.StringVar(value="未选择文件")

        file_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path_var,
            state="readonly",
            width=40
        )
        file_entry.pack(side=tk.LEFT, padx=5)

        select_button = tk.Button(
            file_frame,
            text="选择文件",
            command=self._on_select_file,
            width=10
        )
        select_button.pack(side=tk.RIGHT)

    def _create_file_info_frame(self):
        """创建文件信息显示区域"""
        info_frame = tk.LabelFrame(self.root, text="文件信息", padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.info_text = tk.Text(
            info_frame,
            height=5,
            width=50,
            state="disabled",
            bg="#f0f0f0"
        )
        self.info_text.pack()

    def _create_speed_control_frame(self):
        """创建速度控制区域"""
        speed_frame = tk.LabelFrame(self.root, text="速度调整", padx=10, pady=10)
        speed_frame.pack(fill=tk.X, padx=10, pady=5)

        slider_frame = tk.Frame(speed_frame)
        slider_frame.pack(fill=tk.X)

        self.speed_var = tk.DoubleVar(value=self.DEFAULT_SPEED)

        speed_scale = tk.Scale(
            slider_frame,
            from_=self.MIN_SPEED,
            to=self.MAX_SPEED,
            orient=tk.HORIZONTAL,
            resolution=0.1,
            variable=self.speed_var,
            command=self._on_speed_slider_change,
            length=400
        )
        speed_scale.pack()

        input_frame = tk.Frame(speed_frame, pady=5)
        input_frame.pack()

        tk.Label(input_frame, text="速度倍率:").pack(side=tk.LEFT)

        self.speed_entry = tk.Entry(input_frame, width=10)
        self.speed_entry.insert(0, str(self.DEFAULT_SPEED))
        self.speed_entry.pack(side=tk.LEFT, padx=5)

        self.speed_entry.bind("<KeyRelease>", self._on_speed_entry_change)

        help_label = tk.Label(
            speed_frame,
            text=f"范围: {self.MIN_SPEED}x (减速) - {self.MAX_SPEED}x (加速)",
            font=("Arial", 8),
            fg="gray"
        )
        help_label.pack()

    def _create_button_frame(self):
        """创建按钮区域"""
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack()

        self.process_button = tk.Button(
            button_frame,
            text="处理",
            command=self._on_process,
            width=15,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            state="disabled"
        )
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(
            button_frame,
            text="导出",
            command=self._on_export,
            width=15,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            state="disabled"
        )
        self.export_button.pack(side=tk.LEFT, padx=5)

        exit_button = tk.Button(
            button_frame,
            text="退出",
            command=self._on_exit,
            width=10,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Arial", 10)
        )
        exit_button.pack(side=tk.LEFT, padx=5)

    def _create_status_frame(self):
        """创建状态显示区域"""
        status_frame = tk.Frame(self.root, pady=10)
        status_frame.pack(fill=tk.X, padx=10)

        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_label.pack(fill=tk.X)

    def _on_select_file(self):
        """处理文件选择事件"""
        file_path = filedialog.askopenfilename(
            title="选择MIDI文件",
            filetypes=[("MIDI文件", "*.mid *.midi"), ("所有文件", "*.*")]
        )

        if file_path:
            self.input_file = file_path
            self.file_path_var.set(file_path)
            self.status_var.set(f"已选择: {file_path}")
            self.is_processed = False
            self.process_button.config(state="normal")
            self.export_button.config(state="disabled")

            try:
                self.processor.load_midi(file_path)
                info = self.processor.get_midi_info()
                self.update_file_info(info)
            except Exception as e:
                self.show_error(f"无法加载文件: {e}")
                self.process_button.config(state="disabled")

    def _on_process(self):
        """处理开始处理事件"""
        print("[GUI] _on_process 被调用")
        
        if not self.input_file:
            messagebox.showwarning("警告", "请先选择输入文件")
            return

        try:
            speed = float(self.speed_entry.get())
            if not (self.MIN_SPEED <= speed <= self.MAX_SPEED):
                messagebox.showerror(
                    "错误",
                    f"速度必须在{self.MIN_SPEED}到{self.MAX_SPEED}之间"
                )
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的速度倍率")
            return

        print(f"[GUI] 准备处理: 文件={self.input_file}, 速度={speed}")
        self.status_var.set("处理中...")
        self.root.update()

        if self._process_callback:
            print("[GUI] 调用处理回调函数")
            params = {
                "input_file": self.input_file,
                "speed": speed
            }
            self._process_callback(params)
            print("[GUI] 处理回调函数完成")
        else:
            print("[GUI] 警告: 未设置处理回调函数")
            messagebox.showerror("错误", "处理回调函数未设置")

    def _on_export(self):
        """处理导出事件"""
        if not self.is_processed:
            messagebox.showwarning("警告", "请先处理文件")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存MIDI文件",
            defaultextension=".mid",
            filetypes=[("MIDI文件", "*.mid"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                self.processor.save_midi(file_path)
                self.output_file = file_path
                self.show_success("文件导出成功！")
            except Exception as e:
                self.show_error(f"导出失败: {e}")

    def _on_speed_slider_change(self, value):
        """处理速度滑动条变化事件"""
        speed = float(value)
        self.current_speed = speed
        self.speed_entry.delete(0, tk.END)
        self.speed_entry.insert(0, f"{speed:.1f}")

    def _on_speed_entry_change(self, event):
        """处理速度输入框变化事件"""
        try:
            value = self.speed_entry.get()
            if value:
                speed = float(value)
                if self.MIN_SPEED <= speed <= self.MAX_SPEED:
                    self.current_speed = speed
                    self.speed_var.set(speed)
        except ValueError:
            pass

    def _on_exit(self):
        """处理退出事件"""
        self.root.quit()

    def update_file_info(self, info: Dict[str, Any]):
        """
        更新文件信息显示

        参数:
            info: MIDI文件信息字典
        """
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)

        info_str = (
            f"时长: {info['duration']:.2f} 秒\n"
            f"乐器数: {info['num_instruments']}\n"
            f"音符数: {info['num_notes']}\n"
            f"速度变化: {info['tempo_changes']} 次\n"
            f"调号变化: {info['key_signature_changes']} 次"
        )

        self.info_text.insert(tk.END, info_str)
        self.info_text.config(state="disabled")

    def set_processed(self, processed: bool):
        """
        设置处理状态

        参数:
            processed: 是否已处理
        """
        self.is_processed = processed
        if processed:
            self.export_button.config(state="normal")
            self.process_button.config(state="disabled")
        else:
            self.export_button.config(state="disabled")
            self.process_button.config(state="normal")

    def show_success(self, message: str):
        """
        显示成功消息

        参数:
            message: 消息内容
        """
        messagebox.showinfo("成功", message)
        self.status_var.set(message)

    def show_error(self, message: str):
        """
        显示错误消息

        参数:
            message: 错误消息
        """
        messagebox.showerror("错误", message)
        self.status_var.set(f"错误: {message}")

    def show_warning(self, message: str):
        """
        显示警告消息

        参数:
            message: 警告消息
        """
        messagebox.showwarning("警告", message)
        self.status_var.set(f"警告: {message}")

    def run(self):
        """运行GUI主循环"""
        self.root.mainloop()

    def set_process_callback(self, callback: Callable):
        """
        设置处理回调函数

        参数:
            callback: 处理回调函数
        """
        print(f"[GUI] 设置处理回调函数: {callback}")
        self._process_callback = callback

    def get_speed(self) -> float:
        """
        获取当前速度倍率

        返回:
            float: 速度倍率
        """
        try:
            return float(self.speed_entry.get())
        except ValueError:
            return self.DEFAULT_SPEED
