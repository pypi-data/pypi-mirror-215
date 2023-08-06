from math import ceil

import cv2
import matplotlib
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5.QtGui import QMouseEvent


class MplCanvas(FigureCanvasQTAgg):
    """
    Matplotlib Qt Embedding
    """

    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(1, 1, 1)

    def update_canvas(self):
        """
        Updates the canvas by redrawing it.
        """
        self.fig.canvas.draw()


class Magnifier(MplCanvas):
    """
    Magnifier for user image
    """

    def __init__(self, parent):
        super().__init__()
        # Remove margins and axes
        self.axes.axis("off")
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

        self.parent = parent

        # Point in the center of the magnifier
        self.circle = self.draw_magnifier_point((10, 10), 3)

    def draw_magnifier_point(self, point, radius):
        """
        Draws a point in the center of the magnifier.

        Args:
            point (tuple): The coordinates of the point to be drawn.
            radius (int): The radius of the point to be drawn.

        Returns:
            Circle: The circle object representing the point.
        """
        x, y = point
        circle = matplotlib.patches.Circle(
            (x, y), radius, facecolor='red', edgecolor='red')
        self.axes.add_patch(circle)
        return circle

    def update_magnifier_point(self):
        """
        Redraws the point in the center of the magnifier (erases the old one).
        """
        # Get value from slider
        padding = self.parent.scale_slider.value()

        self.circle.remove()
        self.circle = self.draw_magnifier_point(
            (padding, padding), ceil(padding / 32))


class PlotCanvas(MplCanvas):
    """
    The digitized plot.
    """

    def __init__(self):
        super().__init__()
        self.img = None
        self.orig = None

    def draw_plot(self, x, y):
        """
        Draws a plot with the given x and y values.

        Args:
            x (list): The x values of the plot.
            y (list): The y values of the plot.
        """
        self.axes.plot(x, y)
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.update_canvas()


