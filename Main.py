from Field import Field
from Predator import Predator
from Prey import Prey
from model.SamplingBasedFittedValueIteration import SamplingBasedFittedValueIteration
from State import *

W = 10
H = 10

demo_field = Field(W, H)
demo_pred = Predator(demo_field, 0, 0)
demo_prey = Prey(demo_field, 5, 5)
demo_field.add_players(demo_pred, demo_prey)

n_experiments_per_setting = 100
gammas = [0.8, 0.9]
n_states = [100, 500, 1000]
n_actions = [50, 75, 100]
n_targets = [1, 10, 50]
thresholds = [0.1, 0.01]
state_types = [Distance2DState(demo_field, demo_pred, demo_prey), DistanceState(demo_field, demo_pred, demo_prey)]


def experiment(state, gamma, ns, na, nt, thres):
    demo_planner = SamplingBasedFittedValueIteration(demo_field, gamma, ns, na, nt, thres)
    demo_field.set_state_type(state)
    demo_field.learn()
    res = demo_field.run_n_times(n_experiments_per_setting)
    print str(state.__class__.__name__) +\
        " gamma: %0.2f, #states: %d, #actions: %d, #targets: %d, threshold: %0.2f" % (gamma, ns, na, nt, thres)
    print "steps: %d, duration: %0.2f" % (res[0], res[1])
    return res


def f1():
    results = []
    for g in gammas:
        for s in n_states:
            for a in n_actions:
                for t in n_targets:
                    for th in thresholds:
                        for s_type in state_types:
                            result = experiment(s_type, g, s, a, t, th)
                            results.append((result, (s_type.__class__.__name__, g, s, a, t, th)))
                            demo_pred.x, demo_pred.y = 0, 0
                            demo_prey.x, demo_prey.y = 5, 5
    return results

