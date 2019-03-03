import serial
import time

def drop_mail():
    ser.write('d'.encode('utf-8'))
    time.sleep(1)

def flip_mail():
    ser.write('f'.encode('utf-8'))
    time.sleep(0.5)


if __name__ == "__main__":
    COM = '/dev/ttyACM0'
    baudRate = 9600
    
    ser = serial.Serial(COM, baudRate)
    time.sleep(5)
    drop_mail()
    flip_mail()

    ser.close()

