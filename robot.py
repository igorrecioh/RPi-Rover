#!/usr/bin/env python
try:
	import RPi.GPIO as GPIO

except RuntimeError:
	print("Error al importar RPi.GPIO! Ejecutame como root usando sudo!")

import sys, tty, termios 

#funcion para obtener caracteres del teclado
def getch() :
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
finally:
	termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
return ch

# Motor PINs - Por definir -
MOTOR1A = ?? #izquierda
MOTOR1B = ?? 
MOTOR2A = ?? #derecha
MOTOR2B = ?? 

#Frecuencia del PWM
PWM_FREQ = 50 #50hz

#
GPIO.setmode(GPIO.BCM)

#Ciclo de trabajo del PWM (maximo 100)
speed = 50

#(motor1, motor2)
# 0 = parar motor, 1 = motor1 hacia delante, 2 = motor2 hacia atras

direction = {
	#Teclas
	'x' : (2, 2), #Marcha atras
	'a' : (1, 2), #Derecha
	's' : (0, 0), #Stop
	'd' : (2, 1), #Izquierda
	'w' : (1, 1), #Adelante
}

current_direction = (0, 0)

#Configuración como salidas
GPIO.setup(MOTOR1A, GPIO.OUT)
GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR2A, GPIO.OUT)
GPIO.setup(MOTOR2B, GPIO.OUT)

#Configuración como PWM
pin1A = GPIO.PWM(MOTOR1A, PWM_FREQ)
pin1B = GPIO.PWM(MOTOR1B, PWM_FREQ)
pin2A = GPIO.PWM(MOTOR2A, PWM_FREQ)
pin2B = GPIO.PWM(MOTOR2B, PWM_FREQ)

#Iniciar PWM
pin1A.start (0)
pin1B.start (0)
pin2A.start (0)
pin2B.start (0)

while True:
	## Motor 1
	#Adelante
	if current_direction[0] == 1 :
		pin1B.ChangeDutyCycle(0)
		pin1A.ChangeDutyCycle(speed)
	#Atras
	elif current_direction[0] == 2 :
		pin1A.ChangeDutyCycle(0)
		pin1B.ChangeDutyCycle(speed)
	#Parar
	else :
		pin1A.ChangeDutyCycle(0)
		pin1B.ChangeDutyCycle(0)
	## Motor 2
	#Adelante
	if current_direction[1] == 1 :
		pin2B.ChangeDutyCycle(0)
		pin2A.ChangeDutyCycle(speed)
	#Atras
	elif current_direction[1] == 2 :
		pin2A.ChangeDutyCycle(0)
		pin2B.ChangeDutyCycle(speed)
	#Parar
	else :
		pin2A.ChangeDutyCycle(0)
		pin2B.ChangeDutyCycle(0) 

	#Siguiente caracter
	ch = getch()

	# q = salir de la app
	if (ch == 'q') :
		break

	elif (ch in direction.keys()) :
		current_direction = direction[ch]
		print "Direccion "+str(current_direction[0])+str(current_direction[1])+"\n"

#Parar y limpiar PWM
pin1A.stop()
pin1B.stop()
pin2A.stop()
pin1B.stop()
GPIO.cleanup()