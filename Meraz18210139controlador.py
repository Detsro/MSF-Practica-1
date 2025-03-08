"""
Práctica 1: Diseño de controlador para un sistema de segundo orden

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Mauricio Jesus Meraz Galeana
Número de control: 18210139
Correo institucional: mauricio.meraz18@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m 
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tF, dt, w, h = 0, 0, 10, 1E-3, 6, 3 
N = round((tF-t0)/dt) + 1 
t = np.linspace(t0, tF, N)
u1 = np.ones(N) # Escalón unitario
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 # Impulso
u3 = (np.linspace(t0, tF, N)) / tF # Rampa
u4 = np.sin(m.pi/2 * t) # Función sinusoidal, 1.5708 rad/s = 250 mHz
u = np.stack((u1, u2, u3, u4), axis=1)
signal = ['Escalon', 'Impulso', 'Rampa', 'Sin']

# Componentes del circuito RLC y función de transferencia
R = 100E3
L = 1E-3
C = 1E-6
num = [C*L*R,C*R**2+L,R]
den = [3*C*L*R,5*C*R**2+L,2*R]
sys = ctrl.tf(num, den)
print(sys)


#componentes del controlador
Cr = 1E-6
kI = 1530.1556
Re = 1/(kI*Cr); print('Re=',Re)
numPID = [1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(PID)
# Sistema de control en lazo cerrado
X = ctrl.series(PID,sys)
sysPID = ctrl.feedback(X,1, sign = -1)
print(sysPID)

# Respuesta al escalon unitario
fig1 = plt.figure();
plt.plot(t,u1,'-', color = [0.5,0.03,0.02], label = 'Ve(t)')
_,Vs = ctrl. forced_response(sys,t,u1,x0)
plt.plot(t,Vs,'-', color = [0.1,0.05,0.02], label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u1,x0)
plt.plot(t,VPID,':', linewidth = 3 , color = [0.4,0.05,0.06], label = 'VPID(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.3,0.1))
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('V_i [t] [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 8,frameon = False)
plt.show()
fig1.savefig('step.pdf', bbox_inches = 'tight')

# Respuesta impulso
fig1 = plt.figure();
plt.plot(t,u2,'-', color = [0.5,0.03,0.02], label = 'Ve(t)')
_,Vs = ctrl. forced_response(sys,t,u2,x0)
plt.plot(t,Vs,'-', color = [0.1,0.05,0.02], label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u2,x0)
plt.plot(t,VPID,':', linewidth = 3 , color = [0.4,0.05,0.06], label = 'VPID(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.3,0.1))
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('V_i [t] [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 8,frameon = False)
plt.show()
fig1.savefig('impulse.pdf', bbox_inches = 'tight')
# Respuesta Rampa
fig1 = plt.figure();
plt.plot(t,u3,'-', color = [0.5,0.03,0.02], label = 'Ve(t)')
_,Vs = ctrl. forced_response(sys,t,u3,x0)
plt.plot(t,Vs,'-', color = [0.1,0.05,0.02], label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u3,x0)
plt.plot(t,VPID,':', linewidth = 3 , color = [0.4,0.05,0.06], label = 'VPID(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.3,0.1))
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('V_i [t] [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 8,frameon = False)
plt.show()
fig1.savefig('ramp.pdf', bbox_inches = 'tight')
# Respuesta Sinusoidal
fig1 = plt.figure();
plt.plot(t,u4,'-', color = [0.5,0.03,0.02], label = 'Ve(t)')
_,Vs = ctrl. forced_response(sys,t,u4,x0)
plt.plot(t,Vs,'-', color = [0.1,0.05,0.02], label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u4,x0)
plt.plot(t,VPID,':', linewidth = 3 , color = [0.4,0.05,0.06], label = 'VPID(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(-1,1); plt.yticks(np.arange(-1,1.2,0.1))
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('V_i [t] [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc = 'center', ncol = 3,
           fontsize = 8,frameon = False)
plt.show()
fig1.savefig('sinusoidal.pdf', bbox_inches = 'tight')

