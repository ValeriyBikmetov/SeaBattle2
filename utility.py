# -*- coding utf-8 -*-

from __future__ import annotations
from typing import Optional
from threading import Timer
import uuid

import constants as const


def check_cell_name(name: str) -> bool:
    """ Проверяем коррктность наименования ячейки игрового поля"""
    if len(name) < 2:
        return False
    s0 = name[0]
    if s0 == '#' or s0 not in const.LST_TITLE:
        return False
    s0 = name[1:]
    try:
        num = int(s0)
        if num < 1 or num > 10:
            return False
    except ValueError:
        return False


def check_boat_coordinate(coordinate: str) -> Optional:
    """
    Проверяет строку коррдинат на корректность написания
    :param coordinate: строка координат типа "а1-а4"
    :return: возвращает список кортежей из числовых номеров строк и колонок, либо None при ошибках
    """
    try:
        s0, s1 = coordinate.split('-')
        s0 = s0.strip()
        s1 = s1.strip()
        if not check_cell_name(s0) or not check_cell_name(s1):
            return None
    except ValueError:
        return None
    begin_r, begin_c = coordinate_from_str(s0)
    end_r, end_c = coordinate_from_str(s1)
    if begin_r == end_r and begin_c != end_c:  # Горизонтальный корабль
        num_decks = end_c - begin_c + 1  # Длина корабля (количество палуб)
        if num_decks > 4 or num_decks < 1:  # Неправильная длина корабля
            return None
        return [(begin_r, begin_c + i) for i in range(num_decks)]
    elif begin_r != end_r and begin_c == end_c:  # Вертикальный корабль
        num_decks = end_r - begin_r + 1  # Длина корабля (количество палуб)
        if num_decks > 4 or num_decks < 1:  # Неправильная длина корабля
            return None
        return [(begin_r + i, begin_c) for i in range(num_decks)]
    else:
        return None  # Неправильный корабль


def coordinate_from_str(cell: str) -> tuple:
    """ Преобразуем строку координат ячейки в реальные строку и колонку"""
    s0 = cell[0]
    s1 = cell[1:]
    column = const.LST_TITLE.index(s0)
    row = int(s1)
    return row, column


def generate_uuid() -> str:
    uid = uuid.uuid4()
    return str(uid)


def find_player_in_list(player_id: int, lst: list) -> bool:
    """ Проверяем наличие игрока в списке"""
    for player in lst:
        if player.player_id == player_id:
            return True
    return False


def find_partner_in_rounds(player_id: int, lst: list) -> Optional:
    """
    Ищем партнера игрока
    """
    for round in lst:
        if round.player_a.player_id == player_id:
            return round.player_b.name
        elif round.player_b.player_id == player_id:
            return round.player_a.name
    return None


def coordinate_to_str(begin: tuple, end: tuple) -> str:
    """ Преобразуем координаты корабля в строку
    """
    if begin == end:  # Однопалубный корабль
        r_b, c_b = begin
        s_rb = str(r_b)
        s_cb = const.LST_TITLE[c_b]
        return f'{s_cb}{s_rb}-{s_cb}{s_rb}'
    else:
        r_b, c_b = begin
        s_rb = str(r_b)
        s_cb = const.LST_TITLE[c_b]
        r_e, c_e = end
        s_re = str(r_e)
        s_ce = const.LST_TITLE[c_e]
        return f'{c_b}{r_b}-{c_e}{r_e}'


def timer_timeout(lst_games: list, interval: float, bot: 'Bot') -> None:
    if lst_games:
        for game in lst_games:
            if game.time_out >= const.TIMEOUT or game.game_over:
                player_a = game.player_a
                player_b = game.player_b
                bot.send_message(player_a.chat, const.MES_TIMEOUT)
                bot.send_message(player_b.chat, const.MES_TIMEOUT)
                game.delete_players()
                lst_games.remove(game)
    Timer(interval, timer_timeout, [lst_games, interval]).start()


# Получить текущее время в секундах
# current_time = lambda: int(round(time.time()))
# далее вызов current_time()
"""
Таймер как метод
*****************************************
from threading import Timer
import time

def hello(*num):
	print(f'{str(num)} It is {time.time}')
	next = num + 1
	Timer(10.0, hello, [next]).start()

hello(1)
*****************************************
Это как класс
*****************************************
from threading import Timer,Thread,Event


class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    print 'ipsem lorem'

t = perpetualTimer(5,printer)
t.start()
"""
