"""
铁路环游游戏 - 主程序入口
"""
import tkinter as tk
from game. game_window import GameWindow

def main():
    root = tk.Tk()
    root.title("铁路环游游戏")
    root.geometry("1000x700")
    
    game = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()