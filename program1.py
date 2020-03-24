import numpy as np
import math
import copy
from frozenlake import FrozenLakeEnv
from plot_utils import plot_values

env = FrozenLakeEnv(is_slippery=True)

def policy_evaluation(env, policy, gamma=1, theta=1e-8):
    V = np.zeros(env.nS)
    while True:
        delta = 0
        for s in range(env.nS):
            Vs = 0
            for a, action_prob in enumerate(policy[s]):
                for prob, next_state, reward, _ in env.P[s][a]:
                    Vs += action_prob * prob * (reward + gamma * V[next_state])
            delta = max(delta, np.abs(V[s] - Vs))
            V[s] = Vs
        if delta < theta:
            break
    return V

def q_from_v(env, V, s, gamma=1):
    q = np.zeros(env.nA)
    for a in range(env.nA):
        for prob, next_state, reward, done in env.P[s][a]:
            q[a] += prob * (reward + gamma * V[next_state])
    return q

def policy_improvement(env, V, gamma=1):
    policy = np.ones([env.nS, env.nA]) / env.nA
    for s in range(env.nS):
        q = q_from_v(env, V, s, gamma)
        #stochastic policy:
        best_a = np.argwhere(q==np.max(q)).flatten()
        policy[s] = np.sum([np.eye(env.nA)[i] for i in best_a], axis=0)/len(best_a)
    return policy

def policy_iteration_soln(env, gamma=0.9, theta=1e-8):
    policy = np.ones([env.nS, env.nA]) / env.nA
    while True:
        V = policy_evaluation(env, policy, gamma, theta)
        new_policy = policy_improvement(env, V)
        if (new_policy == policy).all():
            break;
        policy = copy.copy(new_policy)
    return policy, V



if __name__ == "__main__":
    policy = np.ones([env.nS, env.nA]) / env.nA
    V = policy_evaluation(env, policy, gamma=0.9, theta=1e-8)
    Q = np.zeros([env.nS, env.nA])
    for s in range(env.nS):
        Q[s] = q_from_v(env, V, s, gamma=0.9)
    policy_pi, V_pi = policy_iteration_soln(env)
    print("\nOptimal Policy (LEFT = 0, DOWN = 1, RIGHT = 2, UP = 3):")
    print(policy_pi,"\n")
    plot_values(V_pi)












