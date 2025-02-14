from agents import GrassPatch, Sheep, Wolf
from model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.batchrunner import batch_run
import numpy as np

import matplotlib.pyplot as plt

x = np.arange(0.1, 0.6, 0.01)
y = [k for k in range(10,30)] 

simulator = ABMSimulator()

params = {
    "grass":True,
    "initial_sheep": 50,  # Différents nombres de moutons initiaux
    "initial_wolves": 1,   # Différents nombres de loups initiaux
    "grass_regrowth_time": y,
    "sheep_reproduce": x, 
    "wolf_reproduce": 0., 
    "wolf_gain_from_food": 1,
    "sheep_gain_from_food": 5,
    "simulator": simulator,
}

a = 1
# Configuration du BatchRunner
results = batch_run (
    WolfSheep,
    parameters=params,
    iterations=a,  # Nombre de répétitions pour chaque combinaison
    max_steps=100,  # Nombre maximal de pas de simulation
)

Z = np.zeros((len(x),len(y)))
for res in results:
    print(res["sheep_reproduce"], res["grass_regrowth_time"], res["DeathTime"])
    Z[int((res["sheep_reproduce"]*100 - 10)/5),int(res["grass_regrowth_time"])-1] += res["DeathTime"]/a

print(Z)

fig = plt.figure(figsize = (8,6))

ax = plt.axes(projection='3d')
ax.set_xlabel('Grass growth time', labelpad=50)
ax.set_ylabel('Sheep reproduction rate', labelpad=10)
ax.set_zlabel('Death time', labelpad=20)


X, Y = np.meshgrid(y, x)

surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

fig.colorbar(surf, shrink=0.5, aspect=8)
plt.show()
