import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class DataFrameTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def edit_lock(self, colum_count):
        # запрет редактирования первых colum_count столбцов
        for row in range(self.rowCount()):
            for col in range(colum_count):
                item = self.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def save_to_df(self):
        # получение размера таблицы
        rows = self.rowCount()
        cols = self.columnCount()

        # создание пустого списка для хранения данных
        data = []

        # извлечение данных из таблицы
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)

        # создание DataFrame с данными из таблицы
        df = pd.DataFrame(data, columns=[self.horizontalHeaderItem(
            col).text() for col in range(cols)])
        return df

    def add_row(self, x, y):
        # добавление строки в таблицу
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(str(x)))
        self.setItem(row_position, 1, QTableWidgetItem(str(y)))
        self.setItem(row_position, 2, QTableWidgetItem("0"))
        self.setItem(row_position, 3, QTableWidgetItem("0"))
        # запрет редактирования первых двух столбцов
        self.edit_lock(2)

    def remove_row(self, index):
        # удаление строки по индексу
        self.removeRow(index)

    def clear_table(self):
        # удаление всех строк из таблицы
        while self.rowCount() > 0:
            self.removeRow(0)
