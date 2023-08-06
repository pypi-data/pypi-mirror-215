import os
import subprocess
import sys

import numpy as np
import pandas as pd

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout,
                             QHeaderView, QMainWindow, QMessageBox,
                             QPushButton, QSlider, QVBoxLayout, QWidget)


from .data_frame_table import DataFrameTable
from .widgets import Magnifier, PlotCanvas, ImageCanvas

# create_plot - для подключения обработчика к ui (Кнопка Создать график)

path = os.path.abspath(os.path.dirname(__file__))


def start_digitizer(df, path_to_image):
    """
    Запускает процесс оцифровки.
    """
    locations = list(df.apply(lambda row: (
        row['Y Image'], row['X Image']), axis=1))
    points = list(df.apply(lambda row: (row['Y Plot'], row['X Plot']), axis=1))
    script_path = "plotdigitizer.py"
    script_path = os.path.join(path, script_path)
    pts = " ".join([f"-p {','.join(map(str,pt))}" for pt in points])
    locs = " ".join([f"-l {','.join(map(str,pt))}" for pt in locations])
    cmd = "python \"" + script_path + "\" \"" + path_to_image + "\" " + f"{pts} {locs}"

    returncode = subprocess.call(cmd)

    if returncode != 0:
        # Обработка ошибки
        print(script_path)
        print(path_to_image)
        print(path)
        #print(sys.path)
        print(f"Ошибка при запуске команды: код возврата {returncode}")

    return returncode


  
def replace_placeholder(
        parent,
        widget_new,
        placeholder_name,
        fixed_size=False):
    """
    Заменяет плейсхолдер-виджет на новый виджет в окне.

    :param parent: виджет, в котором производится замена
    :type parent: QWidget
    :param widget_new: новый виджет для замены
    :type widget_new: QWidget
    :param placeholder_name: имя плейсхолдера-виджета для замены
    :type placeholder_name: str
    :param fixed_size: флаг для установки фиксированного размера нового виджета
    :type fixed_size: bool
    :param save_minimum_size: флаг для сохранения минимального размера нового виджета
    :type save_minimum_size: bool
    """
    # Найти старый виджет по имени
    widget_old = parent.findChild(QWidget, placeholder_name)
    # Получить родительский layout для старого виджета
    containingLayout = widget_old.parent().layout()
    # Заменить старый виджет на новый в layout
    containingLayout.replaceWidget(widget_old, widget_new)


    # Сохранить размеры
    # Сохранить минимальный размер для нового виджета
    widget_new.setMinimumSize(widget_old.minimumSize())

    # Установить фиксированный размер для нового виджета
    if fixed_size:
        widget_new.setFixedSize(widget_old.size())


def sort_lists(x, y):
    """
    Отсортировать два списка (x и y) по возрастанию значений в списке x.
    Используется для построения графика по точкам
    :param x: список значений для сортировки
    :type x: list
    :param y: список значений, соответствующих значениям в списке x
    :type y: list
    :return: кортеж из двух отсортированных списков (x_sorted, y_sorted)
    :rtype: tuple
    """
    # Создаем список пар (x, y)
    xy_pairs = list(zip(x, y))
    # Сортируем список пар по значению x
    xy_pairs.sort(key=lambda pair: pair[0])
    # Разделяем отсортированные пары обратно на два списка
    x_sorted, y_sorted = zip(*xy_pairs)
    return list(x_sorted), list(y_sorted)


# Виджет кнопок, в нём находятся: текстовая подсказка, лупа, слайдер, кнопки
class ButtonsWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Загрузка дизайна виджета из файла
        uic.loadUi(os.path.join(path, "ui", "buttons.ui"), self)


