# -*- coding utf-8 -*-

from enum import Enum
from dataclasses import dataclass


class ValueCells(Enum):
    deck = 'Ж'  # Символ корабля
    empty = ' '  # Символ пустого места
    hit = 'П'  # Попадание
    shot = '*'  # Выстрел
    sink = 'У'  # Потоплен
    col = '|'  # Символ разделителя колонки


class ResultShot(Enum):
    to_miss = 1  # Результат выстрела - промах
    hit = 2      # Результат выстрела - попадание
    sink = 3     # Потоплен


class StatusBoat(Enum):
    alive = 1  # Не поврежден
    hole = 2  # Есть пробоины
    sink = 3  # Потоплен


class Orientation(Enum):
    horizontal = 1
    vertical = 2


class TypeBoat(Enum):
    deck_1 = 1
    deck_2 = 2
    deck_3 = 3
    deck_4 = 4


class StatusGame(Enum):
    EARLY_EXIT = 0  # Досрочный выход
    DEFEAT = 1  # Поражение
    WIN = 2  # Победа
    CHANGE_PLAYER = 3  # Переход хода другому игроку


class StatusPlayer(Enum):
    TO_FIRE = 1  # Мы обстреливаем
    UNDER_FIRE = 2  # Нас обстреливают
    SET_BOAT = 3  # Рамещаем корабли


class TypeMessage(Enum):
    LOCATE = 1


@dataclass
class Message:
    player_id: int
    type_msg: TypeMessage
    message: str


MES_ERROR_COORDINATE = 'Неправильное задание координаты'
MES_HIT = 'Попадание'
MES_MISS = 'Промах'
MES_WHAT_DO = 'Привет {}: {}. Что будете делать?'
MES_CHOICE_PARTNER = 'Выберите партнера(введите его id):'
MES_WAIT = 'Нет партнера. Пригласите друга'
MES_TIMEOUT = 'Время бездействия более 5 минут. Игра удалена'
MES_YOUR_MOVE = 'Ваш ход'
MES_OTHER_MOVE = 'Ход противника'
MES_ALREADY_IN_GAME = '{} вы уже в игре'
MES_ASK_POSITION = 'Введите координаты {}-х палубного корабля'
MES_INPUT_FOUR_DECK = "Введите координаты четырехпалубного корабля"
MES_INPUT_THREE_DECK = "Введите координаты трехпалубного корабля"
MES_INPUT_TWO_DECK = "Введите координаты двухпалубного корабля"
MES_INPUT_ONE_DECK = "Введите координаты однопалубного корабля"
MES_QUIT = "До свидания"

TIMEOUT = 300.0  # Время бездействия, по истечении котрого иг ра удаляется
TOKEN = "1676624664:AAGswbvETbFWoaHrpAxqx6J0UVLwtRP07_k"
LST_TITLE = list('#абвгдежзик')
START_BUTTONS = [["Играть с ботом"],
                 ["Играть с партнером"],
                 ["Отмена"]]
POSITION_BUTTONS = [["а","б","в","г","д","е","ж","з","и","к"],
                    ["1","2","3","4","5","6","7","8","9","10"],
                    ["-"],
                    ["Ввод"]]