from tkinter.messagebox import RETRY
import serial
import os
import datetime

ser = serial.Serial(               #みちびき対応ＧＰＳ用の設定
  port = "/dev/serial0",           #シリアル通信を用いる
  baudrate = 9600,                 #baudレート
  parity = serial.PARITY_NONE,     #パリティ
  bytesize = serial.EIGHTBITS,     #データのビット数
  stopbits = serial.STOPBITS_ONE,  #ストップビット数
  timeout = None,                  #タイムアウト値
  xonxoff = 0,                     #ソフトウェアフロー制御
  rtscts = 0,                      #RTS/CTSフロー制御
  )

now = datetime.datetime.now()

def sixty_to_ten(x):
  ans = float(int(x) + ((x - int(x)))*100/60) 
  return ans

def Read_data():
        gps_data = ser.readline()  #1行ごとに読み込み、処理を繰り返す
        if not gps_data: 
            print("no data")  
    #GGA GPSセンサの位置情報を知る 
    #$GPGGA,UTC時刻,緯度,緯度の南北,経度,経度の東西,位置特定品質,使用衛星数,
    #水平精度低下率,海抜高さ,高さの単位,ジオイド高さ,高さの単位,DGPS,差動基準地点
        if (gps_data.startswith('$GPGGA')): #startswith:1行の先頭文字を検索する
            gpgga = (gps_data.split(",")) #split:1行をカンマで区切って変数にlist型で保存
            #緯度と経度の情報を、listからfloatに直す
            if gpgga[2]:
                lat_60,long_60,altitude = float(gpgga[2]),float(gpgga[4]),float(gpgga[9]) 
            else:
                lat_60,long_60,altitude = 0,0,0    #緯度の情報が無い
            #緯度と経度を60進法から10進法に変換、東経と北緯で計算
            if gpgga[3] == "W":  lat_60 *= -1
            if gpgga[5] == "S":  long_60 *= -1
            lat_10,long_10 = sixty_to_ten(lat_60/100),sixty_to_ten(long_60/100)
            #csv形式で出力する用のデータを変数にまとめて保存する(なければ０とする)
            alt_lat_long = "%3.2f,%5.6f,%5.6f" % (altitude,lat_10,long_10) if gpgga[9] else "0,0,0" #高度、緯度、経度
            ###############
            #GSA 特定タイプを見ることでGPSの通信状況を確認する
            #$GPGSA,UTC時刻,特定タイプ,衛星番号,精度低下率(位置、水平、垂直)
            #if (gps_data.startswith('$GPGSA')):  print gps_data, #特定タイプ(2D,3D等)を確認するために表示。3の時が良好。
            ###############
            #GSV 受信した衛星の位置等の情報を記録する
            #$GPGSV,UTC時刻,総センテンス数,このセンテンスの番号,総衛星数,
            #衛星番号,衛星仰角,衛星方位角,キャリア/ノイズ比,　を繰り返す
        if (gps_data.startswith('$GPGSV')):
            gpgsv = (gps_data.split(','))
            #衛星の個数を記録し、情報を追加する
        if (gpgsv[2] == '1'):
            num_sat = gpgsv[3]
            (gpgsv[1] + gpgsv[3] + '\n')
        #それぞれの衛星の番号、仰角、方位角を追加する
        if (len(gpgsv) == 4):  num_sat = '0'
        elif (len(gpgsv) >= 8):
            gsv1 =  gpgsv[4] + gpgsv[5] + gpgsv[6]   #センテンス中一つ目の衛星
        elif (len(gpgsv) >= 12):
            gsv2 =  gpgsv[8] + gpgsv[9] + gpgsv[10]  #二つ目の衛星
        elif (len(gpgsv) >= 16):
            gsv3 =  gpgsv[12] + gpgsv[13] + gpgsv[14]#三つ目の衛星
        elif (len(gpgsv) == 20):
            gsv4 =  gpgsv[16] + gpgsv[17] + gpgsv[18]#四つ目の衛星

        #############
        #ZDA NMEA出力における最後の行のため、時間を調べつつ一括ファイル出力する
        #$GPZDA,UTC時刻(hhmmss.mm),日,月,西暦,時,分,
        if (gps_data.startswith('$GPZDA')):
            gpzda = (gps_data.split(","))
            #GPSで取得したUTCの日付を保存する
            yyyymmddhhmmssff = datetime.datetime.strptime(gpzda[4] + '/' + gpzda[3] + '/' + gpzda[2] + ' ' + gpzda[1],"%Y/%m/%d %H%M%S.%f")    
            time_and_number = "%s,%s" % (yyyymmddhhmmssff,num_sat)
            return(time_and_number + ',' + alt_lat_long)

Rp = 6356.8 * 1000#[m] (地球の極半径)
Re = 6378.1 * 1000#[m] (地球の赤道半径)
pi = 3.141592

def GPS_xonly():
    gps_data = [Read_data()]
    x = 2 * pi * Re * (gps_data[-1] / 360)
    return x#[m]
    

def GPS_yonly():
    gps_data = [Read_data()]
    y = 2 * pi * Rp * (gps_data[-2] / 360)
    return y#[m]