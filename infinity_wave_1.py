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
n =60
# Масса шаров
m = 1
# Коэффициент упругости пружины
k = 1
# Расстояние между шарами(в состоянии покоя)
d = 1
# Длины пружины в нерастянутом состоянии
l_rest = d
# Временной шаг
dt = 0.2
# Время симуляции
t_max = 200
#Пауза между кадрами при отображении
dt_show=0.01

#Включение отображения симуляции "Y"-да, "N"-нет 
simulation="Y"
# Задаем положения шаров (координата Х равна номеру) и их скоростей(вначале 0)
x = list(range(0, n))#
x_start=list(range(0, n))#
v = np.zeros(n)#
y=np.zeros(n)#
#Задаем условия вынужденных колебаний 1ого шарика
A=0.3                    #Амлитуда

#запрещеная частота 
#W=1.5*sqrt(2*k/m)  #Угловая скорост
W=0.4*sqrt(2*k/m)

'''
#БЛОК УДАЛЕНИЯ КОНЦА ДЛЯ ОБЕСПЕЧЕНИЯ БЕГУЩЕЙ ВОЛНЫ  *В РАЗРАБОТКЕ*
Max="False"   #Служебная переменная для определения прохождения максимума
y_last=0.6*A  #
n_balls=20
'''
##################################################################################

positions_left = np.zeros(int(t_max/dt)+1)
positions_right = np.zeros(int(t_max/dt)+1)
positions_middle = np.zeros(int(t_max/dt)+1)
time_counter=0

################## БЛОК РАСЧЕТА СИМУЛЯЦИИ ########################3
t = 0
a = np.zeros(n)#начальные ускорения равны 0

print('Количество шаров= '+str(n)+'\nМасса= '+str(m)+'\nКоэффициент жесткости= '+str(k)+'\nДлина недеформированной пружины= '+str(l_rest))
while t < t_max:

    if (t<t_max): x[0] = A*cos(-W*t)
    else :a[0] = -(k * (l_rest-abs(x[1] - x[0]))) / m
    #a[0] = -(k * (l_rest-abs(x[1] - x[0]))) / m
    
    for i in range(1, n-1):#считаем ускорение каждого шара
        a[i] = -(k * (abs(x[i] - x[i-1]) - l_rest) - k * (abs(x[i+1] - x[i]) - l_rest)) / m
    a[n-1] = -(k * (abs(x[n-1] - x[n-2]) - l_rest)) / m
    
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
      
        plt.scatter(x, np.zeros(n), color='blue',  label=f'Шары')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.plot(y*10, color='red', label=f'Смещение')
        plt.plot(np.zeros(n+2), color='black', label=f'Ноль')
        plt.xlabel('Шары')
        plt.ylabel('Положение*10^(-1)')
        plt.title(f'Время: {t:.2f}')
        plt.xlim(-1, 50)
        plt.ylim(-5, 5)
        plt.grid(which='both')
        plt.legend(loc="upper right")
        plt.pause(dt_show)
        plt.draw()
        plt.clf()

        
    
    t += dt# движимся дальше во времени

plt.plot(np.arange(len(positions_left)-1) * dt, positions_left[:-1], label=f'Шар {49}')
plt.plot(np.arange(len(positions_middle)-1) * dt, positions_middle[:-1], label=f'Шар {50}')
plt.plot(np.arange(len(positions_right)-1) * dt, positions_right[:-1], label=f'Шар {51}')

plt.xlabel('Время')
plt.ylabel('Смещение')
plt.title('Смещение средних шаров')
plt.legend()
plt.grid(True)
plt.show()
