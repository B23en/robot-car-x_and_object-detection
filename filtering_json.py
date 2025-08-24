import json
import shutil
import os

target_ids = [70, 69, 68, 43]

with open(r"dataset/test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

filtered_annotations = [item for item in data['annotations'] if item['category_id'] in target_ids]
filtered_ids = [item['image_id'] for item in filtered_annotations]
filtered_images = [item for item in data['images'] if item['id'] in filtered_ids]

filtered_json = {}
filtered_json['images'] = filtered_images
filtered_json['annotations'] = filtered_annotations

with open("dataset/f_test.json", "w", encoding="utf-8") as f:
    json.dump(filtered_json, f, ensure_ascii=False, indent=4)

filtered_filenames = [item['file_name'] for item in filtered_images]
src_img_dir = r"dataset/images"
dst_img_dir = r"dataset/f_images"

cnt = 0
for filename in filtered_filenames:
    src_path = os.path.join(src_img_dir, filename)
    dst_path = os.path.join(dst_img_dir, filename)
    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
        cnt += 1
    # print(f"Moved: {filename}")

print(f"{cnt} files completed.")
print("✅ done.")