#!/usr/bin/env python3

"""SASampler
    This class is a sampler implementation of software simulated annealing.
"""

import math
import random

import numpy as np

# import matplotlib.pyplot as plt
from numba import f8, i8, b1
from numba.experimental import jitclass

from .samplermixin import SimulatorMixin

spec_sa = [
    ("matrix", f8[:, :]),
    ("sign_flag", b1),
    ("iteration", i8),
    ("inner_loop", i8),
    ("outer_loop", i8),
    ("temperature_decay", f8),
    ("temperature_start", f8),
]


class SA(SimulatorMixin):
    def sample(self, model, sign_flag=True, **params):
        self._set_model(model)
        self._set_params(**params)

        params = {
            "iteration": self.iteration,
            "inner_loop": self.inner_loop,
            "outer_loop": self.outer_loop,
            "temperature_decay": self.temperature_decay,
            "temperature_start": self.temperature_start,
        }

        if self.model_type == "ising":
            sa_sample = IsingSA(self.matrix, sign_flag, **params)
        else:
            sa_sample = QuboSA(self.matrix, sign_flag, **params)
        states = [tuple(state.tolist()) for state in sa_sample.sample()]

        params["temperature_end"] = self.temperature_end
        params["solver_name"] = "sa"
        response = {"states": states, "info": params}
        return self._make_sampleset(response, "sa", sign_flag)


@jitclass(spec_sa)
class IsingSA:
    def __init__(
        self,
        matrix,
        sign_flag,
        iteration,
        inner_loop,
        outer_loop,
        temperature_decay,
        temperature_start,
    ):
        self.matrix = matrix
        self.sign_flag = sign_flag
        self.iteration = iteration
        self.inner_loop = inner_loop
        self.outer_loop = outer_loop
        self.temperature_decay = temperature_decay
        self.temperature_start = temperature_start

    def sample(self,):
        return [self.run() for _ in range(self.iteration)]

    def run(self,):
        state_now = np.random.choice(np.array([-1, 1]), len(self.matrix))
        E_now = self._calc_energy(state_now)
        T = self.temperature_start
        for _ in range(self.outer_loop):
            for __ in range(self.inner_loop):
                state_now, E_now = self._update_state(state_now, E_now, T)
            T *= self.temperature_decay
        return state_now

    def _calc_energy(self, state):
        w = np.triu(self.matrix, k=1)
        b = np.diag(self.matrix)
        h = np.sum((w * state).T * state) + np.sum(b * state)
        return (2 * self.sign_flag - 1) * h

    def _update_state(self, state_now, E_now, T):
        state_new = self._change_state(state_now)
        E_new = self._calc_energy(state_new)
        if E_new < E_now:
            return state_new, E_new
        else:
            p = self._calculate_probability(E_new, E_now, T)
            if random.random() < p:
                return state_new, E_new
            else:
                return state_now, E_now

    def _change_state(self, state_now):
        state_new = state_now.copy()
        p = random.randint(0, len(state_now) - 1)
        state_new[p] = -state_now[p]
        return state_new

    def _calculate_probability(self, E_new, E_now, T):
        return math.exp(-abs(E_new - E_now) / T)


@jitclass(spec_sa)
class QuboSA:
    def __init__(
        self,
        matrix,
        sign_flag,
        iteration,
        inner_loop,
        outer_loop,
        temperature_decay,
        temperature_start,
    ):
        self.matrix = matrix
        self.sign_flag = sign_flag
        self.iteration = iteration
        self.inner_loop = inner_loop
        self.outer_loop = outer_loop
        self.temperature_decay = temperature_decay
        self.temperature_start = temperature_start

    def sample(self,):
        return [self.run() for _ in range(self.iteration)]

    def run(self,):
        state_now = np.random.choice(np.array([0, 1]), len(self.matrix))
        E_now = self._calc_energy(state_now)
        T = self.temperature_start
        for _ in range(self.outer_loop):
            for __ in range(self.inner_loop):
                state_now, E_now = self._update_state(state_now, E_now, T)
            T *= self.temperature_decay
        return state_now

    def _calc_energy(self, state):
        w = np.triu(self.matrix, k=1)
        b = np.diag(self.matrix)
        h = np.sum((w * state).T * state) + np.sum(b * state)
        return (2 * self.sign_flag - 1) * h

    def _update_state(self, state_now, E_now, T):
        state_new = self._change_state(state_now)
        E_new = self._calc_energy(state_new)
        if E_new < E_now:
            return state_new, E_new
        else:
            p = self._calculate_probability(E_new, E_now, T)
            if random.random() < p:
                return state_new, E_new
            else:
                return state_now, E_now

    def _change_state(self, state_now):
        state_new = state_now.copy()
        p = random.randint(0, len(state_now) - 1)
        state_new[p] = -state_new[p] + 1
        return state_new

    def _calculate_probability(self, E_new, E_now, T):
        return math.exp(-abs(E_new - E_now) / T)
