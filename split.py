# split_coco_9_1.py
import json, random
from pathlib import Path

# 1) 경로 지정
root = Path("/Users/sonwonbin/vscode/Project/Robot-car-project/dataset")
src  = root / "f_train.json"
dst_train = root / "f_train_split.json"
dst_val   = root / "f_val_split.json"

# 2) 로드
with src.open("r", encoding="utf-8") as f:
    coco = json.load(f)

images = coco.get("images", [])
annotations = coco.get("annotations", [])
categories = coco.get("categories", [])

# 3) 이미지 섞고 9:1 분할 (재현성 고정)
random.seed(42)
random.shuffle(images)
split_idx = int(len(images) * 0.9)
train_images = images[:split_idx]
val_images   = images[split_idx:]

# 4) image_id 세트 만들기
train_ids = {img["id"] for img in train_images}
val_ids   = {img["id"] for img in val_images}

# 5) 어노테이션을 이미지 분할에 맞춰 필터링
train_annotations = [ann for ann in annotations if ann.get("image_id") in train_ids]
val_annotations   = [ann for ann in annotations if ann.get("image_id") in val_ids]

# 6) 결과 COCO 객체 구성
train_coco = {
    "images": train_images,
    "annotations": train_annotations,
    "categories": categories
}
val_coco = {
    "images": val_images,
    "annotations": val_annotations,
    "categories": categories
}

# 7) 저장
with dst_train.open("w", encoding="utf-8") as f:
    json.dump(train_coco, f, ensure_ascii=False)
with dst_val.open("w", encoding="utf-8") as f:
    json.dump(val_coco, f, ensure_ascii=False)

print(f"✅ Done.")
print(f"Train images: {len(train_images)}, anns: {len(train_annotations)} → {dst_train}")
print(f"Val   images: {len(val_images)}, anns: {len(val_annotations)} → {dst_val}")