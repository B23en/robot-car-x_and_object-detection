from picarx import Picarx
import socket

# Change this to your Mac's mDNS hostname (e.g., "aaa.local") or IP address on the same LAN
SERVER_HOST = "172.20.10.13"
SERVER_CMD_PORT = 5002
import time

sign = "none"

def test(px: Picarx):
    print("test")

def track(px: Picarx, th):
    l, m, r = px.get_grayscale_data()

    # stop at a line
    if l > th and m > th and r > th:
        px.stop()
        curr_sign = request_sign()
        print(f"curr_sign: {curr_sign}")
        
        time.sleep(0.5)
        if curr_sign == "go_straight":
            go_straight(px)
            # px.forward(20)
            # time.sleep(0.5)
            # px.stop()
        elif curr_sign == "turn_left":
            turn_left(px, th)
        elif curr_sign == "turn_right":
            turn_right(px, th)
        elif curr_sign == "stop":
            wait(px)
            px.forward(20)
            time.sleep(0.5)
            px.stop()
        elif curr_sign == "stop_and_turn_left":
            stop_and_turn_left(px, th)
        elif curr_sign == "stop_and_turn_right":
            stop_and_turn_right(px, th)
        else:
            px.forward(10)
            time.sleep(0.1)
            px.stop()
        
        reset_sign()
        time.sleep(0.5)
        # detect_around(px)
        return

    print(f"[track] - l({l}) m({m}) r({r})", end=' >> ')
    if m > th: # need to test
        print("'forward'")
        px.set_dir_servo_angle(0)
        px.forward(15)
    elif l > th:
        print("'left'")
        px.set_dir_servo_angle(-20)
        px.forward(15)
    elif r > th:
        print("'right'")
        px.set_dir_servo_angle(20)
        px.forward(15)
    # elif m < th/3 and l < th/3 and r < th/3:
    #     print("'stop'")
    #     px.stop()
    else:
        print("'forward?'")
        px.set_dir_servo_angle(0)
        px.forward(15)

# turn right sign
def turn_right(px, th): 
    print("[turn_right]")
    px.stop()
    time.sleep(0.5)
    px.set_dir_servo_angle(0)
    time.sleep(0.1)
    px.backward(20)
    time.sleep(0.49)
    px.stop()
    time.sleep(0.5)
    px.set_dir_servo_angle(25)
    time.sleep(0.5)
    px.forward(20)
    time.sleep(1.8)
    px.stop()
    time.sleep(0.5)

    while True:
        l, m, r = px.get_grayscale_data()
        if r > th:
            break
        print(f"tune - l({l}) m({m}) r({r})")
        px.forward(5)
        time.sleep(0.05)
    px.stop()

    time.sleep(0.1)
    px.set_dir_servo_angle(0)
    time.sleep(0.1)
    px.backward(10)
    time.sleep(1.5)
    px.stop()
    time.sleep(0.1)

    print("turn right done.")

# turn left sign
def turn_left(px, th):
    print("[turn_left]")
    px.stop()
    time.sleep(0.5)
    px.set_dir_servo_angle(0)
    time.sleep(0.1)
    px.backward(20)
    time.sleep(0.49)
    px.stop()
    time.sleep(0.5)
    px.set_dir_servo_angle(-25)
    time.sleep(0.5)
    px.forward(20)
    time.sleep(1.8)
    px.stop()
    time.sleep(0.5)

    while True:
        l, m, r = px.get_grayscale_data()
        if l > th:
            break
        print(f"tune - l({l}) m({m}) r({r})")
        px.forward(5)
        time.sleep(0.05)
    px.stop()

    time.sleep(0.1)
    px.set_dir_servo_angle(0)
    time.sleep(0.1)
    px.backward(10)
    time.sleep(1.5)
    px.stop()
    time.sleep(0.1)

    print("turn left done.")

# go straight
def go_straight(px):
    print("[go_straight]")
    px.stop()

# wait for a few seconds
def wait(px):
    print("[wait]")
    px.stop()
    wait_time = 3
    for t in range(wait_time):
        time.sleep(1)
        print(f"wait - {t+1}")

def return_to_line(px):
    pass

def arrive(px):
    pass

def request_sign(host: str = SERVER_HOST, port: int = SERVER_CMD_PORT, timeout: float = 1.0):
    """Ask the Mac server for the latest detected sign via a tiny TCP command (GET_SIGN).

    Returns the sign string (e.g., "turn_left", "turn_right", "go_straight", "stop", "none"), or None on error.
    """
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.sendall(b"GET_SIGN\n")
                resp = sock.recv(64)
                if not resp:
                    raise ValueError("No response received")
                return resp.decode("utf-8", "ignore").strip()
        except Exception as e:
            print(f"[request_sign] error on attempt {attempt}: {e}")
            time.sleep(0.2)
    return None

def reset_sign(host: str = SERVER_HOST, port: int = SERVER_CMD_PORT, timeout: float = 1.0):
    """Request the Mac server to reset its current detected sign to "none".

    Returns True on success (server replies b"OK"), otherwise False.
    """
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.sendall(b"RESET_SIGN\n")
                resp = sock.recv(16)
                return resp == b"OK"
        except Exception as e:
            print(f"[reset_sign] error on attempt {attempt}: {e}")
            time.sleep(0.2)
    return False
    
def stop_and_turn_right(px, th):
    print("[[stop_and_turn_right]]")
    time.sleep(0.1)
    wait(px)
    turn_right(px, th)

def stop_and_turn_left(px, th):
    print("[[stop_and_turn_left]]")
    time.sleep(0.1)
    wait(px)
    turn_left(px, th)

def detect_around(px):
    print("[detect]")
    time.sleep(0.1)
    for dir in range(26):
        px.set_cam_pan_angle(dir)
        time.sleep(0.1)

    time.sleep(1)

    for dir in range(26, -1, -1):
        px.set_cam_pan_angle(dir)
        time.sleep(0.1)

    px.set_cam_pan_angle(0)
    time.sleep(0.5)

    for dir in range(0, -26, -1):
        px.set_cam_pan_angle(dir)
        time.sleep(0.1)

    time.sleep(1)

    for dir in range(-26, 1, 1):
        px.set_cam_pan_angle(dir)
        time.sleep(0.1)