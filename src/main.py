import modules
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.IN) 

CDS_PIN = 25

def main():
    while 1:
        gps_data = modules.GPS.Read_data()
        if GPIO.input(CDS_PIN): 
            deployment()

# --------------------------------------------


            
#TODO: サーボを使って展開するコードを書く
def deployment():

#TODO: 着地した後10m走ってGPSの差異をもとに計算するコードを書く
def calc_moment():

#TODO: モーターを動かすコードを書く
def move_motor():


if __name__ == "__main__":
    main()
