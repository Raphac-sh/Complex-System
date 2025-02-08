from agents import GrassPatch, Sheep, Wolf
from model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.batchrunner import batch_run
import numpy as np

import matplotlib.pyplot as plt

x = np.arange(0.04, 0.3, 0.01)
y = np.arange(0.04, 0.3, 0.01)

params = {
    "initial_sheep": 100,  # Différents nombres de moutons initiaux
    "initial_wolves": 5,   # Différents nombres de loups initiaux
    "grass_regrowth_time": 1,
    "sheep_reproduce": x, 
    "wolf_reproduce": y, 
    "wolf_gain_from_food": 20,
    "sheep_gain_from_food": 5,
    "simulator": ABMSimulator(),
}

a = 50
# Configuration du BatchRunner
results = batch_run (
    WolfSheep,
    parameters=params,
    iterations=a,  # Nombre de répétitions pour chaque combinaison
    max_steps=200,  # Nombre maximal de pas de simulation
)

Z = np.zeros((len(x),len(y)))
for res in results:
    print(res["sheep_reproduce"], res["wolf_reproduce"], res["DeathTime"])
    Z[int(res["sheep_reproduce"]*100-4),int(res["wolf_reproduce"]*100-4)] += res["DeathTime"]/a

print(Z)

fig = plt.figure(figsize = (8,6))

ax = plt.axes(projection='3d')
ax.set_xlabel('Wolf gain', labelpad=50)
ax.set_ylabel('Sheep gain', labelpad=10)
ax.set_zlabel('Death time', labelpad=20)


X, Y = np.meshgrid(x, y)

surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

fig.colorbar(surf, shrink=0.5, aspect=8)
plt.show()
