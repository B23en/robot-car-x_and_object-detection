import socket, struct, cv2, numpy as np
import threading
from ultralytics import YOLO

from check_bbox import CheckBbox

HOST = "0.0.0.0"   # listen on all interfaces (Mac)
PORT = 5001         # keep same port as before
CMD_PORT = 5002  # lightweight command server (e.g., GET_SIGN)

checker = CheckBbox()
curr_sign = "none"

def _handle_cmd_client(conn, addr):
    """Handle a single command client; supports GET_SIGN."""
    global curr_sign
    with conn:
        try:
            data = conn.recv(1024)
            if not data:
                return
            msg = data.decode("utf-8", "ignore").strip()
            if msg.startswith("GET_SIGN"):
                # Reply with the latest detected sign string, e.g., "turn_left", "turn_right", etc.
                conn.sendall(curr_sign.encode("utf-8"))
            elif msg.startswith("RESET_SIGN"):
                # Reset current sign to "none"
                checker.reset_curr_sign()
                curr_sign = "none"
                conn.sendall(b"OK")
            else:
                conn.sendall(b"ERR")
        except Exception:
            # Silently ignore per-connection errors
            pass


def _run_cmd_server():
    """Background thread: simple TCP server to answer control queries (GET_SIGN)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cs.bind((HOST, CMD_PORT))
        cs.listen(5)
        print(f"[SERVER] Command port listening on {HOST}:{CMD_PORT}")
        while True:
            try:
                c, a = cs.accept()
                threading.Thread(target=_handle_cmd_client, args=(c, a), daemon=True).start()
            except Exception:
                # Keep the command server alive even if accept() fails transiently
                continue

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
    # Start lightweight command server (answers GET_SIGN requests)
    threading.Thread(target=_run_cmd_server, daemon=True).start()
    model = YOLO("../models/best_s_adv.pt", task="detect")  # or use a custom/best.pt path
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
                results = model(frame, verbose=False, device="mps", conf=0.7)
                curr, second, size, s_size = checker.check(results)
                print(f"curr: {curr}, second: {second}, size: {size}, s_size: {s_size}, gap: {size-s_size}")
                curr_sign = curr
                annotated = results[0].plot()  # BGR image with boxes/labels
                cv2.imshow("PiCar-X YOLO", annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()
            print("[SERVER] Closed.")