# Виджет просмотра графика - 2 окошка: в левом оригинальное изображение, в
# правом построенный по точкам график
class GraphPreviewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Загрузка дизайна виджета из файла
        uic.loadUi(os.path.join(path, "ui", "plots.ui"), self)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Plot Scanner")
        # Горизонтальный layout: слева кнопки и таблица, справа графики
        hbox = QHBoxLayout()
        # Заморозить левый layout с кнопками, чтобы не растягивался
        hbox.setStretch(1, 2)
        # Вертикальный layout: сверху кнопки, снизу таблица точек
        vbox = QVBoxLayout()
        hbox.addLayout(vbox)

        buttons = ButtonsWidget()
        graph = GraphPreviewer()
        vbox.addWidget(buttons)
        hbox.addWidget(graph)

        # Центральный виджета для главного окна
        cw = QWidget()
        cw.setLayout(hbox)
        self.setCentralWidget(cw)

        # Найти кнопки, созданные в дизайнере
        self.button_load = buttons.findChild(QPushButton, "loadButton")
        self.button_create = buttons.findChild(QPushButton, "createButton")
        self.button_save = buttons.findChild(QPushButton, "saveButton")
        # Найди слайдер масштабирования лупы
        self.scale_slider = buttons.findChild(QSlider, "scaleSlider")

        # Обработчики нажатия
        self.button_load.clicked.connect(self.load_plot_image)
        self.button_save.clicked.connect(self.save_points)
        self.button_create.clicked.connect(self.create_plot)

        # Канвасы для вывода изображения непосредственно в окно приложения
        self.origImCanvas = ImageCanvas(self)
        self.readyPlotCanvas = PlotCanvas()
        self.magnifierImCanvas = Magnifier(self)

        # Создание таблицы с 4 столбцами
        self.table = DataFrameTable()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['X Image', 'Y Image', 'X Plot', 'Y Plot'])
        # Установка режима изменения размера столбцов на Stretch
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.table)

        self.table.cellClicked.connect(self.on_cell_clicked)

        # Заменить плейсхолдеры на виджеты для вывода изображения
        replace_placeholder(self, self.origImCanvas, "origWidget")
        replace_placeholder(self, self.readyPlotCanvas, "plotWidget")
        replace_placeholder(buttons, self.magnifierImCanvas,
                            "magnifierWidget", fixed_size=True)

        # Связать колесико мыши с изменением масштаба лупы
        self.scale_slider.valueChanged.connect(
            lambda value: self.on_value_changed(value))

        self.selected_row = None

    def resizeEvent(self, event):
        """
        Обработать изменения размера окна - нужно пересчитать коэффициенты
        """
        # Проверка наличия изображения в канвасе
        if self.origImCanvas.img is not None:
            self.origImCanvas.count_koeffs()

    def on_value_changed(self, value):
        """
        Обработать изменения значения слайдера - изменить масштаб лупы
        """
        # Проверка наличия изображения в канвасе
        if self.origImCanvas.img is not None:
            self.origImCanvas.add_padding(value)
            # Пересчет коэффициентов
            self.origImCanvas.count_koeffs()
            self.magnifierImCanvas.update_magnifier_point()

            self.magnifierImCanvas.update_canvas()

    def load_plot_image(self):
        """
        Попросить пользователя выбрать изображение в проводнике.
        Загрузить это изображение и отобразить.
        """
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', path, "Image files (*.jpg *.png)")
        # Произошла Отмена - ничего не делать
        if fname[0] == '':
            return
        self.path_to_image = fname[0]
        # Отобразить изображение на канвасе
        self.origImCanvas.show_user_image(fname)
        # Обновить лупу
        self.magnifierImCanvas.update_magnifier_point()
        self.origImCanvas.mouseMoved(0, 0)
        # Новое изображение - старые точки не нужны
        self.table.clear_table()
        self.selected_row = None
        self.readyPlotCanvas.points = []

    # выбрана строка таблицы - подсветить точку
    def on_cell_clicked(self, row, column):
        """
        Обработать нажатие на ячейку таблицы.
        Заменить цвет выбранной точки на красный.
        Прежней точке вернуть синий.
        """
        if self.selected_row is not None:
            self.origImCanvas.points[self.selected_row].set_facecolor('blue')
        self.origImCanvas.points[row].set_facecolor('red')
        self.selected_row = row
        self.origImCanvas.update_canvas()

    def eventFilter(self, source, event):
        if (source is self.table and event.type() == QtCore.QEvent.KeyPress):
            row = self.table.currentRow()
            col = self.table.currentColumn()
            if event.key() == QtCore.Qt.Key_Up:
                if row - 1 >= 0:
                    self.on_cell_clicked(row - 1, None)
            elif event.key() == QtCore.Qt.Key_Down:
                if (row + 1) < len(self.origImCanvas.points):
                    self.on_cell_clicked(row + 1, None)
            if event.key() == QtCore.Qt.Key_Tab:
                if col == 3 and (row + 1) < len(self.origImCanvas.points):
                    self.on_cell_clicked(row + 1, None)
                if col == 0:
                    self.on_cell_clicked(row, None)
        return super().eventFilter(source, event)

    def save_points(self):
        """
        Спросить у пользователя путь и расширение выходного файла и записать в него точки.
        """
        # Проверка наличия изображения в канвасе
        if self.origImCanvas.img is None:
            widget = QWidget()
            QMessageBox.warning(
                widget,
                "Внимание",
                "Точки еще не посчитаны")
            return
        file_name, file_type = QFileDialog.getSaveFileName(
            self, 'Save File', '', 'CSV(*.csv);;Excel(*.xlsx);;TSV(*.tsv);;JSON(*.json);;XML(*.xml);;DAT(*.dat);;TXT(*.txt)')
        if file_name:
            df = self.readyPlotCanvas.points
            # Пробелы не поддерживаются в некоторых форматах
            df.columns = [col.replace(' ', '_') for col in df.columns]
            if 'CSV' in file_type:
                df.to_csv(file_name, index=False)
            elif 'Excel' in file_type:
                df.to_excel(file_name, index=False)
            elif 'TSV' in file_type:
                df.to_csv(file_name, index=False, sep='\t')
            elif 'TXT' in file_type:
                df.to_csv(file_name, index=False, sep='\t')
            elif 'DAT' in file_type:
                df.to_csv(file_name, index=False, sep=' ')
            elif 'JSON' in file_type:
                df.to_json(file_name)
            elif 'XML' in file_type:
                df.to_xml(file_name)

    def create_plot(self):
        """
        Посчитать точки нового графика и построить.
        """
        # Проверка наличия изображения в канвасе
        if self.origImCanvas.img is None:
            return
        # Скопировать таблицу с GUI в DataFrame
        df = self.table.save_to_df()

        # Запустить оцифровку
        returncode = start_digitizer(df, self.path_to_image)
        if returncode != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Ошибка {str(returncode)}")
            msg.setInformativeText("Оцифровка не удалась, пожалуйста, "
                                   "проверьте првильность ввода данных")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return
        points = np.load('points.npy')
        # Преобразовать в списки
        x, y = zip(*points)
        x, y = sort_lists(x, y)
        # Удалить старый график
        ax = self.readyPlotCanvas.figure.axes[0]
        for line in ax.lines:
            line.remove()
        self.readyPlotCanvas.draw_plot(x, y)
        self.readyPlotCanvas.points = pd.DataFrame({'X': x, 'Y': y})

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 650)

    window.show()
    app.installEventFilter(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
