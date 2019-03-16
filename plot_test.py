import matplotlib
import matplotlib.pyplot as plt

x = [1,2,3,4,5]
y = [1,4,9,16,25]
v = [2,2,2,2,2]

dataset = open('piranometro.csv','r')

for line in dataset:
    line = line.strip()
    IR,V,data = line.split(',')
    y.append(IR)
    v.append(V)
    x.append(data)

dataset.close()

plt.plot(x,y)
plt.xlabel('Tempo (s)')
plt.show()
