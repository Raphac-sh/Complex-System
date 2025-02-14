from agents import GrassPatch, Sheep, Wolf
from model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.batchrunner import batch_run
import numpy as np

import matplotlib.pyplot as plt

x = [k for k in range(1,10)]
y = [k for k in range(1,50)] 

simulator = ABMSimulator()

params = {
    "grass":True,
    "initial_sheep": 100,  # Différents nombres de moutons initiaux
    "initial_wolves": 5,   # Différents nombres de loups initiaux
    "grass_regrowth_time": 25,
    "sheep_reproduce": 0.04, 
    "wolf_reproduce": 0.05, 
    "wolf_gain_from_food": y,
    "sheep_gain_from_food": x,
    "simulator": simulator,
}

a = 10 
# Configuration du BatchRunner
results = batch_run (
    WolfSheep,
    parameters=params,
    iterations=a,  # Nombre de répétitions pour chaque combinaison
    max_steps=100,  # Nombre maximal de pas de simulation
)

Z = np.zeros((len(x),len(y)))
for res in results:
    Z[int(res["sheep_gain_from_food"]-1),int(res["wolf_gain_from_food"]-1)] += res["DeathTime"]/a

print(Z)

fig = plt.figure(figsize = (8,6))

ax = plt.axes(projection='3d')
ax.set_xlabel('Sheep gain from food', labelpad=50)
ax.set_ylabel('Wolf gain from food', labelpad=10)
ax.set_zlabel('Death time', labelpad=20)


X, Y = np.meshgrid(y, x)

surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

fig.colorbar(surf, shrink=0.5, aspect=8)
plt.show()
