from modules import *

from picarx import Picarx
import time

TH = 650
px = Picarx()

def picar_init():
    px.set_cam_tilt_angle(10)

def start(px: Picarx):
    print("activate.")

    time.sleep(3)
    picar_init()
    print("init.")
    time.sleep(1)
    print("start.")
    while True:
        track(px, TH)
        time.sleep(0.02)

if __name__ == "__main__":
    try:
        start(px)
    except KeyboardInterrupt:
        pass
    finally:
        px.stop()
        time.sleep(0.3)
        px.set_cam_tilt_angle(0)
        time.sleep(0.3)
        px.set_dir_servo_angle(0)
        time.sleep(0.1)
