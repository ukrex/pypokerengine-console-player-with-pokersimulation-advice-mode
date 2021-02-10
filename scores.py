import numpy as np
import pandas as pd
import itertools


def build_deck():
    numbers = list(range(2, 15))
    suits = ['H', 'S', 'C', 'D']
    cardDeck = []
    for i in numbers:
        for s in suits:
            card = s + str(i)
            cardDeck.append(card)
    return cardDeck


def combinations(arr, n):
    arr = np.asarray(arr)
    t = np.dtype([('', arr.dtype)] * n)
    result = np.fromiter(itertools.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)


def check_four_of_a_kind(hand, letters, numbers, rnum, rlet):
    for i in numbers:
        if numbers.count(i) == 4:
            four = i
        elif numbers.count(i) == 1:
            card = i
    score = 105 + four + card / 100
    return score


def check_full_house(hand, letters, numbers, rnum, rlet):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    score = 90 + full + p / 100
    return score


def check_three_of_a_kind(hand, letters, numbers, rnum, rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else:
            cards.append(i)
    score = 45 + three + max(cards) + min(cards) / 1000
    return score


def check_two_pair(hand, letters, numbers, rnum, rlet):
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards, reverse=True)
    score = 30 + max(pairs) + min(pairs) / 100 + cards[0] / 1000
    return score


def check_pair(hand, letters, numbers, rnum, rlet):
    pair = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards, reverse=True)
    score = 15 + pair[0] + cards[0] / 100 + cards[1] / 1000 + cards[2] / 10000
    return score


def score_hand(hand):
    letters = [hand[i][:1] for i in range(5)]  # We get the suit for each card in the hand
    numbers = [int(hand[i][1:]) for i in range(5)]  # We get the number for each card in the hand
    rNum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rLet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers)  # The difference between the greater and smaller number in the hand
    handType = ''
    score = 0
    if 5 in rLet:
        if numbers == [14, 13, 12, 11, 10]:
            handType = 'royal_flush'
            score = 135
        # print('this hand is a %s:, with score: %s' % (handType,score))
        # I comment the prints so the script runs faster
        elif dif == 4 and max(rNum) == 1:
            handType = 'straight_flush'
            score = 120 + max(numbers)
            hand2 = ['H7', 'H7', 'H7', 'H7', 'H7']
        # print('this hand is a %s:, with score: %s' % (handType,score))
        elif 4 in rNum:
            handType = 'four of a kind'
            score = check_four_of_a_kind(hand, letters, numbers, rNum, rLet)
        # print('this hand is a %s:, with score: %s' % (handType,score))
        elif sorted(rNum) == [2, 2, 3, 3, 3]:
            handType = 'full house'
            score = check_full_house(hand, letters, numbers, rNum, rLet)
        # print('this hand is a %s:, with score: %s' % (handType,score))
        elif 3 in rNum:
            handType = 'three of a kind'
            score = check_three_of_a_kind(hand, letters, numbers, rNum, rLet)
        # print('this hand is a %s:, with score: %s' % (handType,score))
        elif rNum.count(2) == 4:
            handType = 'two pair'
            score = check_two_pair(hand, letters, numbers, rNum, rLet)
        # print('this hand is a %s:, with score: %s' % (handType,score))
        elif rNum.count(2) == 2:
            handType = 'pair'
            score = check_pair(hand, letters, numbers, rNum, rLet)
        # print('this hand is a %s:, with score: %s' % (handType,score))
        else:
            handType = 'flush'
            score = 75 + max(numbers) / 100
        # print('this hand is a %s:, with score: %s' % (handType,score))
    elif 4 in rNum:
        handType = 'four of a kind'
        score = check_four_of_a_kind(hand, letters, numbers, rNum, rLet)
    # print('this hand is a %s:, with score: %s' % (handType,score))
    elif sorted(rNum) == [2, 2, 3, 3, 3]:
        handType = 'full house'
        score = check_full_house(hand, letters, numbers, rNum, rLet)
    # print('this hand is a %s:, with score: %s' % (handType,score))
    elif 3 in rNum:
        handType = 'three of a kind'
        score = check_three_of_a_kind(hand, letters, numbers, rNum, rLet)
    # print('this hand is a %s:, with score: %s' % (handType,score))
    elif rNum.count(2) == 4:
        handType = 'two pair'
        score = check_two_pair(hand, letters, numbers, rNum, rLet)
    # print('this hand is a %s:, with score: %s' % (handType,score))
    elif rNum.count(2) == 2:
        handType = 'pair'
        score = check_pair(hand, letters, numbers, rNum, rLet)
    # print('this hand is a %s:, with score: %s' % (handType,score))
    elif dif == 4:
        handType = 'straight'
        score = 65 + max(numbers)
    # print('this hand is a %s:, with score: %s' % (handType,score))
    else:
        handType = 'high card'
        n = sorted(numbers, reverse=True)
        score = n[0] + n[1] / 100 + n[2] / 1000 + n[3] / 10000 + n[4] / 100000
    # print('this hand is a %s:, with score: %s' % (handType,score))

    return score


def hand_values(combine):
    # We iterate over all combinations scoring them
    scores = [{"hand": i, "value": score_hand(i)} for i in combine]
    # We sort hands by score
    scores = sorted(scores, key=lambda k: k['value'])
    return scores


deck = build_deck()  # We create our deck
comb = combinations(deck, 5)  # We create an array containing all possible 5 cards combinations
handValues = hand_values(comb)  # We score all combinations
x = [i.get("hand", "") for i in handValues]  # making a list of hands
y = [i.get("value", "") for i in handValues]  # making a list of values

data = {'hands': x, 'value': y}  # making a dictionary of hands and values
# print("First 10 hands :\n", [x for x in range(10)])
# print("First 10 values :\n", [y for y in range(10)])

df = pd.DataFrame(data)  # making a pandas dataframe with hands and values
