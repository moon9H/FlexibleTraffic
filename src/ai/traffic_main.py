import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from road_drawer import RoadDrawer
from carDetector import CarDetector

class RoadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4차선 교통 시뮬레이션")
        self.setGeometry(100, 100, 900, 900)
        self.scene_width = 900
        self.scene_height = 900

        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.road_drawer = RoadDrawer(self.scene, self.scene_width, self.scene_height)
        self.road_drawer.draw_intersection()
        self.road_drawer.draw_lane_markings()

        self.car_detector = CarDetector()
        self.image_paths = [None] * 4
        self.result_labels = [None] * 4

        self.add_quadrant_buttons()
        self.add_center_button()

    def add_quadrant_buttons(self):
        btn_size = 100
        thumb_size = 200
        positions = [
            (100, 50), (self.scene_width - 200, 50),
            (100, self.scene_height - 300), (self.scene_width - 200, self.scene_height - 300),
        ]
        labels = ["1사분면", "2사분면", "3사분면", "4사분면"]
        self.thumbnails = [None] * 4

        for i, (x, y) in enumerate(positions):
            btn = QPushButton(labels[i], self)
            btn.setGeometry(x, y, btn_size, 40)
            btn.raise_()
            btn.clicked.connect(lambda checked, idx=i: self.load_image(idx, x, y + 40 + (thumb_size // 2)))
            thumb_x = x + (btn_size - thumb_size) // 2
            thumb_y = y + 40
            thumb = QLabel(self)
            thumb.setGeometry(thumb_x, thumb_y, thumb_size, thumb_size)
            thumb.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
            thumb.setAlignment(Qt.AlignCenter)
            self.thumbnails[i] = thumb
            result_label = QLabel("", self)
            result_label.setGeometry(thumb_x, thumb_y + thumb_size + 5, thumb_size, 30)
            result_label.setAlignment(Qt.AlignCenter)
            self.result_labels[i] = result_label

    def add_center_button(self):
        btn_width = 120
        btn_height = 40
        center_x = (self.scene_width - btn_width) // 2
        center_y = (self.scene_height - btn_height) // 2
        center_btn = QPushButton("감지 실행", self)
        center_btn.setGeometry(center_x, center_y, btn_width, btn_height)
        center_btn.raise_()
        center_btn.clicked.connect(self.run_detection)

    def load_image(self, idx, x, y):
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.thumbnails[idx].setPixmap(pixmap)
            self.thumbnails[idx].setToolTip(file_path)
            self.image_paths[idx] = file_path
            self.result_labels[idx].setText("")

    def run_detection(self):
        for i, path in enumerate(self.image_paths):
            if path is None:
                QMessageBox.warning(self, "이미지 누락", f"{i+1}사분면 이미지가 선택되지 않았습니다.")
                return
        for i, path in enumerate(self.image_paths):
            count = self.car_detector.detect_cars(path)
            self.result_labels[i].setText(f"차량 수 : {count}대")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoadWindow()
    window.show()
    sys.exit(app.exec_())