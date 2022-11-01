import modules
import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
GPIO.setup(25, GPIO.IN)

CDS_PIN = 25

def main():
    #TODO: 落下してからパラシュートを切り離すまでの動作
    while GPIO.input(CDS_PIN) >= 100:   #TODO: CDSが読み取る値　要検証
            deployment(90)
            break

    #TODO: ゴールするまでの動作
    while 1:
        gps_data = gps()

# --------------------------------------------


#TODO: サーボを使って展開するコードを書く
def deployment(angle):
    return modules.servo.role(angle)

#TODO: 2つの座補から角度と距離を返す関数
def calc_moment(x0 , y0 , x , y):
    distance_x = x - x0
    distance_y = y - y0
    distance = math.sqrt(distance_x**2 + distance_y**2)
    sita = math.atan(distance_y/distance_x)
    return float(distance) , float(sita)

#TODO: モーターを動かすコードを書く
def move_motor(direc , duty , time):
    if direc == 'fd':
        return modules.DCmotor.foword(duty , time)
    elif direc == 'bc':
        return modules.DCmotor.back(duty , time)
    elif direc == 'rt':
        return modules.DCmotor.right_role(duty , time)
    elif direc == 'lt':
        return modules.DCmotor.left_role(duty ,time) 

#TODO: GPSを読み取る関数
def gps():
    return modules.GPS.Read_data()



if __name__ == "__main__":
    main()
