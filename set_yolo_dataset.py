from pathlib import Path
import json
import shutil

ROOT = Path("/Users/sonwonbin/vscode/Project/Robot-car-project/dataset")

TRAIN_JSON = ROOT / "f_train_split.json"
VAL_JSON   = ROOT / "f_val_split.json"

src_imgs_dir = ROOT / "_imgs"

yolo_images_train = ROOT / "images" / "train"
yolo_images_val = ROOT / "images" / "val"
yolo_labels_train = ROOT / "labels" / "train"
yolo_labels_val = ROOT / "labels" / "val"

CATEGORY_ID_TO_CLASS = {
    68: 0,
    70: 1,
    69: 2,
    43: 3
}

# --- Helper functions ---
from collections import defaultdict

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def coco_to_yolo_xywh(bbox, img_w: int, img_h: int):
    """
    COCO bbox: [x_min, y_min, w, h] (pixels)
    YOLO  bbox: [x_center, y_center, w, h] normalized to [0,1]
    """
    x, y, w, h = bbox
    x_c = (x + w / 2.0) / img_w
    y_c = (y + h / 2.0) / img_h
    w_n = w / img_w
    h_n = h / img_h
    # clamp just in case of slight rounding issues
    x_c = min(max(x_c, 0.0), 1.0)
    y_c = min(max(y_c, 0.0), 1.0)
    w_n = min(max(w_n, 0.0), 1.0)
    h_n = min(max(h_n, 0.0), 1.0)
    return x_c, y_c, w_n, h_n

def generate_txts(json_path: dict, out_label_dir: Path):
    """Read COCO-style JSON and write YOLO .txt labels (normalized) per image.

    - Creates an empty .txt for images that have no matching annotations (valid for negative samples).
    - Uses CATEGORY_ID_TO_CLASS to map category_id -> class index. Unmapped category_ids are skipped.
    """
    ensure_dir(out_label_dir)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    images = data.get("images", [])
    annotations = data.get("annotations", [])

    # index image meta by id
    img_by_id = {img["id"]: img for img in images}

    # group annotations by image_id
    anns_by_img = defaultdict(list)
    for ann in annotations:
        anns_by_img[ann["image_id"]].append(ann)

    written = 0
    skipped_cats = 0

    for img in images:
        img_id = img["id"]
        file_name = img["file_name"]
        img_w = img["width"]
        img_h = img["height"]

        lines = []
        for ann in anns_by_img.get(img_id, []):
            cat_id = ann.get("category_id")
            if cat_id not in CATEGORY_ID_TO_CLASS:
                skipped_cats += 1
                continue
            cls = CATEGORY_ID_TO_CLASS[cat_id]
            x_c, y_c, w_n, h_n = coco_to_yolo_xywh(ann["bbox"], img_w, img_h)
            lines.append(f"{cls} {x_c:.6f} {y_c:.6f} {w_n:.6f} {h_n:.6f}")

        out_txt = out_label_dir / (Path(file_name).stem + ".txt")
        ensure_dir(out_txt.parent)
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        written += 1

    print(f"[labels] Wrote {written} label files to {out_label_dir}")
    if skipped_cats:
        print(f"[labels] Skipped {skipped_cats} annotations due to unmapped category_id")

def move_imgs(_json: dict, dest_img_dir: Path):
    """Copy source images referenced by the JSON into the YOLO images folder.

    Uses global `src_imgs_dir`. Preserves folder structure if any.
    """
    ensure_dir(dest_img_dir)

    with open(_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    images = data.get("images", [])
    copied, missing = 0, 0

    for img in images:
        rel = Path(img["file_name"])  # may be nested
        src = src_imgs_dir / rel
        dst = dest_img_dir / rel
        ensure_dir(dst.parent)
        if src.exists():
            # use copy2 to keep metadata; change to move if you prefer moving
            shutil.copy2(src, dst)
            copied += 1
        else:
            print(f"[images] MISSING: {src}")
            missing += 1

    print(f"[images] Copied {copied} images to {dest_img_dir} ({missing} missing)")


# --- Main block for dataset preparation ---
if __name__ == "__main__":
    # Ensure YOLO folder structure exists
    ensure_dir(yolo_images_train)
    ensure_dir(yolo_images_val)
    ensure_dir(yolo_labels_train)
    ensure_dir(yolo_labels_val)

    # 1) Move/copy images
    move_imgs(TRAIN_JSON, yolo_images_train)
    move_imgs(VAL_JSON, yolo_images_val)

    # 2) Generate YOLO .txt labels
    generate_txts(TRAIN_JSON, yolo_labels_train)
    generate_txts(VAL_JSON, yolo_labels_val)

    print("Done: YOLO dataset prepared.")
