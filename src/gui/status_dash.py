from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

LABELS = ["Road #1", "Road #2", "Road #3", "Road #4"]

class StatusTableManager:
    def __init__(self, parent):
        self.table = QTableWidget(parent)
        self.table.setRowCount(2)
        self.table.setColumnCount(4)

        table_width = 370
        self.table.setGeometry(920, 365, table_width, 152)

        self.table.setHorizontalHeaderLabels(LABELS)
        self.table.setVerticalHeaderLabels(["현재 차량", "할당 시간"])
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Increase font size for header text
        header_font = self.table.font()
        header_font.setPointSize(16)
        self.table.horizontalHeader().setFont(header_font)
        self.table.verticalHeader().setFont(header_font)

        for col in range(4):
            item_current = QTableWidgetItem("0")
            item_current.setTextAlignment(Qt.AlignCenter)
            # Set larger font size for better readability
            font = item_current.font()
            font.setPointSize(20)
            item_current.setFont(font)
            self.table.setItem(0, col, item_current)

            item_time = QTableWidgetItem("0.0s")
            item_time.setTextAlignment(Qt.AlignCenter)
            item_time.setFont(font)
            self.table.setItem(1, col, item_time)

        # 셀 사이즈 설정
        self.table.setRowHeight(0, 60)
        self.table.setRowHeight(1, 60)

        # 헤더 자동 채우기
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setShowGrid(True)
        self.table.setStyleSheet("""
            QTableWidget::item {
                border: 1px solid white;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid white;
            }
        """)

    def update_status_table(self, vehicle_counts, green_durations):
        from PyQt5 import QtGui
        nonzero_counts = [count for count in vehicle_counts if count > 0]
        max_count = max(nonzero_counts) if nonzero_counts else 0
        min_count = min(nonzero_counts) if nonzero_counts else 0

        for i in range(4):
            vehicle_text = f"{vehicle_counts[i]}"
            green_text = f"{green_durations[i] / 100:.1f}s"

            item_current = self.table.item(0, i)
            item_time = self.table.item(1, i)

            item_current.setText(vehicle_text)
            item_time.setText(green_text)

            if vehicle_counts[i] == max_count and vehicle_counts[i] > 0:
                item_current.setForeground(QtGui.QColor("red"))
                item_time.setForeground(QtGui.QColor("red"))
            elif vehicle_counts[i] == min_count and vehicle_counts[i] > 0:
                item_current.setForeground(QtGui.QColor("green"))
                item_time.setForeground(QtGui.QColor("green"))
            else:
                item_current.setForeground(QtGui.QBrush())  # default color
                item_time.setForeground(QtGui.QBrush())