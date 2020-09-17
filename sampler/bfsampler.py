#!/usr/bin/env python3

"""BFSampler
    This class is a sampler implementation based on brute-force search.
"""

import sys

import numpy as np

# import matplotlib.pyplot as plt
from numba import f8, i8, b1
from numba.experimental import jitclass

from ..core import util
from .samplermixin import SimulatorMixin
# from ..response.sampleset import Sample
from ..sampleset import Sample


spec_bf = [
    ("matrix", f8[:, :]),
    ("sign_flag", b1),
    ("spins", i8),
    ("num", i8),
]


class BF(SimulatorMixin):
    def sample(self, model, sign_flag=True):
        self._set_model(model)

        if self.model_type == "ising":
            bf_sample = IsingBF(self.matrix, sign_flag)
        else:
            bf_sample = QuboBF(self.matrix, sign_flag)
        states = [tuple(state.tolist()) for state in bf_sample.sample()]
        params = {"solver_name": "bf"}
        response = {"states": states, "info": params}
        return self._make_sampleset(response, "bf", sign_flag)

    def sample_all(self, model, sign_flag=True):
        self._set_model(model)
        spins = len(self.matrix)
        all_num = 2 ** spins
        num = 0
        while num < all_num:
            state = self._make_state(num)
            i2l = util.get_index2label(self.label2index)
            l2i = {i2l[num]: value for num, value in enumerate(state)}
            yield Sample(l2i, self.model.energy(state, sign_flag), 1)
            num += 1

    def _make_state(self, num):
        spins = len(self.matrix)
        state = np.array([(num & (1 << i)) >> i for i in range(spins)])
        if self.model_type == "ising":
            return 2 * state - 1
        else:
            return state

    # def draw_eng(
    #     self,
    #     model,
    #     xlabel="States",
    #     ylabel="Energy of a model",
    #     name="",
    #     title="",
    #     figsize=(16, 12),
    #     fontsize=28,
    #     show=1,
    # ):
    #     fig = plt.figure(figsize=figsize)
    #     ax = fig.add_subplot(111)
    #     ax.set_xlabel(xlabel, fontsize=fontsize)
    #     ax.set_ylabel(ylabel, fontsize=fontsize)
    #
    #     plt.tick_params(labelbottom=False, bottom=False)
    #
    #     if title:
    #         ax.set_title(title)
    #
    #     num, eng_gen = self._all_s(model)
    #     ax.plot(range(num), list(eng_gen), linewidth=1)
    #
    #     if name:
    #         plt.savefig(name)
    #
    #     if show:
    #         plt.show()
    #     plt.close()


@jitclass(spec_bf)
class IsingBF:
    def __init__(self, matrix, sign_flag):
        self.matrix = matrix
        self.sign_flag = sign_flag
        self.spins = len(matrix)
        self.num = 2 ** self.spins

    def sample(self,):
        e_now = sys.maxsize
        num_now = [-1]
        for i in range(self.num):
            e_new = self._calc_energy(self._make_state(i))
            if e_new < e_now:
                e_now = e_new
                num_now = [i]
            elif e_new == e_now:
                num_now.append(i)
        return [self._make_state(i) for i in num_now]

    def _make_state(self, num):
        state = np.array([(num & (1 << i)) >> i for i in range(self.spins)])
        return 2 * state - 1

    def _calc_energy(self, state):
        w = np.triu(self.matrix, k=1)
        b = np.diag(self.matrix)
        h = np.sum((w * state).T * state) + np.sum(b * state)
        return (2 * self.sign_flag - 1) * h


@jitclass(spec_bf)
class QuboBF:
    def __init__(self, matrix, sign_flag):
        self.matrix = matrix
        self.sign_flag = sign_flag
        self.spins = len(matrix)
        self.num = 2 ** self.spins

    def sample(self,):
        e_now = sys.maxsize
        num_now = [-1]
        for i in range(self.num):
            e_new = self._calc_energy(self._make_state(i))
            if e_new < e_now:
                e_now = e_new
                num_now = [i]
            elif e_new == e_now:
                num_now.append(i)
        return [self._make_state(i) for i in num_now]

    def _make_state(self, num):
        state = np.array([(num & (1 << i)) >> i for i in range(self.spins)])
        return state

    def _calc_energy(self, state):
        w = np.triu(self.matrix, k=1)
        b = np.diag(self.matrix)
        h = np.sum((w * state).T * state) + np.sum(b * state)
        return (2 * self.sign_flag - 1) * h
