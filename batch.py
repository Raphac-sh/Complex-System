from agents import GrassPatch, Sheep, Wolf
from model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.batchrunner import batch_run

import matplotlib.pyplot as plt

params = {
    "initial_sheep": 150,  # Différents nombres de moutons initiaux
    "initial_wolves": 10,   # Différents nombres de loups initiaux
    "grass_regrowth_time": 30,
    "sheep_reproduce": 0.04,
    "wolf_reproduce": 0.05,
    "wolf_gain_from_food": range(1,20),
    "sheep_gain_from_food": range(1,20),
    "simulator": ABMSimulator(),
}

a = 1
# Configuration du BatchRunner
results = batch_run (
    WolfSheep,
    parameters=params,
    iterations=a,  # Nombre de répétitions pour chaque combinaison
    max_steps=200,  # Nombre maximal de pas de simulation
)

ax = plt.axes(projection='3d')
for res in results:
    print("Wolf gain", res["wolf_gain_from_food"], "Sheep gain", res["sheep_gain_from_food"], "Wolf remaining", res["Wolves"], "Sheep remaining", res["Sheep"], res["DeathTime"])
    ax.plot(res["wolf_gain_from_food"], res["sheep_gain_from_food"], res["DeathTime"],marker="o", color="red")

ax.set_xlabel('Wolf gain', labelpad=20)
ax.set_ylabel('Sheep gain', labelpad=20)
ax.set_zlabel('Death time', labelpad=20)

plt.show()
