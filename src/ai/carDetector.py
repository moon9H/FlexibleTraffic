from ultralytics import YOLO

class CarDetector:
    def __init__(self, model_path="ai/yolov8x.pt"):
        self.model = YOLO(model_path)
        self.model.fuse() # for faster inference

    def detect_cars(self, image_path):
        results = self.model.predict(source=image_path, conf=0.25, save=False, verbose=False)
        if not results or not results[0].boxes:
            return 0
        boxes = results[0].boxes
        car_count = 0
        for cls_id in boxes.cls:
            if int(cls_id) in [2, 3, 5, 7]:  # car, motorcycle, bus, truck
                car_count += 1
        return car_count

    def run_detection(self, quadrant_widgets):
        results = []
        for widget in quadrant_widgets:
            count = self.detect_cars(widget.image_path)
            results.append(count)
        return results