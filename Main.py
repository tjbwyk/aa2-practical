from models.Field import Field
from models.Predator import Predator
from models.Prey import Prey
from models.State import *
from planner.SamplingBasedFittedValueIteration import SamplingBasedFittedValueIteration

demo_field = Field(width=10, height=10, state_type=DistanceState, planner_type=SamplingBasedFittedValueIteration)
#demo_field = Field(width=10, height=10, state_type=Distance2DState, planner_type=SamplingBasedFittedValueIteration)

demo_pred = Predator(demo_field, 0, 0)
demo_prey = Prey(demo_field, 5, 5)
demo_field.add_players(demo_pred, demo_prey)
demo_field.learn()
