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

path = os.path.abspath(os.path.dirname(__file__))


def start_digitizer(df, path_to_image):
    """
    Starts the digitization process.

    Args:
        df (pandas.DataFrame): A DataFrame containing the locations and points to be digitized.
        path_to_image (str): The path to the image to be digitized.

    Returns:
        int: The return code of the subprocess call.
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
        # Error handling
        print(f"Error when running command: return code {returncode}")

    return returncode


def replace_placeholder(
        parent,
        widget_new,
        placeholder_name,
        fixed_size=False):
    """
    Replaces a placeholder widget with a new widget in the window.

    Args:
        parent (QWidget): The widget in which the replacement is performed.
        widget_new (QWidget): The new widget for replacement.
        placeholder_name (str): The name of the placeholder widget to be replaced.
        fixed_size (bool): Flag to set a fixed size for the new widget.

    Returns:
        None
    """
    # Find the old widget by name
    widget_old = parent.findChild(QWidget, placeholder_name)
    # Get the parent layout for the old widget
    containingLayout = widget_old.parent().layout()
    # Replace the old widget with the new one in the layout
    containingLayout.replaceWidget(widget_old, widget_new)

    # Save sizes
    # Save minimum size for new widget
    widget_new.setMinimumSize(widget_old.minimumSize())

    # Set fixed size for new widget
    if fixed_size:
        widget_new.setFixedSize(widget_old.size())


def sort_lists(x, y):
    """
    Sorts two lists (x and y) in ascending order of values in the x list.

    Args:
        x (list): The list of values to be sorted.
        y (list): The list of values corresponding to the values in the x list.

    Returns:
        tuple: A tuple of two sorted lists (x_sorted, y_sorted).
    """
    # Create a list of pairs (x, y)
    xy_pairs = list(zip(x, y))
    # Sort the list of pairs by the value of x
    xy_pairs.sort(key=lambda pair: pair[0])
    # Split the sorted pairs back into two lists
    x_sorted, y_sorted = zip(*xy_pairs)
    return list(x_sorted), list(y_sorted)


class ButtonsWidget(QWidget):
    """
    Виджет кнопок, в нём находятся: текстовая подсказка, magnifier, slider, buttons
    """

    def __init__(self):
        QWidget.__init__(self)
        # Загрузка дизайна виджета из файла
        uic.loadUi(os.path.join(path, "ui", "buttons.ui"), self)


class GraphPreviewer(QWidget):
    """
    Chart view widget containing 2 windows: the left one shows the original image,
    the right one shows the graph plotted from points.
    """

    def __init__(self):
        QWidget.__init__(self)
        # Load the widget design from a file
        uic.loadUi(os.path.join(path, "ui", "plots.ui"), self)


class MainWindow(QMainWindow):
    """
    The main window of the application.
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Plot Scanner")
        # Horizontal layout: buttons and table on the left, graphs on the right
        hbox = QHBoxLayout()
        # Freeze the left layout with buttons so it doesn't stretch
        hbox.setStretch(1, 2)
        # Vertical layout: buttons on top, points table at the bottom
        vbox = QVBoxLayout()
        hbox.addLayout(vbox)

        buttons = ButtonsWidget()
        graph = GraphPreviewer()
        vbox.addWidget(buttons)
        hbox.addWidget(graph)

        # Central widget for the main window
        cw = QWidget()
        cw.setLayout(hbox)
        self.setCentralWidget(cw)

        # Find buttons created in designer
        self.button_load = buttons.findChild(QPushButton, "loadButton")
        self.button_create = buttons.findChild(QPushButton, "createButton")
        self.button_save = buttons.findChild(QPushButton, "saveButton")
        # Find magnifier scale slider
        self.scale_slider = buttons.findChild(QSlider, "scaleSlider")

        # Click handlers
        self.button_load.clicked.connect(self.load_plot_image)
        self.button_save.clicked.connect(self.save_points)
        self.button_create.clicked.connect(self.create_plot)

        # Canvases for displaying images directly in the application window
        self.origImCanvas = ImageCanvas(self)
        self.readyPlotCanvas = PlotCanvas()
        self.magnifierImCanvas = Magnifier(self)

        # Create a table with 4 columns
        self.table = DataFrameTable()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['X Image', 'Y Image', 'X Plot', 'Y Plot'])
        # Set column resize mode to Stretch
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.table)

        self.table.cellClicked.connect(self.on_cell_clicked)

        # Replace placeholders with image output widgets
        replace_placeholder(self, self.origImCanvas, "origWidget")
        replace_placeholder(self, self.readyPlotCanvas, "plotWidget")
        replace_placeholder(buttons, self.magnifierImCanvas,
                            "magnifierWidget", fixed_size=True)

        # Connect mouse wheel to magnifier scale change
        self.scale_slider.valueChanged.connect(
            lambda value: self.on_value_changed(value))

        self.selected_row = None

    def resizeEvent(self, event):
        """
        Handles window size changes (need to recalculate coefficients).
        """
        # Check for image presence in canvas
        if self.origImCanvas.img is not None:
            self.origImCanvas.count_koeffs()

    def on_value_changed(self, value):
        """
        Handles changes in slider value (change magnifier scale).
        """
        # Check for image presence in canvas
        if self.origImCanvas.img is not None:
            self.origImCanvas.add_padding(value)
            # Recalculate coefficients
            self.origImCanvas.count_koeffs()
            self.magnifierImCanvas.update_magnifier_point()

            self.magnifierImCanvas.update_canvas()

    def load_plot_image(self):
        """
        Prompts the user to select an image in the file explorer.
        Loads and displays the selected image.
        """
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', path, "Image files (*.jpg *.png)")
        # Cancelled - do nothing
        if fname[0] == '':
            return
        self.path_to_image = fname[0]
        # Display image on canvas
        self.origImCanvas.show_user_image(fname)
        # Update magnifier
        self.magnifierImCanvas.update_magnifier_point()
        self.origImCanvas.mouseMoved(0, 0)
        # New image - old points not needed
        self.table.clear_table()
        self.selected_row = None
        self.readyPlotCanvas.points = []

    # Table row selected - highlight point
    def on_cell_clicked(self, row, column):
        """
        Handles clicking on a table cell.
        Changes the color of the selected point to red.
        Changes the previous point back to blue.
        """
        if self.selected_row is not None:
            self.origImCanvas.points[self.selected_row].set_facecolor('blue')
        self.origImCanvas.points[row].set_facecolor('red')
        self.selected_row = row
        self.origImCanvas.update_canvas()

    def eventFilter(self, source, event):
        """
        Filters events to handle key presses on the table.

        Args:
            source (QObject): The object that generated the event.
            event (QEvent): The event to be filtered.

        Returns:
            bool: Whether the event was handled.
        """
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
        Prompts the user for the path and extension of the output file and writes the points to it.
        """
        # Check for image presence in canvas
        if self.origImCanvas.img is None:
            widget = QWidget()
            QMessageBox.warning(
                widget,
                "Attention",
                "Points have not been calculated yet")
            return
        file_name, file_type = QFileDialog.getSaveFileName(
            self,
            'Save File',
            '',
            'CSV(*.csv);;Excel(*.xlsx);;TSV(*.tsv);;JSON(*.json);;XML(*.xml);;DAT(*.dat);;TXT(*.txt)'
        )
        if file_name:
            df = self.readyPlotCanvas.points
            # Spaces are not supported in some formats
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
        Calculates the points of the new graph and plots it.
        """
        # Check for image presence in canvas
        if self.origImCanvas.img is None:
            return
        # Copy table from GUI to DataFrame
        df = self.table.save_to_df()

        # Start digitization
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
        # Convert to lists
        x, y = zip(*points)
        x, y = sort_lists(x, y)
        # Remove old plot
        ax = self.readyPlotCanvas.figure.axes[0]
        for line in ax.lines:
            line.remove()
        self.readyPlotCanvas.draw_plot(x, y)
        self.readyPlotCanvas.points = pd.DataFrame({'X': x, 'Y': y})


def main():
    """
    The main function that starts the application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 650)

    window.show()
    app.installEventFilter(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
