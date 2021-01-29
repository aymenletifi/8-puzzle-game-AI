class Etat:
	def __init__(self, array, calc_h, g = 0):
		self.array = array
		self.g = g
		self.h = calc_h(array)
		self.f = g + self.h
		self.parent = None
		self.calc_h = calc_h
		self.uuid = ''.join(map(str, array))
	def get_etats_suivants(self):
		results = []
		index = self.array.index(0)
		if(not(index in [0,1,2])):
			arr = self.array.copy()
			aux = arr[index]
			arr[index] = arr[index - 3]
			arr[index - 3] = aux
			etat = Etat(arr, self.calc_h, self.g + 1)
			results.append(etat)
		if(not(index in [6,7,8])):
			arr = self.array.copy()
			aux = arr[index]
			arr[index] = arr[index + 3]
			arr[index + 3] = aux
			etat = Etat(arr, self.calc_h, self.g + 1)
			results.append(etat)
		if(not(index in [0,3,6])):
			arr = self.array.copy()
			aux = arr[index]
			arr[index] = arr[index - 1]
			arr[index - 1] = aux
			etat = Etat(arr, self.calc_h, self.g + 1)
			results.append(etat)
		if(not(index in [2,5,8])):
			arr = self.array.copy()
			aux = arr[index]
			arr[index] = arr[index + 1]
			arr[index + 1] = aux
			etat = Etat(arr, self.calc_h, self.g + 1)
			results.append(etat)
		return results

	def __eq__(self, other):
		return self.array == other.array

	def __lt__(self, other):
		return False
