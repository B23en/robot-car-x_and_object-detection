from picarx import Picarx
import time

th = 900
px = Picarx()

try:
    while True:
        l, m, r = px.get_grayscale_data()

        if m > th:
            px.set_dir_servo_angle(0)
            px.forward(30)
        elif l > th:
            px.set_dir_servo_angle(-25)
            px.forward(30)
        elif r < th:
            px.set_dir_servo_angle(25)
            px.forward(30)
        else:
            px.stop()
        time.sleep(0.05)

except KeyboardInterrupt:
    px.stop()
    px.set_dir_servo_angle(0)