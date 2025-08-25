import socket, struct, cv2, numpy as np
from ultralytics import YOLO

HOST = "0.0.0.0"   # listen on all interfaces (Mac)
PORT = 5001         # keep same port as before

def recv_exact(sock, size: int):
    buf = b""
    while len(buf) < size:
        chunk = sock.recv(min(65536, size - len(buf)))
        if not chunk:
            return None
        buf += chunk
    return buf

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[SERVER] Listening on {HOST}:{PORT} ...")
    model = YOLO("../models/best_s.pt", task="detect")  # or use a custom/best.pt path
    model.to("mps")  # force model to use Apple Metal Performance Shaders
    conn, addr = s.accept()
    print("[SERVER] Connected:", addr)

    with conn:
        try:
            while True:
                header = recv_exact(conn, 8)           # 8-byte length (unsigned long long, network order)
                if not header:
                    print("[SERVER] Disconnected.")
                    break
                (length,) = struct.unpack("!Q", header)
                payload = recv_exact(conn, length)
                if payload is None:
                    print("[SERVER] Incomplete frame; closing.")
                    break
                frame = cv2.imdecode(np.frombuffer(payload, dtype=np.uint8), cv2.IMREAD_COLOR)  # BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if frame is None:
                    print("[SERVER] Decode failed (frame None)")
                    continue
                # YOLO inference (CPU by default); set device="mps"/"cuda" if available
                results = model(frame, verbose=False, device="mps")
                annotated = results[0].plot()  # BGR image with boxes/labels
                cv2.imshow("PiCar-X YOLO", annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()
            print("[SERVER] Closed.")