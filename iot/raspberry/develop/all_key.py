"""
用法：直接运行即可
现象：见云端主函数
总结：做的事就是一直等云端发送数据，如果是发过来了'1'，表示开灯。同时按键也被检测着，一旦被按下则触发中断（另一个线程），灯也亮起。
"""

import RPi.GPIO as GPIO
import socket
import sys
import time
from sensor import SHT20
from threading import Thread

HOST = '124.223.76.58'  # 服务器的公网IP
PORT1 = 7789             # IP开放的socket端口
PORT2 = 8081
BUFSIZ = 1024           # socket缓冲区大小
ADDR1 = (HOST, PORT1)
ADDR2 = (HOST, PORT2)

FORNITURE_CONTROL = {'led_on':1,'led_off':0,'fun_on':3,'fun_off':2}
FORNITURE_CURREN_STATUS = {'led':0,'fun':0}
web_submit_status = FORNITURE_CONTROL['led_off']  # 网页端按下submit(选择了开灯)，则发送过来 '1'

# 初始化端口
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
LED = 27
FUN = 26
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(FUN, GPIO.OUT)
BUTTON_LED = 17                   # 后期换成传感器
GPIO.setup(BUTTON_LED, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # 引脚默认高电平（拉高），按下后接地引脚电平被拉低
GPIO.output(LED,GPIO.LOW)

def send_data_background(addr,delay_time):
    """
    Send furniture status and sensor data

    Arguments:
    addr         -  ('cloud_public_mac', PORT)
    delay_time   -  seconds between sending

    Plus:
    data structure - str((led_status , fun_status , temperature , humidity))
    """
    try:
        soc_bg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc_bg.connect(addr)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    sht = SHT20(1, 0x40)
    while(True):
        led_status   =  GPIO.input(LED) # 0/1
        fun_status   =  GPIO.input(FUN)
        temperature  =  sht.temperature().C
        humidity     =  sht.humidity().RH
        data = str((led_status , fun_status , temperature , humidity))
        soc_bg.send(data.encode('utf-8'))
        time.sleep(delay_time)



# 发送的数据格式：(device_id,time_from_rasp,led_status)，对应云端数据库
def send_data(forniture_name,time_from_rasp,forniture_status):
    data_send = str((forniture_name,time_from_rasp,forniture_status))  
    s.send(data_send.encode('utf-8'))


# 回调函数，按下按键的中断执行函数，现象为灯亮起且发送两次数据给云端
def led_button_callback(BUTTON_LED):
    """
    When the button is pressed, the current state of the LED is changed and the information is sent to the cloud
    """
    data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  raspberry'      # 当前时间
    print('按键按下')
    if GPIO.input(LED) == 1:
        send_data('led',data,0)           # 发送数据（状态为灭掉）
        GPIO.output(LED,GPIO.LOW)
    elif GPIO.input(LED) == 0:
        send_data('led',data,1)           # 发送数据（状态为亮起）
        GPIO.output(LED,GPIO.HIGH)
    else:
        pass

GPIO.add_event_detect(BUTTON_LED, GPIO.RISING, callback=led_button_callback, bouncetime=400)    # 检测BUTTON_LED的中断函数


if __name__ == '__main__':
    Thread(target = send_data_background,args=(ADDR2,5)).start()

    # 建立连接，建议不要做成函数（s需要是全局变量）
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR1)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    # 树莓派主函数就是接受云端是否发来开灯指令，所以需要一直接收着（后面扩展的话可以参考云端的index.py双线程）
    while(True):
        web_submit_status = int(s.recv(BUFSIZ).decode('utf-8'))   # 一直等着收，收着了才继续向下运行，云端发送过来的是'1'
        if(web_submit_status == FORNITURE_CONTROL['led_on'] ):
            data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            send_data('led',data,1)
            GPIO.output(LED,GPIO.HIGH)

        elif(web_submit_status == FORNITURE_CONTROL['led_off']):
            GPIO.output(LED,GPIO.LOW)
            data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            send_data('led',data,0)

        elif(web_submit_status == FORNITURE_CONTROL['fun_on']):
            GPIO.output(FUN,GPIO.HIGH)
            data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            send_data('fun',data,1)

        elif(web_submit_status == FORNITURE_CONTROL['fun_off']):
            GPIO.output(FUN,GPIO.LOW)
            data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            send_data('fun',data,0)

        else:
            pass
            