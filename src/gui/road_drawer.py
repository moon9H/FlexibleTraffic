from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QLabel, QGraphicsRectItem
from PyQt5.QtCore import QTimer

class VehicleItem(QGraphicsRectItem):
    def __init__(self, direction, x, y, stop_line, width=40, height=25, color=QColor(30, 144, 255)):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.NoPen))
        self.setPos(x, y)
        self.direction = direction
        self.speed = 3
        self.stop_line = stop_line  # ✅ 정지선 정보 저장

    def move_forward(self, current_green_direction=None, current_phase=None):
        # ✅ 정지선 넘었는지 판단
        crossed = False
        if self.direction == 'north':
            crossed = self.y() > self.stop_line
        elif self.direction == 'south':
            crossed = self.y() < self.stop_line
        elif self.direction == 'east':
            crossed = self.x() < self.stop_line
        elif self.direction == 'west':
            crossed = self.x() > self.stop_line

        # ✅ 아직 정지선 전인데 초록불이 아니면 멈춤
        if not crossed:
            if current_phase == "green":
                if current_green_direction != self.direction:
                    return
            elif current_phase == "yellow":
                    return
            else:
                return

        # ✅ 이동
        dx, dy = 0, 0
        if self.direction == 'north':
            dy = self.speed
        elif self.direction == 'south':
            dy = -self.speed
        elif self.direction == 'east':
            dx = -self.speed
        elif self.direction == 'west':
            dx = self.speed
        self.moveBy(dx, dy)

