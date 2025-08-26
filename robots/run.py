from modules import *

from picarx import Picarx
import time

TH = 1000
px = Picarx()

def picar_init():
    px.set_cam_tilt_angle(10)

def start(px: Picarx):
    print("activate.")

    time.sleep(2)
    picar_init()
    time.sleep(1)
    print("start.")
    while True:
        track(px, TH)
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        start(px)
    except KeyboardInterrupt:
        pass
    finally:
        px.stop()
        time.sleep(0.3)
        px.set_cam_tilt_angle(10)
        time.sleep(0.3)
        px.set_dir_servo_angle(0)
        time.sleep(0.1)
