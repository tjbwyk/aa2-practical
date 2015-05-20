__author__ = 'kostas'
from Field import Field
from Predator import Predator
from Prey import Prey
from model.SamplingBasedFittedValueIteration import SamplingBasedFittedValueIteration
from State import *


forest = Field(11, 11)
d2_state = RelativeDistanceState(forest)
forest.set_state_type(d2_state)

tiger = Predator(0, 0, forest)
zebra = Prey(5, 5, forest)
policy = SamplingBasedFittedValueIteration()

forest.run()