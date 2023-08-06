import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class DataFrameTable(QTableWidget):
    """
    A QTableWidget that can be used to display and edit data in a DataFrame.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def edit_lock(self, colum_count):
        """
        Prevents editing of the first `colum_count` columns.

        Args:
            colum_count (int): The number of columns to lock.
        """
        # Prevent editing of the first `colum_count` columns
        for row in range(self.rowCount()):
            for col in range(colum_count):
                item = self.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def save_to_df(self):
        """
        Saves the data in the table to a DataFrame.

        Returns:
            DataFrame: The DataFrame containing the data from the table.
        """
        # Get table dimensions
        rows = self.rowCount()
        cols = self.columnCount()

        # Create an empty list to store data
        data = []

        # Extract data from table
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)

        # Create a DataFrame with data from the table
        df = pd.DataFrame(data, columns=[self.horizontalHeaderItem(
            col).text() for col in range(cols)])
        return df

    def add_row(self, x, y):
        """
        Adds a row to the table.

        Args:
            x (int): The value to be added to the first column of the new row.
            y (int): The value to be added to the second column of the new row.
        """
        # Add a row to the table
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(str(x)))
        self.setItem(row_position, 1, QTableWidgetItem(str(y)))
        self.setItem(row_position, 2, QTableWidgetItem("0"))
        self.setItem(row_position, 3, QTableWidgetItem("0"))
        # Prevent editing of the first two columns
        self.edit_lock(2)

    def remove_row(self, index):
        """
        Removes a row from the table.

        Args:
            index (int): The index of the row to be removed.
        """
        # Remove a row by index
        self.removeRow(index)

    def clear_table(self):
        """
        Removes all rows from the table.
        """
        # Remove all rows from the table
        while self.rowCount() > 0:
            self.removeRow(0)
