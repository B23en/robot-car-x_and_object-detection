import socket, struct, time, cv2
from picamera2 import Picamera2

HOST = ""  # IP (update if needed)
PORT = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480), "format": "BGR888"})
picam2.configure(config)
picam2.start()

try:
    while True:
        frame = picam2.capture_array()           # Now BGR numpy array (due to BGR888)
        ok, buf = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            print("[CLIENT] JPEG encode failed; skipping")
            time.sleep(0.2)
            continue
        data = buf.tobytes()
        s.sendall(struct.pack('!Q', len(data)) + data)
        # print("Captured & sent.")
        time.sleep(0.2)  
except KeyboardInterrupt:
    pass
finally:
    s.close()
    picam2.close()