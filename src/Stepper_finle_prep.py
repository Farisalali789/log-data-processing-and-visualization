from functools import reduce
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as md

def checksum(data_line:str):
    checksum_value = data_line[data_line.rfind(',') + 1:]
    main_data = data_line[data_line.rfind(',')::-1]
    main_data = main_data[::-1]

    return checksum_value == hex(reduce(lambda x,y:x^y,map(ord,main_data)))



with open("stepper.log","r") as log:
    tsunix = []
    pos = []
    volt = []
    error_count = 0
    for idx, line in enumerate(log):
        line = line.strip()

        if idx == 0:
            continue
        elif line == "":
            continue

        elif not checksum(line):
            error_count+= 1
            print(f"Error at line -> {idx + 1}")

        else:
            line = line.split(',')
            tsunix.append(float(line[0]))
            pos.append(float(line[2]))
            volt.append(float(line[5]))


tsunix = np.array(tsunix)
pos = np.array(pos)
volt = np.array(volt)
moving_list_idx = []

print(volt)

for idx in range(len(pos) - 1):
    if pos[idx] - pos[idx + 1] != 0:
        moving_list_idx.append(idx)

print(moving_list_idx[0], moving_list_idx[-1])


tsdt = [datetime.fromtimestamp(x) for x in tsunix]

total_time = tsdt[-1] - tsdt[0]
print(total_time)

micro_steps_in_revolution = 64 * 256

circumference = 10 * np.pi

distance_per_micro_step_cm = circumference / micro_steps_in_revolution


dist = [distance_per_micro_step_cm * step for step in pos]

print(f"The total dist in is: {dist[-1] / 100:.3f} m")

for val1, val2 in zip(tsdt,dist):

    if val2 / 100 >= 20:
        print(f"The time is:{datetime.strftime(val1,'%H:%M:%S%f')}")
        break

with open("Output for stepper.csv",'w') as output:
    for dt, d in zip(tsdt,dist):
        print(f"{datetime.date(dt).strftime('%d-%m-%Y')},{datetime.time(dt)},{d /100}",file= output)

ave_volt = np.mean(volt)

x_values = [x for x in range(len(volt))]
coeffs = np.polyfit(x_values,volt,1)
volt_reg = np.polyval(coeffs,x_values)

plt.close()
plt.scatter(tsdt, volt / 1000, label= "volt", color= "blue", marker='+')
plt.plot(tsdt, volt_reg / 1000, label= "volt reg", color= "black")
plt.xlabel( "time")
plt.ylabel("volt")
plt.grid()
plt.legend()
plt.show()























