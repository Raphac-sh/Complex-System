# Introduction

This project has been conducted during the Complex Systems mini-course at ENS-Paris-Saclay.

The goal was to modelize a complex system, to perform batches and then analysing the results
to identify macroscopic behaviours emerging from the variation of parameters. The final 
results are condensed in a pdf report, which also presents the mathematical models involved.

# Codebase

We used the Python Mesa framework to modelize the system, tweeking the existing
example Wolf-Sheep predation model of the library. The project is separated in
different files :

- `agents.py` : Describes the different agents (Wolf, Sheep, Grass) as classes inheriting from the Agent class of Mesa
- `model.py` : Describes the global model and the interactions between agents.
- `app.py` : Launches the model with Solara vizualisation tool. 
- `batch.py` : Runs various simulations and generates 3D graphs of the results with matplotlib. 

To launch the code with vizualisation : `solara run app.py`
To launch bathces : `python3 batch.py`
