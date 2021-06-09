from __future__ import annotations
from constants import Orientation, StatusBoat, TypeBoat
from constants import ValueCells, ResultShot, LST_TITLE

from utility import check_cell_name
from utility import coordinate_from_str
from utility import check_boat_coordinate


class Boat:
    """
    Класс корабля.
    Атрибуты: тип корабля, его ориентация, начальные координаты, статус (живой, подбит или потоплен),
    а так же словарь где ключи кортеж из строки и колонки, значение - соответствующий символ (Ж, П, У)
    Метод get_location выдает массив кортежей координат (строка, колонка)
    """
    def __init__(self, type_boat: TypeBoat, orientation: Orientation = Orientation.horizontal,
                 row: int = 0, column: int = 0) -> None:
        self.type_boat = type_boat
        self.orientation = orientation
        self.row: int = row
        self.column: int = column
        self.decks: dict[tuple, str]
        if row > 0 and column > 0:
            lst = self.get_location()
            self.decks = {cor: 'Ж' for cor in lst}
        else:
            self.decks = {}
        self.status: StatusBoat = StatusBoat.alive

    def get_location(self) -> list:
        """ Получаем массив координат ячеек корабля. Координаты в виде кортежей (строка, колонка)
        """
        length: int = self.type_boat.value  # Длина корабля
        if self.orientation == Orientation.horizontal:  # Горизонтальная ориентация
            begin = self.column  # Начальная колонка
            end = self.column + length  # Конечная колонка
            result = [(self.row, c) for c in range(begin, end)]  # Генерируем массив кортежей (координат)
        else:
            begin = self.row
            end = self.row + length
            result = [(r, self.column) for r in range(begin, end)]
        return result

    def get_exclusion_location(self) -> list:
        """
        Получаем массив эксклюзивных координат ячеек корабля (строка, колонка),
        в которые не должны попадать координаты ячеек других кораблей
        """
        length: int = self.type_boat.value  # Длина корабля
        if self.orientation == Orientation.horizontal:  # Горизонтальная ориентация
            if self.row == 1:  # Первая строка
                if self.column == 1:  # Начало корабля на первой колонке, о конце не беспокоимся
                    result = [(self.row, c) for c in range(self.column, self.column + length + 1)]
                    result += [(self.row + 1, c) for c in range(self.column, self.column + length + 1)]
                elif (self.column + length) == 11:  # Корабль концом упирается в последнюю колонку
                    result = [(self.row, c) for c in range(self.column - 1, self.column + length)]
                    result += [(self.row + 1, c) for c in range(self.column - 1, self.column + length)]
                else:  # Корабль с запасом, по крайней мере, по одной клетке по обе строны
                    result = [(self.row, c) for c in range(self.column - 1, self.column + length + 1)]
                    result += [(self.row + 1, c) for c in range(self.column - 1, self.column + length + 1)]
            elif self.row == 10:  # Корабль на последней строке
                if self.column == 1:  # Начало корабля на первой колонке, о конце не беспокоимся
                    result = [(self.row - 1, c) for c in range(self.column, self.column + length + 1)]
                    result += [(self.row, c) for c in range(self.column, self.column + length + 1)]
                elif (self.column + length) == 11:  # Корабль концом упирается в последнюю колонку
                    result = [(self.row -1, c) for c in range(self.column - 1, self.column + length)]
                    result += [(self.row, c) for c in range(self.column - 1, self.column + length)]
                else:  # Корабль с запасом, по крайней мере, по одной клетке по обе строны
                    result = [(self.row - 1, c) for c in range(self.column - 1, self.column + length + 1)]
                    result += [(self.row, c) for c in range(self.column - 1, self.column + length + 1)]
            else:  # Строка с кораблем не самая первая и не самая последняя
                if self.column == 1:  # Начало корабля на первой колонке, о конце не беспокоимся
                    result = [(self.row - 1, c) for c in range(self.column, self.column + length + 1)]
                    result += [(self.row, c) for c in range(self.column, self.column + length + 1)]
                    result += [(self.row + 1, c) for c in range(self.column, self.column + length + 1)]
                elif (self.column + length) == 11:  # Корабль концом упирается в последнюю колонку
                    result = [(self.row - 1, c) for c in range(self.column - 1, self.column + length)]
                    result += [(self.row, c) for c in range(self.column - 1, self.column + length)]
                    result += [(self.row + 1, c) for c in range(self.column - 1, self.column + length)]
                else:  # Корабль с запасом, по крайней мере, по одной клетке по обе строны
                    result = [(self.row - 1, c) for c in range(self.column - 1, self.column + length + 1)]
                    result += [(self.row, c) for c in range(self.column - 1, self.column + length + 1)]
                    result += [(self.row + 1, c) for c in range(self.column - 1, self.column + length + 1)]
        else:  # Вертикальная ориентация
            if self.column == 1:  # Корабль на первой колонке
                if self.row == 1:  # Начало коробля на первой строке
                    result = [(r, self.column) for r in range(self.row, self.row + length + 1)]
                    result += [(r, self.column + 1) for r in range(self.row, self.row + length + 1)]
                elif (self.row + length) == 11:  # Конец корабля на последней строке
                    result = [(r, self.column) for r in range(self.row - 1, self.row + length)]
                    result += [(r, self.column + 1) for r in range(self.row - 1, self.row + length)]
                else:  # У корабля серху и снизу есть свободные строки
                    result = [(r, self.column) for r in range(self.row - 1, self.row + length + 1)]
                    result += [(r, self.column + 1) for r in range(self.row - 1, self.row + length + 1)]
            elif self.column == 10:  #Корабль на последней колонк
                if self.row == 1:  # Начало коробля на первой строке
                    result = [(r, self.column) for r in range(self.row, self.row + length + 1)]
                    result += [(r, self.column - 1) for r in range(self.row, self.row + length + 1)]
                elif (self.row + length) == 11:  # Конец корабля на последней строке
                    result = [(r, self.column) for r in range(self.row - 1, self.row + length)]
                    result += [(r, self.column - 1) for r in range(self.row - 1, self.row + length)]
                else:  # У корабля серху и снизу есть свободные строки
                    result = [(r, self.column) for r in range(self.row - 1, self.row + length + 1)]
                    result += [(r, self.column - 1) for r in range(self.row - 1, self.row + length + 1)]
            else:  # И слева и справа от корабля есть колонки
                if self.row == 1:  # Начало коробля на первой строке
                    result = [(r, self.column + 1) for r in range(self.row, self.row + length + 1)]
                    result += [(r, self.column) for r in range(self.row, self.row + length + 1)]
                    result += [(r, self.column - 1) for r in range(self.row, self.row + length + 1)]
                elif (self.row + length) == 11:  # Конец корабля на последней строке
                    result = [(r, self.column + 1) for r in range(self.row - 1, self.row + length)]
                    result += [(r, self.column) for r in range(self.row - 1, self.row + length)]
                    result += [(r, self.column - 1) for r in range(self.row - 1, self.row + length)]
                else:  # У корабля серху и снизу есть свободные строки
                    result = [(r, self.column + 1) for r in range(self.row - 1, self.row + length + 1)]
                    result += [(r, self.column) for r in range(self.row - 1, self.row + length + 1)]
                    result += [(r, self.column - 1) for r in range(self.row - 1, self.row + length + 1)]
        return result

    def show_boat(self, battle_array: list) -> None:
        for key in self.decks:
            row, column = key
            battle_array[row][column] = self.decks[key]


