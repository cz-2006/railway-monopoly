"""
游戏窗口UI
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkFont
from game.game_logic import GameLogic
import threading

class GameWindow:
    """游戏窗口类"""
    def __init__(self, root):
        self.root = root
        self.game = GameLogic()
        
        # 添加玩家
        self. game.add_player("玩家", is_ai=False)
        self.game.add_player("AI对手", is_ai=True)
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        """设置UI界面"""
        # 创建主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：棋盘显示
        left_frame = tk.Frame(main_frame, width=600, bg="lightblue")
        left_frame. pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(left_frame, text="铁路环游游戏棋盘", font=("Arial", 16, "bold"), bg="lightblue").pack()
        
        self.board_canvas = tk.Canvas(left_frame, width=550, height=550, bg="white", relief=tk.RAISED, bd=2)
        self.board_canvas.pack(pady=10)
        self.draw_board()
        
        # 右侧：信息面板
        right_frame = tk.Frame(main_frame, width=350, bg="lightyellow")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 游戏状态
        tk.Label(right_frame, text="游戏信息", font=("Arial", 14, "bold"), bg="lightyellow").pack()
        
        self.status_text = scrolledtext.ScrolledText(right_frame, height=15, width=40, font=("Arial", 10))
        self.status_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # 按钮框架
        button_frame = tk. Frame(right_frame, bg="lightyellow")
        button_frame.pack(pady=10)
        
        self.roll_button = tk.Button(button_frame, text="掷骰子", command=self.roll_dice_click, 
                                      font=("Arial", 12), width=15, bg="lightgreen")
        self.roll_button. pack(pady=5)
        
        self.buy_button = tk.Button(button_frame, text="购买站点", command=self.buy_property_click,
                                     font=("Arial", 12), width=15, bg="lightcyan")
        self.buy_button.pack(pady=5)
        
        self.end_turn_button = tk.Button(button_frame, text="结束回合", command=self. end_turn_click,
                                          font=("Arial", 12), width=15, bg="lightsalmon")
        self.end_turn_button.pack(pady=5)
        
        self.quit_button = tk.Button(button_frame, text="退出游戏", command=self.quit_game,
                                      font=("Arial", 12), width=15, bg="lightgray")
        self.quit_button.pack(pady=5)
        
    def draw_board(self):
        """绘制棋盘"""
        self.board_canvas.delete("all")
        
        # 绘制棋盘格子
        cell_size = 50
        grid_size = 8
        
        for row in range(grid_size):
            for col in range(grid_size):
                x1 = col * cell_size + 25
                y1 = row * cell_size + 25
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # 绘制格子
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
        
        # 绘制玩家位置
        self.draw_players()
        
        # 显示站点信息
        self.board_canvas.create_text(275, 10, text="铁路环游游戏", font=("Arial", 12, "bold"))
        
    def draw_players(self):
        """绘制玩家位置"""
        for i, player in enumerate(self.game.players):
            position = player.position
            row = position // 8
            col = position % 8
            
            x = col * 50 + 50
            y = row * 50 + 50
            
            # 绘制玩家圆圈
            color = "blue" if i == 0 else "red"
            self.board_canvas. create_oval(x-15, y-15, x+15, y+15, fill=color, outline="black")
            self.board_canvas.create_text(x, y, text=str(i+1), fill="white", font=("Arial", 10, "bold"))
            
    def update_display(self):
        """更新显示信息"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text. delete(1.0, tk. END)
        
        for i, player in enumerate(self.game.players):
            status = "AI" if player.is_ai else "玩家"
            bankrupt = "破产" if player.is_bankrupt() else "活跃"
            current = ">>> 当前回合" if i == self.game.current_player_index else ""
            
            text = f"\n【{status}】{player.name} {current}\n"
            text += f"  资金:  ¥{player.money}\n"
            text += f"  位置: {self.game.stations[player.position].name}\n"
            text += f"  物业数: {len(player.properties)}\n"
            text += f"  状态: {bankrupt}\n"
            text += "-" * 40 + "\n"
            
            self.status_text.insert(tk.END, text)
            
        self.status_text.config(state=tk.DISABLED)
        
        self.draw_board()
        
    def roll_dice_click(self):
        """掷骰子按钮点击"""
        if self.game.current_player_index == 0:  # 只有人类玩家能点击
            self.execute_player_turn()
        else:
            messagebox.showinfo("提示", "请等待AI玩家完成回合")
            
    def execute_player_turn(self):
        """执行玩家回合"""
        self.roll_button.config(state=tk. DISABLED)
        self.buy_button.config(state=tk.DISABLED)
        
        self.game.execute_turn(self.game.current_player_index)
        
        # 检查破产
        current_player = self.game.players[self.game.current_player_index]
        if current_player.is_bankrupt():
            messagebox.showwarning("破产", f"{current_player.name} 已经破产！")
            
        self.game.check_game_over()
        if self.game.game_over:
            messagebox.showinfo("游戏结束", f"游戏结束！{self.game.winner.name} 赢了！")
            self.root.quit()
            
        self.update_display()
        
    def buy_property_click(self):
        """购买物业按钮点击"""
        if self.game.current_player_index != 0:
            messagebox. showinfo("提示", "只有在你的回合才能购买物业")
            return
            
        player = self.game.players[0]
        station = self.game.stations[player.position]
        
        if station.owner is None and station.price > 0:
            if player.money >= station.price:
                if messagebox.askyesno("购买", f"购买 {station.name}？价格:  ¥{station.price}"):
                    player.buy_property(station)
                    messagebox.showinfo("成功", f"购买了 {station.name}")
                    self.update_display()
            else:
                messagebox.showwarning("资金不足", "你的资金不足以购买该物业")
        else:
            messagebox.showinfo("提示", "该站点无法购买或已被拥有")
            
    def end_turn_click(self):
        """结束回合按钮点击"""
        if self.game.current_player_index == 0:
            # 切换到AI玩家
            self.game. current_player_index = 1
            self.roll_button.config(state=tk.DISABLED)
            self.buy_button.config(state=tk. DISABLED)
            self.end_turn_button.config(state=tk.DISABLED)
            
            # 在线程中执行AI回合
            self.root.after(1000, self. ai_turn)
        
    def ai_turn(self):
        """AI玩家回合"""
        self.game.execute_turn(1)
        
        # 检查破产
        ai_player = self.game.players[1]
        if ai_player.is_bankrupt():
            messagebox.showwarning("破产", "AI对手已经破产！你赢了！")
            self.root.quit()
            
        self.game.check_game_over()
        if self.game.game_over:
            messagebox.showinfo("游戏结束", f"游戏结束！{self. game.winner.name} 赢了！")
            self.root.quit()
            
        # 切换回玩家
        self.game. current_player_index = 0
        self.roll_button. config(state=tk.NORMAL)
        self.buy_button.config(state=tk. NORMAL)
        self.end_turn_button.config(state=tk.NORMAL)
        
        self.update_display()
        
    def quit_game(self):
        """退出游戏"""
        if messagebox.askyesno("确认", "确定要退出游戏吗？"):
            self.root.quit()