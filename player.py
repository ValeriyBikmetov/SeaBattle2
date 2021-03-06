# -*- coding utf-8 -*-

from __future__ import annotations
from typing import Optional
import random
from telegram import Bot
from constants import ValueCells, TypeBoat, StatusPlayer, Message
from battle_array import  BattleArray, InfoArray, SimulatorInfo


class Player:
    """
    Класс Игрок. 
    Содержит свойства:
        player - идентификатор игрока
        name - имя игрока
        chat - идентификатор чата.
        battle_array - поле своих кораблей
        info - поле предполагаемого расположения кораблей противника
        opponent - ссылка на противника
        status - состояние игрока (стреляетЮ под обстрелом, размещает корабли)
    Содержит методы:
        def __init__(self, bot, player_id, first_name, chat_id): Конструктор
    """

    all_players = {}  # Здесь хранятся ссылки на всех созданных игроков

    def __init__(self, player_id: int = None, first_name: str = None, chat_id: int = None, bot: Bot = None) -> None:
        self.player_id = player_id
        self.name = first_name
        self.chat = chat_id
        self.bot = bot
        self.battle_array = BattleArray(self)
        self.info = InfoArray(self)
        self.opponent: Player = None
        self.status = StatusPlayer.SET_BOAT
        self.__class__.all_players[player_id] = self

    def __eq__(self, other: Player) -> bool:
        return self.player_id == other.player_id

    @classmethod
    def find_player(cls, identity: int) -> Player:
        return cls.all_players.get(identity)

    @classmethod
    def delete_players(cls, identity: int) -> bool:
        player: Player = cls.find_player(identity)
        enemy: Player = player.opponent
        if enemy:
            enemy_id: Player = player.opponent.player_id
            del(cls.all_players[enemy_id])
        del(cls.all_players[identity])

    @classmethod
    def delete_from_lst(cls, identity: int) -> bool:
        if identity in cls.all_players:
            del( cls.all_players[identity])

    @classmethod
    def signal_allocation(cls, message: Message):
        player_id: int = message.player_id
        player: Player = cls.find_player(player_id)
        player.allocation(message)


class RealPlayer(Player):
    """ 
    Класс реалльного игрока (человека), наследует класс PLayer
    Дополнительные поля: список количества устноаленных кораблей
    self.counts: list[int] = [0, 0, 0, 0]

    """
    def __init__(self, player_id: int = None, first_name: str = None, chat_id: int = None, bot: Bot = None) -> None:
        super().__init__(player_id, first_name, chat_id, bot)
        self.counts: list[int] = [0, 0, 0, 0]


    def allocation(self, message: Message) -> None:
        """
        Запрашивает координаты кораблей для размещения и размещает их на поле
        """
        ...

    def choice_partner(self) -> None:
        """ Диалог выбора партнера """
        return None


class Simulator(Player):
    """ Класс имитирующий поведение игргока в игре с реальным игроком """
    def __init__(self, player_id: int = None, first_name: str = None, chat_id: int = None, bot: Bot = None) -> None:
        identify = self.new_id()
        super().__init__(identify, first_name, chat_id, bot)
        
    def new_id(self) -> int:
        """ Генерирует уникальный идентификатор симулятора как игрока (player_id) """
        random.seed()
        player_id = random.randint(1, 1000)
        while player_id in self.all_players:
            player_id = random.randint(1, 1000)
        return player_id

    def allocation(self, message: Message) -> None:
        """ размещает корабли на поле """
        self.random_allocation()

    def random_allocation(self) -> None:
        """ Размещает корабли на поле в случайном порядке """
        random.seed()  # Инициализируем генератор случайных чисел
        # Размещаем 4-х палубный корабль
        self.boat_random_location(TypeBoat.deck_4)
        # Размещаем два 3-х палубных корабля
        for _ in range(2):
            self.boat_random_location(TypeBoat.deck_3)
        # Размещаем три 2-х палубных корабля
        for _ in range(3):
            self.boat_random_location(TypeBoat.deck_2)
        # Размещаем четыре одно палубных корабля
        for _ in range(4):
            self.boat_random_location(TypeBoat.deck_1)

    def boat_random_location(self, type_boat: TypeBoat) -> None:
        """
        type_boat - тип корабля (количество палуб)
        Вырабатываем координаты случайного расположения корабля,
        проверяем их на корректность. Если не корректны ищем другие, пока не станут корректными
        Заполняем игровое поле
        """
        # Массив координат запрещенных для размещения
        exclusion_area: list[tuple[int, int]] = self.battle_array.get_exclusion_area()
        length: int = int(type_boat.name[-1])  # Длина корабля равна последниму символу в имени типа, например, deck_3
        correct: bool = False
        orientation: bool = False
        row_b: int = 0
        row_e: int = 0
        column_b: int = 0
        column_e: int = 0
        while not correct:
            orientation = random.choice([True, False])  # Горионтально или вертикально
            if orientation:  # Если горизонтально, то выбираем строку
                row_b = random.randint(1, 10)  # Нулевая строк - строка заголовка
                column_b = random.randint(1, 11 - length)   # Нулевая колонка - номера строк, дальше 11 - length
                                                            # нельзя - не уложится в длину
                row_e = row_b
                column_e = column_b + length - 1
            else:  # Вертикальное расположение
                column_b = random.randint(1, 10)
                row_b = random.randint(1, 11 - length)
                column_e = column_b
                row_e = row_b + length - 1
            correct = (not (row_b, column_b) in exclusion_area) and (not (row_e, column_e) in exclusion_area)
        if orientation:  # Горизонтально
            for i in range(column_b, column_e + 1):
                self.battle_array[row_b][i] = ValueCells.deck.value
        else:
            for i in range(row_b, row_e + 1):
                self.battle_array[i][column_b] = ValueCells.deck.value