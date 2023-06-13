# -*- coding: utf-8 -*-
n = int(input())
cards = list(map(int, input().split()))
m = int(input())
targets = list(map(int, input().split()))

count_dict = {}
for card in cards:
    if card in count_dict:
        count_dict[card] += 1
    else:
        count_dict[card] = 1

result = []
for target in targets:
    if target in count_dict:
        result.append(count_dict[target])
    else:
        result.append(0)

print(' '.join(map(str, result)))