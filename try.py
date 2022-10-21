import cds
import GPS
import servo
import xbee_send
import DCmotor

for i in range(10):
    data = str(GPS.Read_data)
    print(data)

servo.role(90)

t = 1000
duty = 0.5
DCmotor.foword(duty , t)
DCmotor.back(duty , t)
DCmotor.left_role(duty , t)
DCmotor.right_role(duty , t)

cds.read()

xbee_send.send_message(DATA_TO_SEND="Hello Xbee!")