from flask import Flask, render_template, request
import math
import Adafruit_PCA9685

#Aktiviert den Spannungsumsetzer vor dem PCA9685
import RPi.GPIO as GPIO


app = Flask(__name__)

home_positions = [ ("j1", 0, 90/180.0 * math.pi), ("j2", 3, 90.0/180.0 * math.pi), ("j3", 4, 90.0/180.0*math.pi), ("j4", 7, 90.0/180.0 * math.pi) ]

def find_joint( jname, joints ):
    ret = None
    for j in joints:
        if jname == j[0]:
           ret = j
           break
    return ret
    
@app.route('/')
def hello_world():
    title = "Raspberry Pi Ball Balancer"
    return render_template("main.html", title = title )

@app.route('/joints', methods=['GET', 'PUT'])
def joints( ):
    j1 = request.args['j1']
    j2 = request.args['j2']
    j3 = request.args['j3']
    j4 = request.args['j4']

    j1 = float(j1) 
    j2 = float(j2) 
    j3 = float(j3) 
    j4 = float(j4) 
    
    print(f"Setting joints: j1 = {j1}, deg. {j1/math.pi * 180.0}")
    print(f"Setting joints: j2 = {j2}, deg.{j2/math.pi * 180.0}")
    print(f"Setting joints: j3 = {j3}, {j3/math.pi * 180.0}")
    print(f"Setting joints: j4 = {j4}, {j4/math.pi * 180.0}")

    joints = [j1, j2, j3, j4]
    for i,jname in enumerate([ "j1", "j2", "j3", "j4" ]):
        joint = find_joint( jname, home_positions )
        if joint:
    	    joints[i] = normalize_angle(joints[i] + joint[2])
    
    j1, j2, j3, j4 = joints
    	
    print(f"Setting joints: j1 = {j1/math.pi * 180.0}")
    print(f"Setting joints: j2 = {j2/math.pi * 180.0}")
    print(f"Setting joints: j3 = {j3/math.pi * 180.0}")
    print(f"Setting joints: j4 = {j4/math.pi * 180.0}")

    for i,h in enumerate(home_positions):
        jname, joint, home = h
                
        val = convert_angle_to_pwm( joints[i] )
        if val is not None:        
            set_servo_pulse( pwm, joint, val )
            
    return f"Ok"

@app.route('/test/<param>', methods=['GET', 'POST'])
def test( param ):
    print("/test received param", param)
    return "ok"

# Einstellen der Minimal- und Maximal-Pulslaengen
servo_min = 150  # Minimale Pulslaenge
servo_max = 600  # Maximale Pulslaenge

# Hilfsfunktion
def set_servo_pulse(pwm, channel, pulse):
    pulse_length = 1000000 
    pulse_length /= 50     
    print('{0}us per period'.format(pulse_length))
    pulse_length /= 4096     
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    print(pulse_length)
    pulse /= pulse_length
    print(pulse)
    pulse = round(pulse)
    print(pulse)
    pulse = int(pulse)
    print (pulse)
    pwm.set_pwm(channel, 0, pulse-25)

def normalize_angle( angle ):
    while(angle < 0):
        angle = angle + 2 * math.pi
    while(angle > 2 * math.pi):
        angle = angle - 2 * math.pi
    return angle
        
def convert_angle_to_pwm( angle ):
    ret = None
    angle = normalize_angle( angle )
    if angle >= 0.0 and angle < 2 * math.pi:
        p_width = 650 #600 - 150
        pulse = 0 + angle/(2*math.pi)*p_width
        ret = pulse
    return ret

pwm = Adafruit_PCA9685.PCA9685(address=0x41)

def create_app():
    print("setting up GPIO pin")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH)
    # Initalisierung mit alternativer Adresse
    print("Initialize Adafruit")
    
    # Frequenz auf 50Hz setzen
    pwm.set_pwm_freq(50) #50 or 100

    for h in home_positions:
        jname, joint, home = h        
        val = convert_angle_to_pwm( home )
        if val is not None:        
            set_servo_pulse( pwm, joint, home )
            
    app.run( host="0.0.0.0", port=8080 )

if __name__ == "__main__":
    create_app()