class BattleArray:
    """
    Класс боевого расположения кораблей
    Атрибуты: игрок, владелец кораблей, список объектов кораблей
    Методы: shot(self, cell: str) -> ResultShot обрабатывает выстрел по этому полю, и возвращает его результат
            allocation(self, position: str) -> bool прверяет кооректность задааных координат и помещает в них корабль
            координаты получает в виде строки типа "а1-а4". Возвращает True если все хорошо, иначе False
            show_battle_array(self) -> None выводит изображение поля в текстовом формате
    """
    def __init__(self, player: 'Player') -> None:
        self.player:'Player' = player
        self.battle_array: list[Boat] = list()

    def shot(self, cell: str) -> ResultShot:
        """ Обрабатываем выстрел по нашему полю """
        if not check_cell_name(cell):  # Неправильный формат координат
            return ResultShot.to_miss
        else:
            coordinate = coordinate_from_str(cell)  # Получаем реальные координаты (строка, колонка)
            for boat in self.battle_array:
                if coordinate in boat.decks.keys():
                    if boat.status == StatusBoat.sink:
                        return ResultShot.to_miss
                    ch = boat.decks[coordinate]  # Что за символ в этой ячейке
                    if ch == ValueCells.deck.value:  # Если это "Ж" - значит попадание
                        boat.decks[coordinate] = ValueCells.hit.value  # Исправляем на "П"
                        if ValueCells.deck.value in boat.decks.values():  # Проверяем есть ли еще символы "Ж"
                            if boat.status != StatusBoat.hole:  # Они есть - статус пробоина
                                boat.status = StatusBoat.hole
                            return ResultShot.hit
                        else:  # Символов "Ж" нет, корабль потоплен
                            boat.status = StatusBoat.sink
                            for row, column in boat.decks.keys():
                                boat.decks[(row, column)] = ValueCells.sink.value
                            return ResultShot.sink
                    else:
                        return ResultShot.to_miss

    def allocation(self, coordinates: str) -> bool:
        position: list[tuple] = check_boat_coordinate(coordinates)
        # Получили список координат корабля (строка, колонка)
        if not position:
            return False
        # Проверим не попадают ли эти координаты на уже существующие
        exclusion_area = self.get_exclusion_area()
        for coordinate in position:
            if coordinate in exclusion_area:
                return False
        row_begin, column_begin = position[0]
        row_end, column_end = position[-1]
        if row_begin == row_end:  # Начальная и конечная строки равны - ориентация горизонтальная
            orientation = Orientation.horizontal
        else:
            orientation = Orientation.vertical
        length = len(position)  # Длина корабля соответствует его типу, а числовое значение типа - клоичеству
        counts = [0, 0, 0, 0, 0]  # Массив для количества уже установленных кораблей
        for boat in self.battle_array:
            if boat.type_boat == TypeBoat.deck_1:
                counts[1] += 1
            elif boat.type_boat == TypeBoat.deck_2:
                counts[2] += 1
            elif boat.type_boat == TypeBoat.deck_3:
                counts[3] += 1
            else:
                counts[4] += 1
        current_count: int = counts[length]  # Текущее количество кораблей, тип которых соответствует length
        type_count: list[tuple[str, int]] = [(name, value.value) for name, value in TypeBoat.__members__.items()]
        max_count: int = type_count[length - 1][1]  # Максимально допустимое количество данного типа кораблей
        if current_count < max_count:  # Можно еще разместить корабль такого типа
            type_boat: TypeBoat = TypeBoat[type_count[length - 1][0]]
            boat: Boat = Boat(type_boat, orientation, row_begin, column_begin)
            self.battle_array.append(boat)
            return True
        return False

    def show_battle_array(self) -> str:
        ch_list = list()
        ch_list.append(LST_TITLE)
        for i in range(1, 11):  # Добавляем еще 10 строк
            t = [str(i)]  # Номер строки
            t += [ValueCells.empty.value for _ in range(10)]  # Дополняем 10-ю пустыми полями
            ch_list.append(t)  # Добавляем сформированную строку в основной массив
        for boat in self.__array:
            boat.show_boat(ch_list)
        result: str = ''
        for i in range(10):
            row = ch_list[i]
            s = f'|{"|".join(row)}|'
            result += s + "\n"
        text = f'<pre>{result}</pre>'
        return text

    def get_exclusion_area(self) -> list[tuple[int, int]]:
        result:list[tuple[int, int]] = list()
        for boat in self.battle_array:
            result += boat.get_exclusion_location()
        return result