class RoadDrawer:
    def __init__(self, scene, scene_width, scene_height, parent=None):
        self.scene = scene
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.parent = parent
        self.vert_road_width = 200
        self.horiz_road_height = 200
        self.center_box_size = 200
        self.center_x = self.scene_width / 2
        self.center_y = self.scene_height / 2

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.vehicles = []

    def draw_intersection(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb_size = self.center_box_size
        self.scene.addRect(QRectF(csx - vrw / 2, 0, vrw, self.scene_height), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(0, csy - hrh / 2, self.scene_width, hrh), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(csx - cb_size / 2, csy - cb_size / 2, cb_size, cb_size), brush=QBrush(QColor("dimgray")))

    def draw_lane_markings(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb_size = self.center_box_size
        white_pen = QPen(QColor("white")); white_pen.setWidth(2); white_pen.setStyle(Qt.DashLine)
        yellow_pen = QPen(QColor("yellow")); yellow_pen.setWidth(3)
        stop_pen = QPen(QColor("white")); stop_pen.setWidth(4)
        border_pen = QPen(QColor("white")); border_pen.setWidth(2)

        self.scene.addLine(csx, 0, csx, csy - cb_size / 2, yellow_pen)
        self.scene.addLine(csx, csy + cb_size / 2, csx, self.scene_height, yellow_pen)
        for x in [csx - vrw / 4, csx + vrw / 4]:
            self.scene.addLine(x, 0, x, csy - cb_size / 2, white_pen)
            self.scene.addLine(x, csy + cb_size / 2, x, self.scene_height, white_pen)
        self.scene.addLine(0, csy, csx - cb_size / 2, csy, yellow_pen)
        self.scene.addLine(csx + cb_size / 2, csy, self.scene_width, csy, yellow_pen)
        for y in [csy - hrh / 4, csy + hrh / 4]:
            self.scene.addLine(0, y, csx - cb_size / 2, y, white_pen)
            self.scene.addLine(csx + cb_size / 2, y, self.scene_width, y, white_pen)

        self.scene.addLine(csx - vrw / 2, csy - cb_size / 2, csx + vrw / 2, csy - cb_size / 2, stop_pen)
        self.scene.addLine(csx - vrw / 2, csy + cb_size / 2, csx + vrw / 2, csy + cb_size / 2, stop_pen)
        self.scene.addLine(csx - cb_size / 2, csy - hrh / 2, csx - cb_size / 2, csy + hrh / 2, stop_pen)
        self.scene.addLine(csx + cb_size / 2, csy - hrh / 2, csx + cb_size / 2, csy + hrh / 2, stop_pen)

        self.scene.addRect(csx - vrw / 2, 0, vrw, self.scene_height, border_pen)
        self.scene.addRect(0, csy - hrh / 2, self.scene_width, hrh, border_pen)

    def add_road_labels(self, labels):
        label_positions = [
            (450, 10),
            (800, 320),
            (350, 860),
            (10, 550),
        ]
        self.parent.label_widgets = []  # 라벨 저장 리스트 초기화

        for i, (x, y) in enumerate(label_positions):
            road_label = QLabel(labels[i], self.parent)
            road_label.setGeometry(x, y, 100, 30)
            road_label.setAlignment(Qt.AlignCenter)
            road_label.setStyleSheet(
                "font-weight: bold; font-size: 16px; background: rgba(255,255,255,180); border-radius: 8px;"
            )
            self.parent.label_widgets.append(road_label)  # ✅ 이 줄이 가장 중요!

    def add_detected_vehicles(self, vehicle_counts):
        car_gap = 10
        car_width = 40
        car_height = 25
        cx, cy = self.center_x, self.center_y
        vrw, hrh = self.vert_road_width, self.horiz_road_height
        cb = self.center_box_size

        def distribute(n):
            h = n // 2
            return [h + n % 2, h]

        lanes = {
            "north": [cx - vrw / 4 - car_width / 2],
            "east": [cy - hrh / 4 - car_height / 2],
            "south": [cx + vrw / 4 - car_width / 2],
            "west": [cy + hrh / 4 - car_height / 2]
        }
        stop_lines = {
            "north": cy - cb / 2 - car_height - car_gap,
            "south": cy + cb / 2 + car_gap,
            "east": cx + cb / 2 + car_gap,
            "west": cx - cb / 2 - car_width - car_gap
        }

        dir_map = {"north": 0, "east": 1, "south": 2, "west": 3}

        for dir in ["north"]:
            base_x = lanes[dir][0]
            count = vehicle_counts[dir_map[dir]]
            dist = distribute(count)
            offsets = [-car_width / 2 - 5, car_width / 2 + 5]
            for i in range(2):
                for j in range(dist[i]):
                    x = base_x + offsets[i]
                    y = stop_lines[dir] - j * (car_height + car_gap)
                    car = VehicleItem(dir, x, y, stop_lines[dir])
                    self.scene.addItem(car)
                    self.vehicles.append(car)

        for dir in ["east"]:
            base_y = lanes[dir][0]
            count = vehicle_counts[dir_map[dir]]
            dist = distribute(count)
            offsets = [-car_height / 2 - 5, car_height / 2 + 5]
            for i in range(2):
                for j in range(dist[i]):
                    y = base_y + offsets[i]
                    x = stop_lines[dir] + j * (car_width + car_gap)
                    car = VehicleItem(dir, x, y, stop_lines[dir])
                    self.scene.addItem(car)
                    self.vehicles.append(car)

        for dir in ["south"]:
            base_x = lanes[dir][0]
            count = vehicle_counts[dir_map[dir]]
            dist = distribute(count)
            offsets = [-car_width / 2 - 5, car_width / 2 + 5]
            for i in range(2):
                for j in range(dist[i]):
                    x = base_x + offsets[i]
                    y = stop_lines[dir] + j * (car_height + car_gap)
                    car = VehicleItem(dir, x, y, stop_lines[dir])
                    self.scene.addItem(car)
                    self.vehicles.append(car)

        for dir in ["west"]:
            base_y = lanes[dir][0]
            count = vehicle_counts[dir_map[dir]]
            dist = distribute(count)
            offsets = [-car_height / 2 - 5, car_height / 2 + 5]
            for i in range(2):
                for j in range(dist[i]):
                    y = base_y + offsets[i]
                    x = stop_lines[dir] - j * (car_width + car_gap)
                    car = VehicleItem(dir, x, y, stop_lines[dir])
                    self.scene.addItem(car)
                    self.vehicles.append(car)

    def update_simulation(self):
        for car in self.vehicles:
            car.move_forward(self.current_green_direction, self.current_phase)  # ✅ 초록불 방향 전달

    def animate_vehicles(self, vehicle_counts):
        self.timer.start(30)