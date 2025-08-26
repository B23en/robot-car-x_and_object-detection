from pathlib import Path

TARGET_FOLDER = Path(r"/Users/sonwonbin/vscode/Project/Robot-car-project/dataset_left_right/val/labels")

# CLASS_MAP = {
#     5: 0,
#     2: 1,
#     3: 2,
#     4: 3
# }
CLASS_MAP = {
    0: 1,
    1: 2
}

for f in TARGET_FOLDER.rglob("*.txt"):
    out = []
    for s in f.read_text(encoding="utf-8").splitlines():
        a = s.split()
        if int(a[0]) in CLASS_MAP.keys():
            a[0] = str(CLASS_MAP[int(a[0])])
            out.append(" ".join(a))

    f.write_text("\n".join(out) + "\n", encoding="utf-8")

print("done.")