class ImageCanvas(MplCanvas):
    """
    The user's image.
    """

    def __init__(self, parent):
        super().__init__()
        self.img = None
        self.orig = None
        # Reduce margins and disable axes
        self.axes.axis("off")
        # Remove image margins
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.parent = parent
        # Get value from slider
        self.padding = parent.scale_slider.value()  # on each side
        self.setMouseTracking(True)
        self.points = []
        self.mpl_connect('button_press_event', self.on_click)

        # Coefficients
        self.k_image = 1
        self.k_canvas = 1
        self.image_over_canvas = 1
        self.pad = 10

    def show_user_image(self, path):
        """
        Opens the image at the specified path.

        Args:
            path (str): The path to the image to be opened.
        """
        # Check path validity
        if path[0] == '':
            return
        # Clear points
        for i in range(len(self.points)):
            self.remove_point(0)
        # Original image
        self.orig = cv2.imread(path[0])
        self.orig = self.orig[..., ::-1]
        # Image to be shown to user
        self.img = np.array(self.orig, copy=True)
        # Get value from slider
        self.padding = self.parent.scale_slider.value()
        # Add padding for magnifier
        self.add_padding(self.padding)
        self.axes.imshow(self.orig, cmap='gray')
        self.update_canvas()
        self.count_koeffs()

    def add_padding(self, padding):
        """
        Adds white pixels around the perimeter of the image.

        Args:
            padding (int): The number of pixels to add on each side of the image.
        """
        self.padding = padding
        # Padding
        old_image_height, old_image_width, channels = self.orig.shape
        # Create new image of desired size and color (white) for padding
        new_image_width = old_image_width + padding * 2
        new_image_height = old_image_height + padding * 2
        color = (255, 255, 255)  # white
        result = np.full((new_image_height, new_image_width,
                          channels), color, dtype=np.uint8)

        # Compute center offset
        x_center = (new_image_width - old_image_width) // 2
        y_center = (new_image_height - old_image_height) // 2

        # Copy original image into center of result image
        result[y_center:y_center + old_image_height,
               x_center:x_center + old_image_width] = self.orig

        self.img = result

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        """
        Handles mouse movement events.

        Args:
            a0 (QMouseEvent): The mouse event to be handled.
        """
        x = a0.pos().x()
        y = a0.pos().y()
        self.mouseMoved(x, y)
        return super().mouseMoveEvent(a0)

    def remove_point(self, index):
        """
        Removes a point.

        Args:
            index (int): The index of the point to be removed.
        """
        circle = self.points.pop(index)
        self.parent.table.remove_row(index)
        circle.remove()
        self.update_canvas()

    def add_point(self, x, y, radius):
        """
        Adds a point.

        Args:
            x (int): The x coordinate of the point to be added.
            y (int): The y coordinate of the point to be added.
            radius (int): The radius of the point to be added.
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
        Handles left mouse button clicks - adds or removes a point.

        Args:
            event (MouseEvent): The mouse event to be handled.
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
        Handles mouse wheel events.

        Args:
            event (WheelEvent): The wheel event to be handled.
        """
        if event.angleDelta().y() > 0:
            # Wheel is scrolling up
            value = self.parent.scale_slider.value() - self.parent.scale_slider.singleStep()
            if value >= self.parent.scale_slider.minimum():
                self.parent.scale_slider.setValue(value)
        else:
            # Wheel is scrolling down
            value = self.parent.scale_slider.value() + self.parent.scale_slider.singleStep()
            if value <= self.parent.scale_slider.maximum():
                self.parent.scale_slider.setValue(value)
        # For smoothness
        cursor_pos = event.pos()
        self.mouseMoved(cursor_pos.x(), cursor_pos.y())

    def count_koeffs(self):
        """
        Calculates the aspect ratio and scale coefficients for the image and canvas.
        The coefficients only change under certain conditions, so it's better to calculate them once.
        These coefficients are needed for the magnifier.
        """
        # Get original image from canvas
        orig = self.orig
        # Check for image presence in canvas
        if orig is None:
            return

        # Get image dimensions
        h_image, w_image, _ = orig.shape
        # Get canvas dimensions
        w_canvas, h_canvas = self.size().width(), self.size().height()

        # Calculate aspect ratio coefficients for image and canvas (w:h)
        self.k_image = w_image / h_image
        self.k_canvas = w_canvas / h_canvas

        # Convert canvas coordinates to image coordinates with padding
        # Here, padding is the area of the canvas not occupied by the image
        if self.k_canvas > self.k_image:  # Vertical image - padding on sides
            # Calculate scale coefficient image / canvas
            self.image_over_canvas = h_image / h_canvas
            self.pad = round((w_canvas - h_canvas * self.k_image) / 2)
        else:  # Horizontal image - padding on top and bottom
            self.image_over_canvas = w_image / w_canvas
            self.pad = round((h_canvas - w_canvas / self.k_image) / 2)

    def mouseMoved(self, x, y):
        """
        Handles mouse movement within the canvas (redraws the magnification).

        Args:
            x (int): The x coordinate of the mouse cursor.
            y (int): The y coordinate of the mouse cursor.
        """
        # Get image (with padding) from canvas
        # Here padding is additional white pixels around the perimeter,
        # so that it is possible to crop the edges of the image for the magnifier
        img = self.img
        # Check for image presence in canvas
        if img is None:
            return
        padding = self.padding
        # Get image dimensions (with padding)
        h_image, w_image, _ = img.shape

        # Convert canvas coordinates to image coordinates with padding
        if self.k_canvas > self.k_image:  # Vertical image - padding on sides
            x_image = round((x - self.pad) * self.image_over_canvas)
            y_image = round((y) * self.image_over_canvas)
        else:  # Horizontal image - padding on top and bottom
            x_image = round((x) * self.image_over_canvas)
            y_image = round((y - self.pad) * self.image_over_canvas)

        # Transition from padded image to unpadded image
        # Recalculate coordinates
        y_image += padding
        x_image += padding
        # Handle edge values
        y_image = max(padding, min(y_image, h_image - padding - 1))
        x_image = max(padding, min(x_image, w_image - padding - 1))

        # Crop padded image
        img = img[y_image - padding:y_image + padding,
                  x_image - padding:x_image + padding, :]

        self.parent.magnifierImCanvas.axes.imshow(img, cmap='gray')
        self.parent.magnifierImCanvas.update_canvas()
