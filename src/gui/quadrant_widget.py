from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class QuadrantWidget:
    def __init__(self, parent, label, x, y, btn_size=100, thumb_size=200):
        self.parent = parent
        self.btn_size = btn_size
        self.thumb_size = thumb_size
        self.x = x
        self.y = y
        self.image_path = None

        self.button = QPushButton(label, parent)
        self.button.setGeometry(x, y, btn_size, 40)
        self.button.raise_()
        self.button.clicked.connect(self.load_image)

        thumb_x = x + (btn_size - thumb_size) // 2
        thumb_y = y + 40
        self.thumbnail = QLabel(parent)
        self.thumbnail.setGeometry(thumb_x, thumb_y, thumb_size, thumb_size)
        self.thumbnail.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.thumbnail.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("", parent)
        self.result_label.setGeometry(thumb_x, thumb_y + thumb_size + 5, thumb_size, 30)
        self.result_label.setAlignment(Qt.AlignCenter)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "이미지 선택", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path).scaled(self.thumb_size, self.thumb_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.thumbnail.setPixmap(pixmap)
            self.thumbnail.setToolTip(file_path)
            self.image_path = file_path
            self.result_label.setText("")