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

md.xbee_send.send_message(DATA_TO_SEND="Hello Xbee!")
