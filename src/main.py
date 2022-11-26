import modules
import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
GPIO.setup(25, GPIO.IN)

CDS_PIN = 25               # CDSのピン番号

Rp = 6356.8 * 1000#[m] (地球の極半径)
Re = 6378.1 * 1000#[m] (地球の赤道半径)
pi = 3.141592

gps_start = [gps()]         #スタート地点のGPSの座標
gps_x0 = gps_start[-1]      #スタート地点のx座標
gps_y0 = gps_start[-2]      #スタート地点のy座標

def main():
    #TODO: 落下してからパラシュートを切り離すまでの動作
    while GPIO.input(CDS_PIN) >= 100:   #TODO: CDSが読み取る値　要検証
            deployment(90)
            break

    #TODO: ゴールするまでの動作
    while calc_moment(x = 2*pi*Re*(gps_x0 / 360) , y = 2*pi*Rp*(gps_y0 / 360) , data='d') < 10:
        move_motor(direc='fd' , duty=1.0 , time=1000)
        temp_gps = gps()
        xbee(temp_gps)

# --------------------------------------------


#TODO: サーボを使って展開するコードを書く
def deployment(angle):  #angle[°]だけサーボが回転する
    return modules.servo.role(angle)

#TODO: 2つの座補から角度と距離を返す関数
def calc_moment(
    x0 = modules.GPS.GPS_xonly(gps_data=gps_x0),    #GPSから取得した座標を読み取る
    y0 = modules.GPS.GPS_yonly(gps_data=gps_y0),
    x = modules.GPS.GPS_xonly(),                    #ゴールの座標
    y = modules.GPS.GPS_yonly(),
    data='a'
    ):
    #ゴールの方向を計算する
    distance_x = x - x0
    distance_y = y - y0
    distance = math.sqrt(distance_x**2 + distance_y**2)
    sita = math.atan(distance_y/distance_x)
    #dで距離、sで角度、初期値(a)で両方出力する
    if data == 'd':
        return float(distance)#[m]
    elif data == 's':
        return float(sita)
    else:
        return float(distance) , float(sita)

#TODO: モーターを動かすコードを書く
def move_motor(direc , duty , time):
    #f -> 前進
    if direc == 'f':
        return modules.DCmotor.foword(duty , time)
    #b -> 後進
    elif direc == 'b':
        return modules.DCmotor.back(duty , time)
    #r -> 右回転
    elif direc == 'r':
        return modules.DCmotor.right_role(duty , time)
    #l -> 左回転
    elif direc == 'l':
        return modules.DCmotor.left_role(duty ,time) 

#TODO: GPSを読み取る関数
def gps():
    #いちいちmodules.GPS.Read_data()って打つのめんどい
    return modules.GPS.Read_data()

#TODO: xbeeでデータを送る関数
def xbee(s):
    #いちいち打つのめんどい
    return modules.xbee_send(s)

#TODO: GPSを使ってゴール座標を取ってくる
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
