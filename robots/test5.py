from picarx import Picarx
import time

px = Picarx()

# time.sleep(0.1)
# px.set_cam_pan_angle(10)
# time.sleep(1)
# px.set_cam_pan_angle(-10)
# time.sleep(1)
# px.set_cam_pan_angle(0)
# time.sleep(0.5)
# px.set_cam_pan_angle(1)
# time.sleep(1)

for dir in range(25):
    px.set_cam_pan_angle(dir)
    time.sleep(0.1)

time.sleep(0.5)

for dir in range(25, -1, -1):
    px.set_cam_pan_angle(dir)
    time.sleep(0.1)

px.set_cam_pan_angle(0)
time.sleep(0.5)