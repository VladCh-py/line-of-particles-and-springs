import numpy as np
import matplotlib.pyplot as plt
from math import * 
import keyboard
###########################Функция досрочного прекращения симуляции##############

def STOP():
    global simulation
    simulation="N"
keyboard.add_hotkey("esc", STOP)
########################БЛОК ЗАДАНИЯ НАЧАЛЬНЫХ УСЛОВИЙ############################

# Количество шаров
n = 500
# Масса шаров
Mode= int(input("Режим (1- в одной фазе; 2- в противофазе): "))
# m1 = int(input("m1= "))
# m2 = int(input("m2= "))

# m1 = 1.1#одна фаза
# m2 = 1

m1 = 1.5
m2 = 1

# Коэффициент упругости пружины
k = 1
# Расстояние между шарами(в состоянии покоя)
d = 1
# Длины пружины в нерастянутом состоянии
l_rest = d
# Временной шаг
dt = 0.2
# Время симуляции
t_max = 300
#Пауза между кадрами при отображении
dt_show=0.01

#Включение отображения симуляции "Y"-да, "N"-нет 
simulation="Y"
# Задаем положения шаров (координата Х равна номеру) и их скоростей(вначале 0)
x = list(range(0, n))#
x_start=list(range(0, n))#
v = np.zeros(n)#
y=np.zeros(n)#

# Задаем отклонение из положения равновесия
x0 = 0
# Задаем начальное отклонение какого-то шара 
otkl=2
x[otkl-1] =x[otkl-1]+ x0
x_start[otkl-1] =x[otkl-1]-x0
'''
x[7] =x[7]+ x0
x[15] =x[15]+ x0
x[20] =x[20]+ x0
x[40] =x[40]+ x0
'''
#Задаем условия вынужденных колебаний 1ого шарика
if Mode == 1:
    A=0.4                        #Амлитуда
    koeff=0.4               #коэффициент
    W=koeff*sqrt(2*k*(1/m1+1/m2))  #Угловая скорость
else:
    A=0.2                        #Амлитуда
    koeff=0.9              #коэффициент
    W=koeff*sqrt(2*k*(1/m1+1/m2))  #Угловая скорость   

#пограничная зона
# A=0.1                        #Амлитуда
# koeff=0.59 #0.85 #m1/m2=2            #коэффициент/m
# W=koeff*sqrt(2*k*(1/m1+1/m2))  #Угловая ско=рость 

#запрещеная зона
A=0.3                       #Амлитуда
koeff=0.7            #коэффициент/m
W=koeff*sqrt(2*k*(1/m1+1/m2))  #Угловая ско=рость 

##################################################################################

positions_left = np.zeros(int(t_max/dt)+1)
positions_right = np.zeros(int(t_max/dt)+1)
positions_middle = np.zeros(int(t_max/dt)+1)
time_counter=0

################## БЛОК РАСЧЕТА СИМУЛЯЦИИ ########################3
t = 0
a = np.zeros(n)#начальные ускорения равны 0

print('Количество шаров= '+str(n)+'\nМасса 1= '+str(m1)
      +'\nМасса 2= '+str(m2)
      +'\nКоэффициент жесткости= '
      +str(k)
      
      #+'\nНачальное смещение шара № '
      #+str(otkl)+'= '+str(x0)
      
      +'\nДлина недеформированной пружины= '+str(l_rest))

while t < t_max:

    if (t<t_max): x[0] = A*cos(-W*t)
    #else :a[0] = -(k * (l_rest-abs(x[1] - x[0]))) / m
    #a[0] = -(k * (l_rest-abs(x[1] - x[0]))) / m
    
    for i in range(1, n-1):#считаем ускорение каждого шара
        if ((i%2)==1 or i==1):
            a[i] = -(k * (abs(x[i] - x[i-1]) - l_rest) - k * (abs(x[i+1] - x[i]) - l_rest)) / m2
        else:
            a[i] = -(k * (abs(x[i] - x[i-1]) - l_rest) - k * (abs(x[i+1] - x[i]) - l_rest)) / m1
    if ((n%2)==0):
        a[n-1] = -(k * (abs(x[n-1] - x[n-2]) - l_rest)) / m1
    else:
        a[n-1] = -(k * (abs(x[n-1] - x[n-2]) - l_rest)) / m2

    
    # рассчитываем новую скорость и новую координату
    v += a * dt
    x += v * dt
    y = x-x_start
    positions_left[time_counter]=x[49]
    positions_middle[time_counter]=x[50]
    positions_right[time_counter]=x[51]
    time_counter=time_counter+1
    
    #print(time_counter,"   ", x[5])
    
################БЛОК ВЫВДА НА ЭКРАН#######################
    if (simulation == "Y"):
      
        x1=x[::2]
        x2=x[1::2]
        plt.scatter(x1, np.zeros(len(x1)), color='blue',  label=f'm1= {m1}')
        plt.scatter(x2, np.zeros(len(x2)), color='red', label=f'm2= {m2}')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.plot(y[::2]*10, color='blue', label=f'Смещение m1')
        plt.plot(y[1::2]*10, color='red', label=f'Смещение m2')
        plt.plot(np.zeros(n+2), color='black', label=f'Ноль')
        plt.xlabel('Шары')
        plt.ylabel('Положение*10^(-1)')
        plt.title(f'Время: {t:.2f}')
        plt.xlim(-1, 20)
        plt.ylim(-5, 5)
        plt.grid(which='both')
        plt.legend(loc="upper right")
        plt.pause(dt_show)
        plt.draw()
        plt.clf()

        
    
    t += dt# движимся дальше во времени
    
#['Ball '+str(n//2+1),'Ball '+str(n//2), 'Ball '+str(n//2-1), str(n), str(k), str(x0)])
plt.plot(np.arange(len(positions_left)-1) * dt, positions_left[:-1], label=f'Шар {49} (m2={m2})')
plt.plot(np.arange(len(positions_middle)-1) * dt, positions_middle[:-1], label=f'Шар {50} (m1={m1})')
plt.plot(np.arange(len(positions_right)-1) * dt, positions_right[:-1], label=f'Шар {51} (m2={m2})')

plt.xlabel('Время')
plt.ylabel('Смещение')
plt.title('Смещение средних шаров')
plt.legend()
plt.grid(True)
plt.show()
