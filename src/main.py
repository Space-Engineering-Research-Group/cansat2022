import modules
import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
GPIO.setup(25, GPIO.IN)

CDS_PIN = 25

Rp = 6356.8 * 1000#[m] (地球の極半径)
Re = 6378.1 * 1000#[m] (地球の赤道半径)
pi = 3.141592

def main():
    #TODO: 落下してからパラシュートを切り離すまでの動作
    while GPIO.input(CDS_PIN) >= 100:   #TODO: CDSが読み取る値　要検証
            deployment(90)
            break

    gps_start = [gps()]
    gps_x0 = gps_start[-1]
    gps_y0 = gps_start[-2]
    #TODO: ゴールするまでの動作
    while calc_moment(x = 2*pi*Re*(gps_x0 / 360) , y = 2*pi*Rp*(gps_y0 / 360) , data='d') < 10:
        move_motor(direc='fd' , duty=1.0 , time=1000)
        temp_gps = gps()
        xbee(temp_gps)
        
         

# --------------------------------------------


#TODO: サーボを使って展開するコードを書く
def deployment(angle):
    return modules.servo.role(angle)

#TODO: 2つの座補から角度と距離を返す関数
def calc_moment(x0 , y0 , x=modules.GPS.GPS_xonly() , y=modules.GPS.GPS_yonly() , data='a'):
    distance_x = x - x0
    distance_y = y - y0
    distance = math.sqrt(distance_x**2 + distance_y**2)
    sita = math.atan(distance_y/distance_x)
    if data == 'd':
        return float(distance)
    elif data == 's':
        return float(sita)
    else:
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

#TODO: xbeeでデータを送る関数
def xbee(s):
    return modules.xbee_send(s)

def goals_data():
    xbee("Please stand at goal")
    while 1:
        try:
            gps_data = gps()
            xbee(gps_data)
        except KeyboardInterrupt:
            return gps()

if __name__ == "__main__":
    main()