class InfoArray:
    def __init__(self, player: 'Player' = None) -> None:
        self.player = player
        # Создаем массив, добавляем заголовок столбцов и пустыми строками с их номерами
        self.field = list()
        self.field.append(LST_TITLE)  # Добавляем заголовки колонок
        for i in range(1, 11):  # Добавляем еще 10 строк
            t = [str(i)]  # Номер строки
            t += [ValueCells.empty.value for _ in range(10)]  # Дополняем 10-ю пустыми полями
            self.field.append(t)  # Добавляем сформированную строку в основной массив

    def show_info(self) -> str:
        str_field: str = ''
        for i in range(10):
            row = self.field[i]
            s = f'|{"|".join(row)}|'
            str_field += s + "\n"
        text = f'<pre>{str_field}</pre>'
        return text

    def add_result_shot(self, row: int, column: int, result_shot: ResultShot) -> None:
        # Фиксация результатов выстрела игрока по противнику
        if result_shot == ResultShot.to_miss:  # Если промах
            self.field[row][column] =  ValueCells.shot.value  # Ставим в "*"
        elif result_shot == ResultShot.hit:  # Попадание
            self.field[row][column] = ValueCells.hit.value
        elif result_shot == ResultShot.sink:  # Потоплен
            # Получаем координаты коробля от противника и по этим координатам ставим "У"
            battle_array = self.__player.opponent.battle_array.battle_array
            for boat in battle_array:
                if (row, column) in boat.decks.keys():
                    for r, c in boat.decks.keys():
                        self.field[r][c] = ValueCells.sink.value
                    return


