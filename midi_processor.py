"""
MIDI处理核心模块

该模块负责MIDI文件的加载、速度调整和保存操作。
基于pretty_midi库实现。
"""

import pretty_midi
import numpy as np
import os
from typing import Optional, Dict, Any


class MidiProcessor:
    """
    MIDI处理器类

    提供MIDI文件的加载、速度调整、保存和信息获取功能。
    """

    MIN_SPEED = 0.1
    MAX_SPEED = 3.0

    def __init__(self):
        """初始化MIDI处理器"""
        self.midi: Optional[pretty_midi.PrettyMIDI] = None
        self.original_file: Optional[str] = None

    def load_midi(self, file_path: str) -> bool:
        """
        加载MIDI文件

        参数:
            file_path: MIDI文件路径

        返回:
            bool: 加载成功返回True，失败返回False

        异常:
            FileNotFoundError: 文件不存在
            Exception: 文件解析错误
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        try:
            self.midi = pretty_midi.PrettyMIDI(file_path)
            self.original_file = file_path
            return True
        except Exception as e:
            self.midi = None
            self.original_file = None
            raise Exception(f"无法解析MIDI文件: {e}")

    def adjust_speed(self, speed_factor: float) -> None:
        """
        调整MIDI播放速度

        参数:
            speed_factor: 速度倍率（0.1-3.0）
                        小于1为减速，大于1为加速，1.0为原速

        异常:
            ValueError: 速度倍率超出范围
            RuntimeError: 未加载MIDI文件
        """
        if not self.midi:
            raise RuntimeError("请先加载MIDI文件")

        if not self.MIN_SPEED <= speed_factor <= self.MAX_SPEED:
            raise ValueError(
                f"速度倍率必须在{self.MIN_SPEED}到{self.MAX_SPEED}之间"
            )

        if not self.midi._tick_scales:
            return

        ticks = np.array([ts[0] for ts in self.midi._tick_scales])
        scales = np.array([ts[1] for ts in self.midi._tick_scales])
        scales /= speed_factor
        self.midi._tick_scales = list(zip(ticks, scales))

    def save_midi(self, output_path: str) -> bool:
        """
        保存MIDI文件

        参数:
            output_path: 输出文件路径

        返回:
            bool: 保存成功返回True，失败返回False

        异常:
            RuntimeError: 未加载MIDI文件
            Exception: 文件保存错误
        """
        if not self.midi:
            raise RuntimeError("请先加载MIDI文件")

        try:
            self.midi.write(output_path)
            return True
        except Exception as e:
            raise Exception(f"保存MIDI文件失败: {e}")

    def get_midi_info(self) -> Dict[str, Any]:
        """
        获取MIDI文件信息

        返回:
            dict: 包含MIDI文件信息的字典
                - duration: 时长（秒）
                - num_instruments: 乐器数量
                - num_notes: 音符总数
                - tempo_changes: 速度变化次数
                - key_signature_changes: 调号变化次数

        异常:
            RuntimeError: 未加载MIDI文件
        """
        if not self.midi:
            raise RuntimeError("请先加载MIDI文件")

        num_notes = sum(len(inst.notes) for inst in self.midi.instruments)
        tempo_changes = len(self.midi._tick_scales)

        return {
            "duration": self.midi.get_end_time(),
            "num_instruments": len(self.midi.instruments),
            "num_notes": num_notes,
            "tempo_changes": tempo_changes,
            "key_signature_changes": len(self.midi.key_signature_changes)
        }

    def is_loaded(self) -> bool:
        """
        检查是否已加载MIDI文件

        返回:
            bool: 已加载返回True，否则返回False
        """
        return self.midi is not None

    def get_current_file(self) -> Optional[str]:
        """
        获取当前加载的文件路径

        返回:
            str: 文件路径，未加载时返回None
        """
        return self.original_file
