import consoleplayer
from scores import combinations, comb, score_hand, hand_values, df

from functools import lru_cache as cache
import pandas as pd
from IPython import get_ipython
import itertools
from statistics import mean
from numba import jit, vectorize
import timeit
import numpy as np
from itertools import permutations
from numpy import vectorize
import random

maxi, overallMean = 0, 0
c3, c4 = [], []


@jit(nopython=True)
def common(a, b):
    l1 = [i for i in a]
    l2 = [i for i in b]
    commonList = len([i for i in l1 if i in l2])
    return commonList


@jit(nopython=True)
def numba_4():
    results = []
    len1 = c4.shape[0]
    len2 = comb.shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c4[i], comb[j]) == 4:
                results.append(comb[j])
    return results


@jit(nopython=True)
def numba_3():
    results = []
    len1 = c3.shape[0]
    len2 = comb.shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c3[i], comb[j]) == 4:
                results.append(comb[j])
    return results


@cache(maxsize=None)
def opti_3():
    values = numba_3()
    return [score_hand(i) for i in values]


@cache(maxsize=None)
def opti_4():
    values = numba_4()
    return [score_hand(i) for i in values]


def expected_value(hand, comb):
    global maxi, overallMean
    if len(hand) == 5:
        maxi = score_hand(hand)
        overallMean = np.mean(opti_3() + opti_4())
    elif len(hand) == 6:
        maxi = max([score_hand(i) for i in combinations(hand, 5)])
        overallMean = np.mean(opti_4())
    elif len(hand) == 7:
        maxi = max([score_hand(i) for i in combinations(hand, 5)])
        overallMean = maxi
    values = [maxi, overallMean]
    return values


def should_call(players_num, percentile, pot, price):
    pWin = (percentile / 100) ** players_num
    ev = pWin * pot
    if ev <= 0:
        print('**** You should fold')
    if ev > 0:
        print('**** You should bet as long as your bet value is less than %s$' % int(ev))
        if ev > price:
            print('**** Expected bet value %s$ is lower than evaluated value by %s$ (you should raise)' %
                  (price, int(ev - price)))
        else:
            print('**** Expected bet value %s$ is higher than evaluated value by %s$ (you should call)' %
                  (price, int(price - ev)))
    return pWin * 100


def change_card_value(card):
    # change symbol pypokerengine card value to numerical card value only for faced cards,
    # and leave the rest of cards values unchanged as below
    # DJ -> D11, DQ -> D12, DK -> D13, DA, DT -> D14
    # SJ -> S11, SQ -> S12, SK -> S13, SA, ST -> S14
    # and so on...

    if card == "DT":
        numValueCard = "D10"
    elif card == "DJ":
        numValueCard = "D11"
    elif card == "DQ":
        numValueCard = "D12"
    elif card == "DK":
        numValueCard = "D13"
    elif card == "DA":
        numValueCard = "D14"

    elif card == "HT":
        numValueCard = "H10"
    elif card == "HJ":
        numValueCard = "H11"
    elif card == "HQ":
        numValueCard = "H12"
    elif card == "HK":
        numValueCard = "H13"
    elif card == "HA":
        numValueCard = "H14"

    elif card == "ST":
        numValueCard = "S10"
    elif card == "SJ":
        numValueCard = "S11"
    elif card == "SQ":
        numValueCard = "S12"
    elif card == "SK":
        numValueCard = "S13"
    elif card == "SA":
        numValueCard = "S14"

    elif card == "CT":
        numValueCard = "C10"
    elif card == "CJ":
        numValueCard = "C11"
    elif card == "CQ":
        numValueCard = "C12"
    elif card == "CK":
        numValueCard = "C13"
    elif card == "CA":
        numValueCard = "C14"

    else:
        numValueCard = card
    return numValueCard


def flop_combinations(flop_cards = []):
    global c3, c4
    c4 = combinations(flop_cards, 4)
    c3 = combinations(flop_cards, 3)


def turn_combinations(turn_cards = []):
    global c4
    c4 = np.array([sorted(i) for i in combinations(turn_cards, 4)])