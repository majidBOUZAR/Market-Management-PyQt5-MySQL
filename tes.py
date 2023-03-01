import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QTextDocument, QTextTableFormat, QTextCursor, QFont,QTextLength
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QTextDocument, QTextTableFormat, QTextCursor, QFont
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Export TableWidget to PDF")
        self.setGeometry(100, 100, 600, 500)
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setRowCount(5)
        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f"({i}, {j})")
                self.table.setItem(i, j, item)
        self.exportBtn = QPushButton("Export to PDF", self)
        self.exportBtn.clicked.connect(self.exportTableWidget)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Table Example", self, alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("User: John Doe", self))
        layout.addWidget(QLabel("Total: $100", self))
        layout.addWidget(self.table)
        layout.addWidget(self.exportBtn, alignment=Qt.AlignCenter)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def exportTableWidget(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("table.pdf")
        document = QTextDocument()
        font = QFont()
        font.setPointSize(12)
        document.setDefaultFont(font)
        cursor = QTextCursor(document)
        
        # Insert Title
        titleFormat = QTextTableFormat()
        titleFormat.setAlignment(Qt.AlignHCenter)
        titleTable = cursor.insertTable(1, 1, titleFormat)
        titleCell = titleTable.cellAt(0, 0)
        cursor = titleCell.firstCursorPosition()
        cursor.insertText("Table Example")
        cursor.insertBlock()
        
        # Insert User
        userLabel = self.centralWidget().findChild(QLabel, "User: John Doe")
        if userLabel is not None:
            cursor.insertText("User: ")
            cursor.insertText(userLabel.text())
            cursor.insertBlock()
        
        # Insert Total Price
        totalLabel = self.centralWidget().findChild(QLabel, "Total: $100")
        if totalLabel is not None:
            cursor.insertText("Total: ")
            cursor.insertText(totalLabel.text())
            cursor.insertBlock()
        
        # Insert Table
        tableFormat = QTextTableFormat()
        tableFormat.setAlignment(Qt.AlignHCenter)
        tableFormat.setWidth(1500)
        table = cursor.insertTable(self.table.rowCount() + 1, self.table.columnCount(), tableFormat)
        
        # Set Headers
        headers = ["Column 1", "Column 2", "Column 3"]
        for col in range(self.table.columnCount()):
            tableCell = table.cellAt(0, col)
            cursor = tableCell.firstCursorPosition()
            cursor.insertText(headers[col])
            cursor.insertBlock()
        
        # Set Items
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    tableCell = table.cellAt(row + 1, col)
                    cursor = tableCell.firstCursorPosition()
                    cursor.insertText(item.text())
                    cursor.insertBlock()
        document.print_(printer)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
