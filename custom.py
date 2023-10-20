"""
custom made dialog box
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QGroupBox, QLabel, QTableWidget,
QTableWidgetItem, QAbstractItemView, QHeaderView, QPushButton, QHBoxLayout, QApplication
)
from PySide6.QtGui import QFont, Qt


# Define the font
FW_FONT = QFont("Monaco")
FW_FONT.setStyleHint(QFont.StyleHint.TypeWriter)
FW_FONT.setPointSize(14)
FW_FONT.setFixedPitch(True)


class BoxDialog(QDialog):
    """
    dialog box
    """
    def __init__(self, title, object_info,
     produced_by, classification, information):
        """
        Initialize the BoxDialog.
        Args:
            title (str): The title of the dialog.
            object_info (dict): The object information to display.
            produced_by (str): The producer information to display.
            classification (str): The classification information to display.
            information (list): The additional information to display.
        """

        super().__init__()

        header_font = QFont(FW_FONT)  # create a new font for the headings
        header_font.setPointSize(18)
        self.setWindowTitle(title)

        # Screen size to be no larger than 1/4 of the total screen area
        screen_size = QApplication.primaryScreen().size()
        width = screen_size.width()//1.5
        height = screen_size.height()//1.2
        self.setFixedSize(width, height)


        # Object Information section
        obj_group_box = QGroupBox("Object Information")
        obj_layout = QVBoxLayout()
        obj_group_box.setFont(header_font)

        obj_table = QTableWidget()
        obj_table.setColumnCount(4)

        obj_table.setHorizontalHeaderLabels(["Accession No.", "Label", "Date", "Place"])
        obj_table.setRowCount(1)
        obj_table.horizontalHeader().setFont(header_font)

        obj_table.setColumnWidth(0, 30)
        obj_table.setColumnWidth(1, 60)
        obj_table.setColumnWidth(1, 30)
        obj_table.setColumnWidth(1, 30)

        obj_table.setItem(0, 0, QTableWidgetItem(self.wrap_text(object_info["accession_no"], 30)))
        obj_table.setItem(0, 1, QTableWidgetItem(self.wrap_text(object_info["label"], 60)))
        obj_table.setItem(0, 2, QTableWidgetItem(self.wrap_text(object_info["date"], 30)))
        obj_table.setItem(0, 3, QTableWidgetItem(self.wrap_text(object_info["place"], 30)))


        # Resize the table to fit the contents
        obj_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        obj_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        obj_table.setFocusPolicy(Qt.NoFocus)  # remove focusability
        obj_table.resizeColumnsToContents()
        obj_table.setFont(FW_FONT)
        obj_table.setWordWrap(True)
        # Set the selection behavior and mode
        obj_table.setSelectionMode(QAbstractItemView.NoSelection)


        obj_table.setEditTriggers(QTableWidget.NoEditTriggers)

        obj_layout.addWidget(obj_table)
        obj_group_box.setLayout(obj_layout)

        # Produced By section
        produced_by_group_box = QGroupBox("Produced By")
        produced_by_layout = QVBoxLayout()
        produced_by_group_box.setFont(header_font)

        produced_by_table = QTableWidget()
        produced_by_table.setColumnCount(4)
        produced_by_table.setHorizontalHeaderLabels(["Part", "Name", "Nationalities", "Timespan"])
        produced_by_table.horizontalHeader().setFont(header_font)
        # Resize the table to fit the contents
        produced_by_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        produced_by_table.setColumnWidth(0, 30)
        produced_by_table.setColumnWidth(1, 60)
        produced_by_table.setColumnWidth(1, 30)
        produced_by_table.setColumnWidth(1, 30)
        for i, agent in enumerate(produced_by):
            produced_by_table.insertRow(i)

            produced_by_table.setItem(i, 0, QTableWidgetItem(self.wrap_text(agent['part'], 30)))
            produced_by_table.setItem(i, 1, QTableWidgetItem(self.wrap_text(agent['name'], 60)))
            produced_by_table.setItem(i, 2,
            QTableWidgetItem(self.wrap_text(agent['nationalities'], 30)))
            produced_by_table.setItem(i, 3, QTableWidgetItem(self.wrap_text(agent['timespan'], 30)))

        produced_by_table.resizeColumnsToContents()
        produced_by_table.setFont(FW_FONT)
        obj_table.setWordWrap(True)
        produced_by_table.setEditTriggers(QTableWidget.NoEditTriggers)
         # Set the selection behavior and mode
        produced_by_table.setSelectionMode(QAbstractItemView.NoSelection)


        produced_by_layout.addWidget(produced_by_table)
        produced_by_group_box.setLayout(produced_by_layout)

        # Classification section
        classification_group_box = QGroupBox("Classification")
        classification_layout = QVBoxLayout()
        classification_group_box.setFont(header_font)

        classification_label = QLabel(self.wrap_text(classification, 150))
        classification_label.setFont(FW_FONT)

        classification_layout.addWidget(classification_label)
        classification_group_box.setLayout(classification_layout)

        # Information section
        info_group_box = QGroupBox("Information")
        info_layout = QVBoxLayout()
        info_group_box.setFont(header_font)

        info_table = QTableWidget()
        info_h = screen_size.height() // 3
        info_table.setFixedHeight(info_h)
        info_table.setColumnCount(2)
        info_table.setFont(FW_FONT)

        info_table.setHorizontalHeaderLabels(["Type", "Content"])
        info_table.horizontalHeader().setFont(header_font)
        # Resize the table to fit the contents
        info_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Set minimum and maximum width of columns
        info_table.setColumnWidth(0, 30)
        info_table.setColumnWidth(1, 120)
        for i, reference in enumerate(information):
            info_table.insertRow(i)
            info_table.setItem(i, 0, QTableWidgetItem(self.wrap_text(reference['type'], 30)))
            line =self.wrap_text(reference['content'], 120)
            info_table.setItem(i, 1, QTableWidgetItem(line))

        info_table.setWordWrap(True)
        info_table.resizeColumnsToContents()
        info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        # Set the selection behavior and mode
        info_table.setSelectionMode(QAbstractItemView.NoSelection)
        # Set maximum width for each column

        info_layout.addWidget(info_table)
        info_group_box.setLayout(info_layout)

        # hide grid
        obj_table.setShowGrid(False)
        produced_by_table.setShowGrid(False)
        info_table.setShowGrid(False)
        obj_table.verticalHeader().setVisible(False)
        produced_by_table.verticalHeader().setVisible(False)
        info_table.verticalHeader().setVisible(False)
        # Remove click functionality from horizontal headers
        obj_table.horizontalHeader().setSectionsClickable(False)
        produced_by_table.horizontalHeader().setSectionsClickable(False)
        info_table.horizontalHeader().setSectionsClickable(False)

        # okay button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        # Dialog layout
        layout = QVBoxLayout()
        layout.addWidget(obj_group_box)
        layout.addWidget(produced_by_group_box)
        layout.addWidget(classification_group_box)
        layout.addWidget(info_group_box)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    def key_press_event(self, event):
        """handle events"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.accept()
    def wrap_text(self, text, max_width):
        """
        Wrap text to a maximum width using newlines.

        Args:
            text (str): The text to wrap.
            max_width (int): The maximum width of each line.

        Returns:
            str: The wrapped text.
        """
        if not text:
            return ""

        wrapped_text = ""
        words = text.split()
        lines = []
        line_length = 0
        for word in words:
            if line_length + len(word) < max_width:
                wrapped_text += word + " "
                line_length += len(word) + 1
            else:
                lines.append(wrapped_text)
                wrapped_text = word + " "
                line_length = len(word) + 1
        lines.append(wrapped_text)
        formated = "\n".join(lines)
        return formated
