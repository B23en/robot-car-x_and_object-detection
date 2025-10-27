from picarx import Picarx
import time

px = Picarx()

px.stop()
time.sleep(0.5)
px.backward(20)
time.sleep(0.49)
px.stop()
time.sleep(0.5)
px.set_dir_servo_angle(30)
time.sleep(0.5)
px.forward(30)
time.sleep(1.8)
px.stop()
time.sleep(0.5)
px.set_dir_servo_angle(0)
time.sleep(0.5)

px.stop()
time.sleep(0.2)
