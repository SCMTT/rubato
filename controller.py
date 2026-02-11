"""
控制器模块

协调GUI和MIDI处理器之间的交互。
"""

from typing import Dict, Any
from midi_processor import MidiProcessor
from gui import GUI


class Controller:
    """
    控制器类

    负责协调GUI和MidiProcessor之间的交互。
    """

    def __init__(self, gui: GUI, processor: MidiProcessor):
        """
        初始化控制器

        参数:
            gui: GUI实例
            processor: MidiProcessor实例
        """
        self.gui = gui
        self.processor = processor

        self._setup_callbacks()

    def _setup_callbacks(self):
        """设置GUI回调函数"""
        self.gui.set_process_callback(self.process_midi)

    def process_midi(self, params: Dict[str, Any]):
        """
        处理MIDI文件

        参数:
            params: 包含处理参数的字典
                - input_file: 输入文件路径
                - speed: 速度倍率
        """
        input_file = params["input_file"]
        speed = params["speed"]

        try:
            print(f"[DEBUG] 开始处理 MIDI 文件: {input_file}, 速度: {speed}x")
            
            if not self.processor.is_loaded():
                raise RuntimeError("MIDI 文件未加载，请先选择文件")
            
            print(f"[DEBUG] 调用 adjust_speed...")
            self.processor.adjust_speed(speed)
            print(f"[DEBUG] adjust_speed 完成")
            
            speed_text = "加速" if speed > 1.0 else "减速" if speed < 1.0 else "原速"
            message = f"MIDI文件{speed_text}处理成功！\n速度: {speed}x"
            
            print(f"[DEBUG] 准备显示成功消息...")
            self.gui.show_success(message)
            print(f"[DEBUG] 成功消息已显示")
            
            print(f"[DEBUG] 设置处理状态为 True...")
            self.gui.set_processed(True)
            print(f"[DEBUG] 处理完成")

        except FileNotFoundError as e:
            print(f"[ERROR] 文件不存在: {e}")
            self.gui.show_error(f"文件不存在: {e}")
        except ValueError as e:
            print(f"[ERROR] 参数错误: {e}")
            self.gui.show_error(f"参数错误: {e}")
        except RuntimeError as e:
            print(f"[ERROR] 运行时错误: {e}")
            self.gui.show_error(f"处理失败: {e}")
        except Exception as e:
            print(f"[ERROR] 未知错误: {e}")
            import traceback
            traceback.print_exc()
            self.gui.show_error(f"处理失败: {e}")

    def run(self):
        """运行应用程序"""
        self.gui.run()
