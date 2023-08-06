from math import ceil

import cv2
import matplotlib
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5.QtGui import QMouseEvent


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(1, 1, 1)

    def update_canvas(self):
        self.fig.canvas.draw()

# Лупа


class Magnifier(MplCanvas):
    def __init__(self, parent):
        super().__init__()
        # Убрать отступы и оси
        self.axes.axis("off")
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

        self.parent = parent

        # Точка по центру лупы
        self.circle = self.draw_magnifier_point((10, 10), 3)

    def draw_magnifier_point(self, point, radius):
        """
        Нарисовать точку в центре лупы
        """
        x, y = point
        circle = matplotlib.patches.Circle(
            (x, y), radius, facecolor='red', edgecolor='red')
        self.axes.add_patch(circle)
        return circle

    def update_magnifier_point(self):
        """
        Перерисовать точку в центре лупы (старую стереть)
        """
        # Взять значение со слайдера
        padding = self.parent.scale_slider.value()

        self.circle.remove()
        self.circle = self.draw_magnifier_point(
            (padding, padding), ceil(padding / 32))

# Оцифрованный график


class PlotCanvas(MplCanvas):
    def __init__(self):
        super().__init__()
        self.img = None
        self.orig = None

    def draw_plot(self, x, y):
        self.axes.plot(x, y)
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.update_canvas()

# Оригинальное изображение


