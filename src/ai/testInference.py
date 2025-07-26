import os
import time
from ultralytics import YOLO

def get_image_paths(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

def run_inference(model, image_paths):
    total_time = 0.0
    for image_path in image_paths:
        start = time.time()
        model.predict(source=image_path, conf=0.25, save=False, verbose=False)
        end = time.time()
        total_time += (end - start)
    return total_time / len(image_paths), total_time

def main():
    image_paths = get_image_paths("ai/test_car/images")

    print(f"\n\n총 {len(image_paths)}개의 이미지에 대해 테스트 수행 중...\n")

    # fuse 적용 안한 모델
    model_unfused = YOLO("ai/yolov8n.pt")  # 또는 원하는 모델 경로
    time_unfused, total_time_unfused = run_inference(model_unfused, image_paths)
    print(f"[비융합 모델] 총 추론 시간: {total_time_unfused:.4f}초")
    print(f"[비융합 모델] 평균 추론 시간: {time_unfused:.4f}초\n")

    # fuse 적용한 모델
    model_fused = YOLO("ai/yolov8n.pt")
    model_fused.fuse()
    time_fused, total_time_fused = run_inference(model_fused, image_paths)
    print(f"[융합 모델] 총 추론 시간: {total_time_fused:.4f}초")
    print(f"[융합 모델] 평균 추론 시간: {time_fused:.4f}초\n\n")

    # 비교
    total_diff = total_time_unfused - total_time_fused
    avg_diff = time_unfused - time_fused
    print(f"\n총 추론 시간 차이: {total_diff:.4f}초")
    print(f"평균 추론 시간 차이: {avg_diff:.4f}초 {(avg_diff/time_unfused)*100:.2f}% 향상\n\n")

if __name__ == "__main__":
    main()