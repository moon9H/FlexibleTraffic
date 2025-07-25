import time
from ultralytics import YOLO

# 테스트 이미지 경로
IMAGE_PATH = "../img/test/car.jpg"

def run_inference(model, image_path):
    start = time.time()
    results = model.predict(source=image_path, conf=0.25, save=False, verbose=False)
    end = time.time()
    return end - start

def main():
    print("\n\n모델 로딩 중...\n")

    # fuse 적용 안한 모델
    model_unfused = YOLO("ai/yolov8x.pt")  # 또는 원하는 모델 경로
    time_unfused = run_inference(model_unfused, IMAGE_PATH)
    print(f"[비융합 모델] 추론 시간: {time_unfused:.4f}초\n\n")

    # fuse 적용한 모델
    model_fused = YOLO("ai/yolov8x.pt")
    model_fused.fuse()
    time_fused = run_inference(model_fused, IMAGE_PATH)
    print(f"[융합 모델] 추론 시간: {time_fused:.4f}초\n\n")

    # 비교
    diff = time_unfused - time_fused
    print(f"\n추론 시간 차이: {diff:.4f}초 ({(diff/time_unfused)*100:.2f}% 향상)\n\n\n")

if __name__ == "__main__":
    main()