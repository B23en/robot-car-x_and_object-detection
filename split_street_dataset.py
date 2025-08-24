
import os, random, shutil
from pathlib import Path

root = Path("/Users/sonwonbin/vscode/Project/Robot-car-project/dataset_street_signs")
train_img = root / "train/images"
train_lbl = root / "train/labels"
val_img = root / "val/images"
val_lbl = root / "val/labels"

# 폴더 생성
val_img.mkdir(parents=True, exist_ok=True)
val_lbl.mkdir(parents=True, exist_ok=True)

# 이미지 파일 목록
files = list(train_img.glob("*.jpg"))  # 확장자에 맞게 조정
n_val = int(len(files) * 0.2)

# 무작위 20% 샘플
val_files = random.sample(files, n_val)

for img_path in val_files:
    lbl_path = train_lbl / (img_path.stem + ".txt")

    # move 이미지
    shutil.move(str(img_path), val_img / img_path.name)
    # move 라벨
    if lbl_path.exists():
        shutil.move(str(lbl_path), val_lbl / lbl_path.name)

print(f"Moved {n_val} files to val/")