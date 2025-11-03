
import numpy as np
import matplotlib.pyplot as plt
import keyboard
###########################Функция досрочного прекращения симуляции##############
def STOP():
    global simulation
    simulation="N"
keyboard.add_hotkey("esc", STOP)
####################БЛОК ЗАДАНИЯ НАЧАЛЬНЫХ УСЛОВИЙ###################

# Количество шаров
n = 30
# Масса шаров
m1 =1 #int(input("m1= "))
m2 =2 #int(input("m2= "))
# Коэффициент упругости пружины
k = 1
# Расстояние между шарами(в состоянии покоя)
d = 1
# Длина пружины в нерастянутом состоянии
l_rest = d
# Временной шаг
dt = 0.1
# Время симуляции
t_max = 200
# Задаем отклонение из положения равновесия
x0 = 0.5
#Включение отображения симуляции "Y"-да, "N"-нет 
simulation="Y"
# Задаем положения шаров (координата Х равна номеру) и их скоростей(вначале 0)
x = list(range(0, n))
x_start=list(range(0, n))

v = np.zeros(n)

y=np.zeros(n)
# Задаем начальное отклонение какого-то шара 
otkl=2
x[otkl-1] =x[otkl-1]+x0

positions_left = np.zeros(int(t_max/dt)+1)
positions_right = np.zeros(int(t_max/dt)+1)
positions_middle = np.zeros(int(t_max/dt)+1)
time_counter=0

################## БЛОК РАСЧЕТА СИМУЛЯЦИИ ########################3
t = 0
a = np.zeros(n)#ачальные ускорения равны 0
while t < t_max:

    a[0]=-(k*(l_rest-abs(x[1]-x[0])))/m1

    for i in range(1, n-1):#считаем ускорение каждого шара
        if ((i%2)==1 or i==1):
            a[i]=-(k*(abs(x[i]-x[i-1])-l_rest)-k*(abs(x[i+1]-x[i])-l_rest))/m2
        else:
            a[i]=-(k*(abs(x[i]-x[i-1])-l_rest)-k*(abs(x[i+1]-x[i])-l_rest))/m1
    if ((n%2)==0):
        a[n-1]=-(k*(abs(x[n-1]-x[n-2])-l_rest))/m1
    else:
        a[n-1]=-(k*(abs(x[n-1]-x[n-2])-l_rest))/m2

    
    # рассчитываем новую скорость и новую координату
    v += a * dt
    x += v * dt
    y = x-x_start
    
    positions_left[time_counter]=x[n//2-1]
    positions_middle[time_counter]=x[n//2]
    positions_right[time_counter]=x[n//2+1]
    time_counter=time_counter+1
    
    #print(time_counter,"   ", x[5])
################БЛОК ВЫВДА НА ЭКРАН#######################

    if (simulation == "Y"):
        x1=x[range(0, n-1,2)]
        x2=x[range(1, n-1,2)] 
        plt.scatter(x1, np.zeros(len(x1)), color='blue',  label=f'm1= {m1}')
        plt.scatter(x2, np.zeros(len(x2)), color='green', label=f'm2= {m2}')
        plt.plot(y, color='red', label=f'Смещение')
        plt.plot(np.zeros(n+2), color='black', label=f'Ноль')
        plt.xlabel('Шары')
        plt.ylabel('Положение')
        plt.title(f'Время: {t:.2f}')

        #plt.xlim(-1, 11)
        #plt.ylim(-1, 1)
        #plt.xlim(n//2-20, n//2+20)
        #plt.ylim(-1, 1)

        plt.xlim(-1, n)
        plt.ylim(-1, 1)
        plt.draw()
        plt.legend(loc="upper right")
        plt.pause(0.01)
        plt.clf()
    
    
    t += dt# движимся дальше во времени
    
print('Количество шаров ='+str(n)
      +'\nМасса 1= '+str(m1)
      +'\nМасса 2= '+str(m2)
      +'\nКоэффициент жесткости = '+str(k)
      +'\nНачальное смещение шара № '
      +str(otkl)+'= '+str(x0)
      +'\nДлина недеформированной пружины= '+str(l_rest))
#plt.show()
#plt.figure(figsize=(12, 6))
plt.plot(np.arange(len(positions_left)-1) * dt, positions_left[:-1], label=f'Шар {n//2-1} (m2={m2})')
plt.plot(np.arange(len(positions_middle)-1) * dt, positions_middle[:-1], label=f'Шар {n//2}  (m1={m1})')
plt.plot(np.arange(len(positions_right)-1) * dt, positions_right[:-1], label=f'Шар {n//2+1} (m2={m2})')
plt.xlabel('Время')
plt.ylabel('смещение')
plt.title('Смещение среднего шара')
plt.legend()
plt.grid(True)
plt.show()
