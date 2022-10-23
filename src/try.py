<<<<<<< HEAD
import modules

for i in range(10):
    data = str(modules.GPS.Read_data)
    print(data)

modules.servo.role(90)

t = 1000
duty = 0.5
modules.DCmotor.foword(duty , t)
modules.DCmotor.back(duty , t)
modules.DCmotor.left_role(duty , t)
modules.DCmotor.right_role(duty , t)

modules.cds.read()

modules.xbee_send.send_message(DATA_TO_SEND="Hello Xbee!")
import modules as md

for i in range(10):
    data = str(md.GPS.Read_data)
    print(data)

md.servo.role(90)

t = 1000
duty = 0.5
md.DCmotor.foword(duty , t)
md.DCmotor.back(duty , t)
md.DCmotor.left_role(duty , t)
md.DCmotor.right_role(duty , t)

md.cds.read()

=======
import modules as md

for i in range(10):
    data = str(md.GPS.Read_data)
    print(data)

md.servo.role(90)

t = 1000
duty = 0.5
md.DCmotor.foword(duty , t)
md.DCmotor.back(duty , t)
md.DCmotor.left_role(duty , t)
md.DCmotor.right_role(duty , t)

md.cds.read()

>>>>>>> 9dcdc1a (change modules)
md.xbee_send.send_message(DATA_TO_SEND="Hello Xbee!")
