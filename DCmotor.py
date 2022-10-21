import pigpio
import time

IN1_1_PWM = 13  #right motor foword
IN1_2_PWM = 19  #right motor back
IN2_1_PWM = 18  #left motor foword
IN2_2_PWM = 12  #left motor back
duty = 0
dcm_pins = [IN1_1_PWM , IN1_2_PWM , IN2_1_PWM , IN2_2_PWM]


pi = pigpio.pi()

for pin in dcm_pins:
    pi.set_mode(pi , pigpio.OUTPUT)
    pi.write(pin , 0)

def foword(duty , pwm_time):
    #duty[μs] , time[s]
    t = (time.perf_counter() + pwm_time)
    while(True):
        pi.set_servo_pulsewidth(IN1_1_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN2_1_PWM , duty*1000)
        if(t == time.perf_counter()):
            break

def back(duty , pwm_time):
    t = (time.perf_counter() + pwm_time)
    while(True):
        pi.set_servo_pulsewidth(IN1_2_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN2_2_PWM , duty*1000)
        if(t == time.perf_counter()):
            break

def left_role(duty , pwm_time):
    t = (time.perf_counter() + pwm_time)
    while(True):
        pi.set_servo_pulsewidth(IN1_2_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN2_1_PWM , duty*1000)
        if(t == time.perf_counter()):
            break

def right_role(duty , pwm_time):
    t = (time.perf_counter() + pwm_time)
    while(True):
        pi.set_servo_pulsewidth(IN1_1_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN2_2_PWM , duty*1000)
        if(t == time.perf_counter()):
            break

def stop(duty , pwm_time):
    t = (time.perf_counter() + pwm_time)
    while(True):
        pi.set_servo_pulsewidth(IN1_1_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN1_2_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN2_1_PWM , duty*1000)
        pi.set_servo_pulsewidth(IN2_2_PWM , duty*1000)
        if(t == time.perf_counter()):
            break