class SimulatorInfo(InfoArray):
    def __init__(self, player: 'Player' = None) -> None:
        super().__init__(player)  # Вызываем конструктор родительского класса
        # Создаем квадратный массив 11Х11 для запрещенных для выстрелов поле, заполняем его еденицами
        # Если единица - поле под прицелом. Ноль - стрелять нельзя, будет мимо
        # Нулевую колонку и нулевую строку заполняем нулями, это не простреливаемая область
        self.exclusion_area = [[1 for _ in range(11)] for _ in range(11)]
        for i in range(11):
            self.exclusion_area[0][i] = 0
            self.exclusion_area[i][0] = 0

    def set_row_null(self, row: int, start: int, stop: int) -> None:
        try:
            for i in range(start, stop):
                self.exclusion_area[row][i] = 0
        except IndexError:
            return

    def set_column_null(self, column: int, start: int, stop: int) -> None:
        try:
            for i in range(start, stop):
                self.exclusion_area[i][column] = 0
        except IndexError:
            return

    def add_result_shot(self, row: int, column: int, result_shot: ResultShot) -> None:
        # Это фиксация результатов выстрела симулятора
        # Вызываем метод родительского класса для визуаоьного отображения результата
        super(SimulatorInfo, self).add_result_shot(row, column,result_shot)
        # Теперь пытаемся анаизировать сложившуюся ситуацию расставить приоритеты по ячейкам поля
        if result_shot == ResultShot.to_miss:
            self.exclusion_area[row][column] = 0   #  Обнуляем поле промаха
            return
        for r in range(1, 11):  # Проходим по всем строкам
            for c in range(1, 11):  # всем колонкам в строке
                ch = self.get_value_cell(r, c)
                if ch == ValueCells.hit.value:  # Поле с попаданием
                    self.hit_analysis(r, c)
                elif ch == ValueCells.sink.value:  # Поле с потопленым кораблем
                    self.sink_analysis(row, column)

    def hit_analysis(self, row: int, column: int) -> None:
        """
        Проверяем близьлежащие поля вокруг этого поля
        Если одно из этих полей так же с символом "П", то ясен вариант расположение корабля.
        В этом случае обследуем поля по концам пораженных полей в этом направлении
        иначе ставим вокруг поля приоритеты 2, а по углам 0
        """
        if self.field[row][column - 1] == ValueCells.hit.value or self.field[row][column + 1] == ValueCells.hit.value:
            self.check_left_right(row, column)
        elif self.field[row -1][column] == ValueCells.hit.value or self.field[row + 1][column] == ValueCells.hit.value:
            self.check_top_down(row, column)
        else:  # Нет попаданий вокруг этого. Ставим в окружающих клетках приоритеты = 2, а в угловых 0
            if row > 1:
                self.exclusion_area[row - 1][column] = 2  # Сверху
                if column > 1:
                    self.exclusion_area[row - 1][column - 1] = 0  # Левый верхний угол
                if column < 10:
                    self.exclusion_area[row - 1][column + 1] = 0  # Правый верхний угол
            if row < 10:
                self.exclusion_area[row + 1][column] = 2  #
                if column > 1:
                    self.exclusion_area[row + 1][column - 1] = 0  # Левый нижний угол
                if column < 10:
                    self.exclusion_area[row + 1][column + 1] = 0  # Правый нижний угол
            if column > 1:
                self.exclusion_area[row][column - 1] = 2
            if column < 10:
                self.exclusion_area[row][column + 1] = 2

    def check_left_right(self, row: int, column: int) -> None:
        """
        Если одно из конечных полей имеет символ "*", то помечаем его 0, а противоположное 3.
        Если же ни одно из полей не имеет символа "*", то помечаем их 2.
        Остальные клетки вокруг пораженных полей помечаем 0
        """
        ch: str = ValueCells.hit.value
        col: int = column
        while ch == ValueCells.hit.value:  # Идем влево до тех пор пока не появится символ не равный "П"
            col -= 1
            ch = self.field[row][col]
        if ch == ValueCells.shot.value or ch.isdigit():  # Стоит символ "*" или долшлт до нулевой колонки
            # Тогда ставим нули начинач с этой клетки до column, а сверху и снизу нули на 1 больше column
            # В клетке после column ставим приоритет 3
            self.exclusion_area[row][column + 1] = 3
            self.set_row_null(row, col, column)
            if row > 1:
                self.set_row_null(row - 1, col, column + 2)
            if row < 10:
                self.set_row_null(row + 1, col, column + 2)
            return
        elif ch == ValueCells.empty.value:
            # Стоит символ " " - временно до проверки правой стороны ставим 2, а далее до column нули
            left_col = col
            self.exclusion_area[row][col] = 2
            self.set_row_null(row, col - 1, column)
            if row > 1:
                self.set_row_null(row - 1, col, column + 2)
            if row < 10:
                self.set_row_null(row + 1, col , column + 2)
            # Идем вправо
            ch = ValueCells.hit.value
            col = column
            while ch == ValueCells.hit.value and col <= 10:
                col += 1
                ch = self.field[row][col]
            if col == 10:  # Дошли до конца. Справа больше ничего нет
                # Меняем слева приоритет на 3
                self.exclusion_area[row][left_col] = 3
                self.set_row_null(row, column + 1, col + 1)
                if row > 1:
                    self.set_row_null(row - 1, column, col + 1)
                if row < 10:
                    self.set_row_null(row + 1, column, col + 1)
                return
            elif ch == ValueCells.shot.value:  # Символ "*"
                # Меняем слева приоритет на 3
                self.exclusion_area[row][left_col] = 3
                self.set_row_null(row, column + 1, col + 2)
                if row > 1:
                    self.set_row_null(row - 1, column, col + 2)
                if row < 10:
                    self.set_row_null(row + 1, column, col + 2)
                return
            elif ch == ValueCells.empty.value:  # Символ " ". С обоих концов приоритеты 2
                self.exclusion_area[row][col] = 2
                self.set_row_null(row, column + 1, col)
                if row > 1:
                    self.set_row_null(row - 1, column, col + 1)
                if row < 10:
                    self.set_row_null(row + 1, column, col + 1)
                return

    def check_top_down(self, row: int, column: int) -> None:
        ch: str = ValueCells.hit.value
        cur_row: int = row
        while ch == ValueCells.hit.value:  # Идем вверх до тех пор пока не появится символ не равный "П"
            cur_row -= 1
            ch = self.field[cur_row][column]
        if ch == ValueCells.shot.value or ch != ValueCells.empty.value:
            # Символ "*" или дошли до нулевой строки. Выше ничего нет. Ставим на противоположном конце приоритет 3 .
            self.exclusion_area[row + 1][column] = 3
            # Ставим 0 в остальных полях
            self.set_column_null(column, cur_row, row)
            if column > 1:
                self.set_column_null(column - 1, cur_row, row + 2)
            if column < 10:
                self.set_column_null(column + 1, cur_row, row + 2)
            return
        elif ch == ValueCells.empty.value:  # Временно до исследования вниз ставим проритет 2
            self.exclusion_area[cur_row][column] = 2
            # Ставим 0 в остальных полях
            self.set_column_null(column, cur_row + 1, row)
            if column > 1:
                self.set_column_null(column - 1, cur_row, row + 2)
            if column < 10:
                self.set_column_null(column + 1, cur_row, row + 2)
            top_row = cur_row  # Запоминаем строку с приоритетом 2
            ch = ValueCells.hit.value
            cur_row = row
            while ch == ValueCells.hit.value and cur_row <= 10:
                cur_row += 1
                ch = self.field[cur_row][column]
            if ch == ValueCells.shot.value or cur_row == 10:
                # Символ "*" или дошли до нижней строки. Меняем приоритет в верху на 3 и воруг нули
                self.exclusion_area[top_row][column] = 3
                self.set_column_null(column, row, cur_row + 2)
                if column > 1:
                    self.set_column_null(column - 1, row, cur_row + 2)
                if column < 10:
                    self.set_column_null(column + 1, row, cur_row + 2)
            elif ch == ValueCells.empty.value:  # Символ " ". На обоих концах приоритеты 2.
                self.exclusion_area[cur_row][column] = 2
                self.set_column_null(column, row, cur_row)
                if column > 1:
                    self.set_column_null(column - 1, row, cur_row + 2)
                if column < 10:
                    self.set_column_null(column + 1, row, cur_row + 2)

    def sink_analysis(self, row: int, column: int) -> None:
        """
        Находим в базе противника этот корабль. Получаем координаты его расположения.
        Если в этих координатах 0 - это уже обработанный корабль. Выход
        Иначе заносим 0 по этим координатам и вокруг этих координат
        """
        opponent_array = self.player.opponent.battle_array.battle_array
        for boat in opponent_array:
            if (row, column) in boat.decks.keys():  # Нужный корабль
                location: list[tuple] = boat.get_location()
                r, c = location[0]
                if self.exclusion_area[r][c] == 0:
                    break
                else:
                    r, c = location[0]  # Начало корабля
                    orientation = boat.orientation
                    length = len(location)
                    if orientation == Orientation.horizontal:
                        for i in range(r - 1, r + 2):
                            if r < 1 or r > 10:
                                continue
                            for j in range(c - 1, c + length + 1):
                                if c < 1 or c > 10:
                                    continue
                                self.exclusion_area[i][j] = 0
                    else:
                        for i in range(r - 1, r + length + 1):
                            if r < 1 or r > 10:
                                continue
                            for j in range(c - 1, c + 2):
                                if c < 1 or c > 10:
                                    continue
                                self.exclusion_area[i][j] = 0

