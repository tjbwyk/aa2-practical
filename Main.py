from models.Field import Field
from models.Predator import Predator
from models.Prey import Prey
from models.State import *
from planner.SamplingBasedFittedValueIteration import SamplingBasedFittedValueIteration

def experiment(field, pred, prey, statetype, gamma, ns, na, nt, thres):
    field.set_state_type(statetype)
    field.add_players(pred, prey)
    field.set_planner_type(SamplingBasedFittedValueIteration)
    field.set_planner(field, gamma, ns, na, nt, thres)
    field.learn()
    res = field.run_n_times(n_experiments_per_setting)
    print statetype.__name__ +\
        " gamma: %0.2f, #states: %d, #actions: %d, #targets: %d, threshold: %0.3f" % (gamma, ns, na, nt, thres)
    print "steps: %d, duration: %0.2f" % (res[0], res[1])
    return res

if __name__ == "__main__":
    W = 10
    H = 10

    demo_field = Field(width=10, height=10)

    demo_pred = Predator(demo_field, 0, 0)
    demo_prey = Prey(demo_field, 5, 5)

    n_experiments_per_setting = 100
    gammas = [0.5, 0.9]
    n_states = [100, 500, 1000]
    n_actions = [10, 50, 100]
    n_targets = [1, 10, 50]
    thresholds = [0.1, 0.01, 0.001]
    # gammas = [0.9]
    # n_states = [100]
    # n_actions = [10]
    # n_targets = [10]
    # thresholds = [0.1]
    state_types = [Distance2DState, DistanceState]

    results = []
    for g in gammas:
        for s in n_states:
            for a in n_actions:
                for t in n_targets:
                    for th in thresholds:
                        for s_type in state_types:
                            result = experiment(demo_field, demo_pred, demo_prey, s_type, g, s, a, t, th)
                            results.append((result, (s_type.__name__, g, s, a, t, th)))
                            demo_pred.x, demo_pred.y = 0, 0
                            demo_prey.x, demo_prey.y = 5, 5
    print results
