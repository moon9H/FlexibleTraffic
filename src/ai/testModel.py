from ultralytics import YOLO
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 모델 로드 및 평가
model = YOLO("ai/yolov8x.pt")
model.fuse()
metrics = model.val(data="ai/test_car/data.yaml")

# 클래스 이름 정의
class_names = ['car', 'motorcycle', 'bus', 'truck']

# 📊 전체 결과 출력
print(f"\n📊 [Overall Metrics]")
print(f"Mean Precision : {metrics.box.mp:.3f}")
print(f"Mean Recall    : {metrics.box.mr:.3f}")
print(f"Mean AP@0.5    : {metrics.box.map50:.3f}")
print(f"Mean mAP@0.5:0.95 : {metrics.box.map:.3f}\n")

# 🔍 클래스별 결과 출력
print("🔍 [Class-wise Results]")
for i, name in enumerate(class_names):
    p, r, ap50, ap = metrics.box.class_result(i)
    print(f"{name:<12} P={p:.3f}, R={r:.3f}, AP50={ap50:.3f}, mAP={ap:.3f}")

# 전체 confusion matrix
full_conf_matrix = metrics.confusion_matrix.matrix  # shape: (N, N)

# 사용할 클래스 ID만 선택 (COCO 기준)
target_class_ids = [2, 3, 5, 7]
class_names = ['car', 'motorcycle', 'bus', 'truck']

# 해당 클래스만 인덱싱해서 새로운 confusion matrix 생성
conf_matrix = full_conf_matrix[np.ix_(target_class_ids, target_class_ids)]

# 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix.astype(int), annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Class-wise Confusion Matrix')
plt.tight_layout()
plt.show()

# Precision 계산 및 시각화
tp = np.diag(conf_matrix)
fp_plus_tp = conf_matrix.sum(axis=0)
precision_per_class = tp / np.maximum(fp_plus_tp, 1e-6)

plt.figure(figsize=(8, 6))
ax = sns.barplot(x=class_names, y=precision_per_class)
plt.ylim(0, 1.05)
plt.ylabel('Precision')
plt.title('Class-wise Precision')

# 막대 위에 소수점 둘째자리 텍스트 추가
for i, p in enumerate(precision_per_class):
    ax.text(i, p + 0.02, f'{p:.2f}', ha='center', va='bottom', color='black', fontsize=10)

plt.tight_layout()
plt.show()