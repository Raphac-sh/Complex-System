import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Sheep(Agent):
    def step(self, model):
        self.move(model)
        if self.random.random() < 0.1:
            self.reproduce(model)

    def move(self, model):
        possible_steps = model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        model.grid.move_agent(self, new_position)

    def reproduce(self, model):
        if model.grid.is_cell_empty(self.pos):
            new_agent = Sheep(model.next_id(), model)
            model.grid.place_agent(new_agent, self.pos)
            model.schedule.add(new_agent)

class Wolf(Agent):
    def step(self, model):
        self.move(model)
        self.eat(model)
        if self.random.random() < 0.1:
            self.reproduce(model)

    def move(self, model):
        possible_steps = model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        model.grid.move_agent(self, new_position)

    def eat(self, model):
        cellmates = model.grid.get_cell_list_contents([self.pos])
        sheep = [agent for agent in cellmates if isinstance(agent, Sheep)]
        if sheep:
            sheep_to_eat = self.random.choice(sheep)
            model.grid.remove_agent(sheep_to_eat)
            model.schedule.remove(sheep_to_eat)

    def reproduce(self, model):
        if model.grid.is_cell_empty(self.pos):
            new_agent = Wolf(model.next_id(), model)
            model.grid.place_agent(new_agent, self.pos)
            model.schedule.add(new_agent)

class WolfSheepModel(Model):
    def __init__(self, width, height, initial_sheep, initial_wolves):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={"Sheep": lambda m: m.schedule.get_type_count(Sheep),
                             "Wolves": lambda m: m.schedule.get_type_count(Wolf)})

        for i in range(initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            sheep = Sheep(self.next_id(), self)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        for i in range(initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            wolf = Wolf(self.next_id(), self)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

def run_model(steps, width, height, initial_sheep, initial_wolves):
    model = WolfSheepModel(width, height, initial_sheep, initial_wolves)
    for i in range(steps):
        model.step()
    return model.datacollector.get_model_vars_dataframe()

def plot_phase_diagram(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Sheep'], data['Wolves'], label='Phase Diagram')
    plt.xlabel('Sheep Population')
    plt.ylabel('Wolf Population')
    plt.title('Wolf-Sheep Phase Diagram')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    steps = 100
    width = 20
    height = 20
    initial_sheep = 100
    initial_wolves = 50

    data = run_model(steps, width, height, initial_sheep, initial_wolves)
    plot_phase_diagram(data)
