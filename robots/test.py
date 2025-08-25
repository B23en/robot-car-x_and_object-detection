from picarx import Picarx
import time

px = Picarx()

print("run.")
px.forward(20)
time.sleep(1)
px.stop()

px.backward(40)
time.sleep(0.5)
px.stop()

px.set_dir_servo_angle(30)
time.sleep(1)
px.set_dir_servo_angle(-30)
time.sleep(1)
px.set_dir_servo_angle(0)
time.sleep(1)

px.set_dir_servo_angle(30)
time.sleep(0.5)
px.forward(30)
time.sleep(1.2)
px.stop()
time.sleep(0.5)
px.set_dir_servo_angle(0)
time.sleep(0.5)

px.stop()
time.sleep(0.2)