class ImageCanvas(MplCanvas):
    def __init__(self, parent):
        super().__init__()
        self.img = None
        self.orig = None
        # уменьшшить отступы и отключить оси
        self.axes.axis("off")
        # убрать отступы у изображения
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.parent = parent
        # Взять значение со слайдера
        self.padding = parent.scale_slider.value()  # с каждой стороны
        self.setMouseTracking(True)
        self.points = []
        self.mpl_connect('button_press_event', self.on_click)

        # Коэффициенты
        self.k_image = 1
        self.k_canvas = 1
        self.image_over_canvas = 1
        self.pad = 10

    def show_user_image(self, path):
        """
        Открыть изображение по указанному пути.
        """
        # Проверка корректности пути
        if path[0] == '':
            return
        # очистка точек
        for i in range(len(self.points)):
            self.remove_point(0)
        # оригинальное изображение
        self.orig = cv2.imread(path[0])
        self.orig = self.orig[..., ::-1]
        # изображение, которое будет показано пользователю
        self.img = np.array(self.orig, copy=True)
        # взять значение со слайдера
        self.padding = self.parent.scale_slider.value()
        # добавить паддинг для лупы
        self.add_padding(self.padding)
        self.axes.imshow(self.orig, cmap='gray')
        self.update_canvas()
        self.count_koeffs()

    def add_padding(self, padding):
        """
        Добавить к изображению белые пиксели по периметру
        """
        self.padding = padding
        # padding
        old_image_height, old_image_width, channels = self.orig.shape
        # create new image of desired size and color (blue) for padding
        new_image_width = old_image_width + padding * 2
        new_image_height = old_image_height + padding * 2
        color = (255, 255, 255)  # белый
        result = np.full((new_image_height, new_image_width,
                         channels), color, dtype=np.uint8)

        # compute center offset
        x_center = (new_image_width - old_image_width) // 2
        y_center = (new_image_height - old_image_height) // 2

        # copy orig image into center of result image
        result[y_center:y_center + old_image_height,
               x_center:x_center + old_image_width] = self.orig

        self.img = result

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        """
        Событие движения мышью
        """
        x = a0.pos().x()
        y = a0.pos().y()
        self.mouseMoved(x, y)
        return super().mouseMoveEvent(a0)

    def remove_point(self, index):
        """
        Удалить точку
        """
        circle = self.points.pop(index)
        self.parent.table.remove_row(index)
        circle.remove()
        self.update_canvas()

    def add_point(self, x, y, radius):
        """
        Добавить точку
        """
        if len(self.points) >= 3:
            return
        h, _, _ = self.orig.shape
        self.parent.table.add_row(int(x), int(h - y))
        circle = matplotlib.patches.Circle(
            (x, y), radius, facecolor='blue', edgecolor='blue')
        self.axes.add_patch(circle)
        self.points.append(circle)
        self.update_canvas()

    def on_click(self, event):
        """
        Обработать нажатие ЛКМ - поставить или убрать точку
        """
        if self.img is not None:
            for i, circle in enumerate(self.points):
                if circle.contains(event)[0]:
                    self.parent.selected_row = None
                    self.remove_point(i)
                    return
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                radius = 7
                self.add_point(x, y, radius)

    def wheelEvent(self, event):
        """
        Обработать колесико мыши
        """
        if event.angleDelta().y() > 0:
            # Колесико крутится вверх
            value = self.parent.scale_slider.value() - self.parent.scale_slider.singleStep()
            if value >= self.parent.scale_slider.minimum():
                self.parent.scale_slider.setValue(value)
        else:
            # Колесико крутится вниз
            value = self.parent.scale_slider.value() + self.parent.scale_slider.singleStep()
            if value <= self.parent.scale_slider.maximum():
                self.parent.scale_slider.setValue(value)
        # Для плавности
        cursor_pos = event.pos()
        self.mouseMoved(cursor_pos.x(), cursor_pos.y())

    def count_koeffs(self):
        """
        Вычислить коэффициенты соотношения сторон и масштаба для изображения и канваса.
        Коэффициенты меняются только при определенных условиях, поэтому лучше один раз посчитать.
        Эти коэффициенты нужны лупе.
        """
        # Получение оригинального изображения из канваса
        orig = self.orig
        # Проверка наличия изображения в канвасе
        if orig is None:
            return

        # Получение размеров изображения
        h_image, w_image, _ = orig.shape
        # Получение размеров канваса
        w_canvas, h_canvas = self.size().width(
        ), self.size().height()

        # Вычисление коэффициентов соотношения сторон для изображения и канваса
        # (w:h)
        self.k_image = w_image / h_image
        self.k_canvas = w_canvas / h_canvas

        # Преобразование координат канваса в координаты изображения с учетом паддинга
        # Здесь, паддинг - область канваса, не занятая изображением
        if self.k_canvas > self.k_image:  # картинка вертикальная - паддинг по бокам
            # Вычисление коэффициента масштаба image / canvas
            self.image_over_canvas = h_image / h_canvas
            self.pad = round((w_canvas - h_canvas * self.k_image) / 2)

        else:  # картинка горизонтальная - паддинг сверху и снизу
            self.image_over_canvas = w_image / w_canvas
            self.pad = round((h_canvas - w_canvas / self.k_image) / 2)

    def mouseMoved(self, x, y):
        """
        Обработать движение мыши внутри канваса - перереисовать увеличение.
        """
        # Получение изображения (с паддингом) из канваса.
        # Здесь паддинг - дополнительные белые пиксели по периметру,
        # чтобы можно было сделать crop краев изображения для лупы.
        img = self.img
        # Проверка наличия изображения в канвасе
        if img is None:
            return
        padding = self.padding
        # Получение размеров изображения (с паддингом)
        h_image, w_image, _ = img.shape

        # Преобразование координат canvas в координаты изображения с учетом
        # паддинга
        if self.k_canvas > self.k_image:  # картинка вертикальная - паддинг по бокам
            x_image = round((x - self.pad) *
                            self.image_over_canvas)
            y_image = round((y) * self.image_over_canvas)
        else:  # картинка горизонтальная - паддинг сверху и снизу
            x_image = round((x) * self.image_over_canvas)
            y_image = round((y - self.pad) *
                            self.image_over_canvas)

        # Переход от изображения с паддингом к изображению без него.
        # Пересчитать координаты
        y_image += padding
        x_image += padding
        # Обработка крайних значений
        y_image = max(padding, min(y_image, h_image - padding - 1))
        x_image = max(padding, min(x_image, w_image - padding - 1))

        # Crop изображения с паддингом
        img = img[y_image - padding:y_image + padding,
                  x_image - padding:x_image + padding, :]

        self.parent.magnifierImCanvas.axes.imshow(img, cmap='gray')

        self.parent.magnifierImCanvas.update_canvas()
        