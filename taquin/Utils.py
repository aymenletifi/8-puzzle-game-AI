import random
from Etat import Etat
from PrioQueue import PrioQueue

def h1(arr):
	cost = 0

	for i, item in enumerate(arr):
		if (i != item):
			cost += 1
	return cost


def h2(arr):
	cost = 0

	for i, item in enumerate(arr):
		correct_posx = item % 3
		correct_posy = item // 3
		posx = i % 3
		posy = i // 3
		cost += abs(posx - correct_posx) + abs(posy - correct_posy)
	return cost


def get_shuffled():
	arr = list(range(9))
	random.shuffle(arr)

	while (not solvable(arr)):
		random.shuffle(arr)
	return arr


def solvable(arr):
	inversions = 0
	for i in range(0, len(arr) - 1):
		for j in range(i + 1, len(arr)):
			if(arr[i] != 0 and arr[j] != 0 and arr[i] > arr[j]):
				inversions += 1

	return inversions % 2 == 0


def draw(arr):
	for i in range(3):
		for j in range(3):
			print(arr[i * 3 + j] if arr[i * 3 + j] != 0 else '-', end=' ')
		print()


def find(arr, etat):
	for i, item in enumerate(arr):
		if item == etat:
			return i
	return -1


def astar(start, goal):
	eclosed = PrioQueue()
	eopen = PrioQueue()
	eopen.push(0, start)
	iters = 0

	while (eopen):
		iters += 1
		ecurrent = eopen.pop()
		eclosed.push(0, ecurrent)

		if(ecurrent == goal):
			break
		suivants = ecurrent.get_etats_suivants()
		for item in suivants:
			if(eclosed.exists(item)):
				continue

			eopen.remove(item)
			eopen.push(item.f, item)

			item.parent = ecurrent

	if(ecurrent != goal):
		return
	result = []
	while(ecurrent.parent):
		result.insert(0, ecurrent)
		ecurrent = ecurrent.parent
	result.insert(0, ecurrent)
	return (iters, len(eopen.queue) + len(eclosed.queue), result)
