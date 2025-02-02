from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.visualization import (
    SolaraViz,
    make_space_component,
)

from mesa.datacollection import DataCollector
import numpy as np
import random
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)

class Bee(Agent):
    def __init__(self, model, x, y):
        super().__init__(model)
        self.bee = True
        self.x = x
        self.y = y
        self.heading = random.uniform(0, 360)
        self.speed = 10.0

    def move(self):
        patch = self.model.get_patch(self.x, self.y)
        print(patch.chemical)
        self.heading += 6 * patch.chemical
        self.speed = 10 + (patch.chemical ** 2) / 60
        
        dx = np.cos(np.radians(self.heading)) * self.speed
        dy = np.sin(np.radians(self.heading)) * self.speed
        
        new_x = (self.x + dx) % self.model.width
        new_y = (self.y + dy) % self.model.height
        
        self.model.space.move_agent(self, (new_x, new_y))
        self.model.inc_patch(self.x,self.y,2)  # Drop chemical
        
    def step(self):
        self.move()

class Patch(Agent):
    def __init__(self, model, x, y):
        super().__init__(model)
        self.bee = False 
        self.x = x
        self.y = y
        self.chemical = 0

    def diffuse(self, patches, diffusion_rate=0.1):
        eps = [-1,1]
        for dx in eps:
            for dy in eps:
                patch = patches[(self.x + dx) % self.model.width, (self.y + dy) % self.model.height]
                patch.augment(patch.chemical*0.05)

    def evaporate(self, evaporation_rate=0.9):
        self.chemical *= evaporation_rate

    def augment(self, inc):
        self.chemical += inc

class BeeModel(Model):
    def __init__(self, num_bees=10, width=100, height=100, seed=None):
        super().__init__(seed=seed)
        self.num_bees = num_bees
        self.width = width
        self.height = height
        self.custom_agents = []
        self.space = ContinuousSpace(width, height, torus=True)
        
        self.patches = {(x, y): Patch(self, x, y) for x in range(width) for y in range(height)}
        
        for i in range(num_bees):
            x, y = random.uniform(0, width), random.uniform(0, height)
            bee = Bee(self, x, y)
            self.space.place_agent(bee, (x, y))
            self.custom_agents.append(bee)

    def get_patch(self, x, y):
        return self.patches[(int(x) % self.width, int(y) % self.height)]

    def inc_patch(self,x,y,inc):
        self.patches[(int(x) % self.width, int(y) % self.height)].augment(inc)

    def step(self):
        for patch in self.patches.values():
            patch.diffuse(self.patches)
            patch.evaporate()
        for bee in self.custom_agents:
            bee.move()

    def visualize(self):
        matrix = np.zeros((self.height, self.width))
        
        for (x, y), patch in self.patches.items():
            matrix[y, x] = patch.chemical
            
        print(matrix)

# Example run
model1 = BeeModel(num_bees=250, width=400, height=400)

def agent_portrayal(agent):
    return {
        "color": "red" if agent.bee else "grey",
        "marker": "s",
        "size": 5,
    }


def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


model_params = {
    "num_bees": {
        "type": "SliderInt",
        "value": 250,
        "min": 50,
        "max": 400,
        "label": "Number of bees",
    },
    "width": {
        "type": "SliderInt",
        "value": 400,
        "label": "Width",
        "min": 200,
        "max": 600,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 400,
        "label": "Height",
        "min": 200,
        "max": 600,
        "step": 1,
    },
}

# Create initial model instance

# Create visualization elements. The visualization elements are solara components
# that receive the model instance as a "prop" and display it in a certain way.
# Under the hood these are just classes that receive the model instance.
# You can also author your own visualization elements, which can also be functions
# that receive the model instance and return a valid solara component.
SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process, draw_grid=False
)


# Create the SolaraViz page. This will automatically create a server and display the
# visualization elements in a web browser.
# Display it using the following command in the example directory:
# solara run app.py
# It will automatically update and display any changes made to this file
page = SolaraViz(
    model1,
    components=[SpaceGraph],
    model_params=model_params,
    name="HoneyComb",
)
page  # noqa
