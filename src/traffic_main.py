import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from gui.road_drawer import RoadDrawer
from ai.carDetector import CarDetector
from gui.quadrant_widget import QuadrantWidget

BTN_SIZE = 100

THUMB_SIZE = 200

BTN_POSITIONS = [
    (100, 50), (700, 50),
    (100, 600), (700, 600),
]

LABELS = ["Road #1", "Road #2", "Road #3", "Road #4"]

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

        self.road_drawer = RoadDrawer(self.scene, self.scene_width, self.scene_height, parent=self)
        self.road_drawer.draw_intersection()
        self.road_drawer.draw_lane_markings()
        self.road_drawer.add_road_labels(LABELS)

        self.car_detector = CarDetector()
        self.quadrants = [QuadrantWidget(self, LABELS[i], BTN_POSITIONS[i][0], BTN_POSITIONS[i][1], BTN_SIZE, THUMB_SIZE) for i in range(4)]

        self.add_center_button()


    def add_center_button(self):
        btn_width = 120
        btn_height = 40
        center_x = (self.scene_width - btn_width) // 2
        center_y = (self.scene_height - btn_height) // 2
        center_btn = QPushButton("감지 실행", self)
        center_btn.setGeometry(center_x, center_y, btn_width, btn_height)
        center_btn.raise_()
        center_btn.clicked.connect(self.run_detection)

    def run_detection(self):
        missing = [i+1 for i, q in enumerate(self.quadrants) if q.image_path is None]
        if missing:
            QMessageBox.warning(self, "이미지 누락", f"{', '.join(map(str, missing))}사분면 이미지가 선택되지 않았습니다.")
            return
        results = self.car_detector.run_detection(self.quadrants)
        for i, count in enumerate(results):
            self.quadrants[i].result_label.setText(f"차량 수 : {count}대")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoadWindow()
    window.show()
    sys.exit(app.exec_())