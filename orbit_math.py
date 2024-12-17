import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы
F_thrust = 34e6  # Сила тяги (Н)
g = 9.81  # Ускорение свободного падения (м/с^2)
p0 = 101000  # Атмосферное давление у земли (Па)
M = 0.029  # Молярная масса воздуха (кг/моль)
R = 8.31  # Газовая постоянная (Дж/(моль·К))
alpha_target = np.radians(90)  # Целевой угол в радианах
t_max = 160  # Время достижения целевого угла (с)
S = 80.1  # Площадь поперечного сечения (м²)
Cf = 0.4
beta = 12900
m0 = 2970000
T = 300

t_eval = np.linspace(1, 160, 1000)


def equations(t, y):
    vx, vy, h, a = y
    m = m0 - beta * t
    alpha = np.radians(90) * np.exp(-(t / t_max))

    v = np.sqrt(vx**2 + vy**2)
    rho = ((p0 * M) / (R * T)) * np.exp(-((M * g) / (R * T)) * h)
    drag = (Cf * rho * S * v ** 2) / 2
    dvx_dt = (F_thrust * np.cos(alpha) - (drag * np.cos(alpha))) / m
    dvy_dt = (F_thrust * np.sin(alpha) - (drag * np.sin(alpha)) - m * g) / m

    return [dvx_dt, dvy_dt, vy, alpha]


y0 = [0, 0, 1, 90]

solution = solve_ivp(equations, [1, 160], y0, t_eval=t_eval)

vx = solution.y[0]
vy = solution.y[1]
h = solution.y[2]
v = np.sqrt(vx**2 + vy**2)
t = solution.t

alpha_deg = np.degrees(solution.y[3])

time_file = []
height_file = []
speed_file = []

with open("flight_log.txt", "r", encoding="UTF-8") as file:
    file.readline()
    for line in file:
        time, height, speed = list(map(float, line.strip().split(', ')))
        time_file.append(time)
        height_file.append(height)
        speed_file.append(speed)

# Построение графиков
plt.figure(figsize=(12, 10))

# График скорости
plt.subplot(3, 1, 1)
plt.plot(t, v, label="Скорость (моделирование)", color="red")
plt.plot(time_file, speed_file, label="Скорость (данные из файла)", linestyle="--", color="orange")
plt.title("Скорость ракеты от времени")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.grid()
plt.legend()

# График высоты
plt.subplot(3, 1, 2)
plt.plot(t, h, label="Высота (моделирование)", color="blue")
plt.plot(time_file, height_file, label="Высота (данные из файла)", linestyle="--", color="green")
plt.title("Высота ракеты от времени")
plt.xlabel("Время (с)")
plt.ylabel("Высота (м)")
plt.grid()
plt.legend()

# График угла наклона
plt.subplot(3, 1, 3)
plt.plot(t, alpha_deg, label="Угол наклона (градусы)", color="purple")
plt.title("Угол наклона ракеты от времени")
plt.xlabel("Время (с)")
plt.ylabel("Угол (градусы)")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
