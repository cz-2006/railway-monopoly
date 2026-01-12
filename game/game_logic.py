"""
游戏逻辑核心
"""
import random
from enum import Enum

class StationType(Enum):
    STATION = 1
    TAX = 2
    FREE_PARKING = 3
    GO_TO_JAIL = 4
    JUST_VISITING = 5

class Station:
    """铁路站点类"""
    def __init__(self, name, position, price=0, station_type=StationType.STATION):
        self.name = name
        self.position = position
        self.price = price
        self.owner = None
        self.station_type = station_type
        self.house_count = 0
        self.rent_multiplier = 1.0
        
    def set_owner(self, player):
        self.owner = player
        
    def get_rent(self):
        """计算租金"""
        if self.owner is None or self.owner == self.player:
            return 0
        base_rent = self.price // 10
        return base_rent * (self.house_count + 1) * int(self.rent_multiplier)

class Player:
    """玩家类"""
    def __init__(self, name, is_ai=False):
        self.name = name
        self. is_ai = is_ai
        self.position = 0
        self.money = 2000
        self.properties = []
        self.in_jail = False
        self. jail_turns = 0
        
    def move(self, steps):
        """移动玩家"""
        old_position = self.position
        self.position = (self.position + steps) % 40
        
        # 如果绕过起点，获得200元
        if self.position < old_position:
            self.money += 200
            
    def buy_property(self, station):
        """购买物业"""
        if self.money >= station.price:
            self. money -= station.price
            station.set_owner(self)
            self.properties.append(station)
            return True
        return False
        
    def pay_rent(self, amount):
        """支付租金"""
        self.money -= amount
        
    def add_money(self, amount):
        """增加金钱"""
        self.money += amount
        
    def is_bankrupt(self):
        """检查是否破产"""
        return self.money < 0

class GameLogic:
    """游戏逻辑管理器"""
    def __init__(self):
        self.stations = self._create_stations()
        self.players = []
        self.current_player_index = 0
        self. game_over = False
        self. winner = None
        
    def _create_stations(self):
        """创建40个站点"""
        stations = []
        station_names = [
            "起点", "北京", "税收", "上海", "停泊", "广州", "免费停泊", "深圳",
            "监狱", "成都", "税收", "杭州", "停泊", "南京", "免费停泊", "武汉",
            "监狱", "西安", "税收", "长沙", "停泊", "沈阳", "免费停泊", "青岛",
            "监狱", "郑州", "税收", "哈尔滨", "停泊", "天津", "免费停泊", "重庆",
            "监狱", "苏州", "税收", "厦门", "停泊", "福州", "免费停泊", "回到起点"
        ]
        
        prices = [0, 100, 0, 100, 0, 120, 0, 140,
                  0, 160, 0, 180, 0, 200, 0, 220,
                  0, 240, 0, 260, 0, 280, 0, 300,
                  0, 320, 0, 340, 0, 360, 0, 380,
                  0, 400, 0, 420, 0, 440, 0, 0]
        
        for i, (name, price) in enumerate(zip(station_names, prices)):
            if name == "税收":
                station_type = StationType.TAX
            elif name == "停泊":
                station_type = StationType.FREE_PARKING
            elif name == "监狱" or name == "回到起点":
                station_type = StationType.GO_TO_JAIL
            else: 
                station_type = StationType. STATION
                
            stations.append(Station(name, i, price, station_type))
            
        return stations
        
    def add_player(self, name, is_ai=False):
        """添加���家"""
        player = Player(name, is_ai)
        self.players.append(player)
        
    def roll_dice(self):
        """掷骰子"""
        return random.randint(1, 6) + random.randint(1, 6)
        
    def execute_turn(self, player_index):
        """执行玩家回合"""
        player = self. players[player_index]
        
        # 掷骰子
        dice = self.roll_dice()
        player.move(dice)
        
        # 到达站点的处理
        station = self.stations[player.position]
        self._handle_station(player, station)
        
    def _handle_station(self, player, station):
        """处理站点逻辑"""
        if station.station_type == StationType. TAX:
            player.pay_rent(200)
        elif station.station_type == StationType.FREE_PARKING:
            player.add_money(100)
        elif station.station_type == StationType.GO_TO_JAIL: 
            player.in_jail = True
            player.jail_turns = 3
        elif station.station_type == StationType.STATION:
            if station.owner is None:
                # AI玩家自动决定是否购买
                if player.is_ai:
                    if player.money >= station.price and random.random() > 0.5:
                        player.buy_property(station)
            else:
                # 支付租金
                rent = station.get_rent()
                player.pay_rent(rent)
                station.owner. add_money(rent)
                
    def check_game_over(self):
        """检查游戏是否结束"""
        active_players = [p for p in self.players if not p.is_bankrupt()]
        if len(active_players) == 1:
            self.game_over = True
            self. winner = active_players[0]