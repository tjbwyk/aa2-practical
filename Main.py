__author__ = 'kostas'
from Field import Field
from Predator import Predator
from Prey import Prey
from model.SamplingBasedFittedValueIteration import SamplingBasedFittedValueIteration
from State import *


forest = Field(10, 10)
d2_state = RelativeDistanceState(forest)
forest.set_state_type(d2_state)

tiger = Predator(0, 0, forest)
zebra = Prey(5, 5, forest)
policy = SamplingBasedFittedValueIteration(forest, forest.get_current_state())
policy.fit()
tiger.set_policy(policy)


forest.run()