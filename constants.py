# -*- coding utf-8 -*-

from enum import Enum


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
    deck_1 = 4
    deck_2 = 3
    deck_3 = 2
    deck_4 = 1


class StatusGame(Enum):
    EARLY_EXIT = 0  # Досрочный выход
    DEFEAT = 1  # Поражение
    WIN = 2  # Победа
    CHANGE_PLAYER = 3  # Переход хода другому игроку



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
MES_INPUT = "Ввод"
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