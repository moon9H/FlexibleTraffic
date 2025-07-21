import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import Qt, QTimer
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

        self.green_durations = [2700, 4500, 3100, 1700]  # 북, 동, 남, 서 초록불 시간 (ms)

        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.road_drawer = RoadDrawer(self.scene, self.scene_width, self.scene_height, parent=self)
        self.road_drawer.draw_intersection()
        self.road_drawer.draw_lane_markings()
        self.road_drawer.add_road_labels(LABELS)

        self.car_detector = CarDetector()
        self.quadrants = [QuadrantWidget(self, LABELS[i], BTN_POSITIONS[i][0], BTN_POSITIONS[i][1], BTN_SIZE, THUMB_SIZE) for i in range(4)]
        self.results = []

        self.elapsed_time = 0  # 경과 시간 (초)
        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)

        self.timer_label = QLabel("시뮬레이션 시간: 0초", self)
        self.timer_label.setGeometry((self.scene_width - 200) // 2, (self.scene_height - 40) // 2 + 70, 200, 30)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.timer_label.hide()

        self.add_detection_center_button()
        self.add_simulation_center_button()

        # 🔹 신호등 순환 관련 변수
        self.current_signal_index = -1
        self.signal_timer = QTimer()
        self.signal_timer.timeout.connect(self.update_signal)

    def add_detection_center_button(self):
        btn_width = 120
        btn_height = 40
        center_x = (self.scene_width - btn_width) // 2
        center_y = (self.scene_height - btn_height) // 2 - 20
        center_btn = QPushButton("감지 실행", self)
        center_btn.setGeometry(center_x, center_y, btn_width, btn_height)
        center_btn.raise_()
        center_btn.clicked.connect(self.run_detection)

    def add_simulation_center_button(self):
        btn_width = 120
        btn_height = 40
        center_x = (self.scene_width - btn_width) // 2
        center_y = (self.scene_height - btn_height) // 2 + 20
        center_btn = QPushButton("시뮬레이션 실행", self)
        center_btn.setGeometry(center_x, center_y, btn_width, btn_height)
        center_btn.raise_()
        center_btn.clicked.connect(self.call_animator)

    def run_detection(self):
        missing = [i+1 for i, q in enumerate(self.quadrants) if q.image_path is None]
        if missing:
            QMessageBox.warning(self, "이미지 누락", f"{', '.join(map(str, missing))}사분면 이미지가 선택되지 않았습니다.")
            return

        self.results = self.car_detector.run_detection(self.quadrants)

        for i, count in enumerate(self.results):
            self.quadrants[i].result_label.setText(f"차량 수 : {count}대")

        self.road_drawer.add_detected_vehicles(self.results)

    def call_animator(self):
        if len(self.results) != 4:
            QMessageBox.warning(self, "도로별 차량수 미설정", "도로별 차량수를 모두 설정해주세요.")
            return
        self.road_drawer.animate_vehicles(self.results)
        self.start_signal_cycle()  # 🔥 시뮬레이션과 함께 신호등 시작

        self.elapsed_time = 0
        self.timer_label.setText("시뮬레이션 시간: 0초")
        self.timer_label.show()
        self.elapsed_timer.start(1000)  # 1초마다 업데이트

    def start_signal_cycle(self):
        self.update_signal()

    def update_signal(self):
        self.current_signal_index = (self.current_signal_index + 1) % 4

        # 모든 라벨 흰색
        for label in self.label_widgets:
            label.setStyleSheet("font-weight: bold; font-size: 16px; background-color: red; border-radius: 8px;")

        # 현재 라벨 초록색
        self.label_widgets[self.current_signal_index].setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: lightgreen; border-radius: 8px;"
        )

        current_direction = ['north', 'east', 'south', 'west'][self.current_signal_index]
        self.road_drawer.current_green_direction = current_direction

        # 현재 방향의 초록불 지속 시간 사용 (초 → ms)
        duration = self.green_durations[self.current_signal_index]
        self.signal_timer.start(duration)
    
    def update_elapsed_time(self):
        self.elapsed_time += 1
        self.timer_label.setText(f"시뮬레이션 시간: {self.elapsed_time}초")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoadWindow()
    window.show()
    sys.exit(app.exec_())