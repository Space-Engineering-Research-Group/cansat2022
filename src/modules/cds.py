#必要なモジュールをインポート
import spidev                       #SPI通信用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

#SPI通信を行うための準備
spi = spidev.SpiDev()               #インスタンスを生成
spi.open(0, 0)                      #CE0(24番ピン)を指定
spi.max_speed_hz = 1000000          #転送速度 1MHz

def read():
    resp = spi.xfer2([0x68, 0x00])                  #SPI通信で値を読み込む
    volume = ((resp[0] << 8) + resp[1]) & 0x3FF     #読み込んだ値を10ビットの数値に変換
    time.sleep(1)                                   #1秒間待つ
    if volume <= 200:                                   
        spi.close()                                 #SPI通信を終了
        sys.exit()                                  #プログラム終了

    return volume                                   #変換した値を表示