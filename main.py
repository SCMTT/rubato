"""
MIDI速度调整器 - 主程序入口

启动MIDI速度调整器应用程序。
"""

from midi_processor import MidiProcessor
from gui import GUI
from controller import Controller


def main():
    """
    主函数

    初始化并启动MIDI速度调整器应用程序。
    """
    processor = MidiProcessor()
    gui = GUI(processor)
    controller = Controller(gui, processor)

    controller.run()


if __name__ == "__main__":
    main()
