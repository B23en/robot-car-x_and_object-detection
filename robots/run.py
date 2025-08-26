from modules import *

from picarx import Picarx
import time

TH = 1000
px = Picarx()

def picar_init():
    px.set_cam_tilt_angle(15)

def start(px: Picarx):
    print("activate.")

    time.sleep(2)
    picar_init()
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
        px.set_dir_servo_angle(0)
