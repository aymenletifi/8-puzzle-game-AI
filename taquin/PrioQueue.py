
from heapq import heappush, heappop

class PrioQueue: 
	def __init__(self): 
		self.queue = []
		self.map = {}

	def remove(self, data):
		if (data.uuid in self.map.keys()):
			self.map[data.uuid][2] = False
			del self.map[data.uuid]

	def exists(self, data):
		if (data.uuid in self.map.keys()):
			return True
		return False
  
	def push(self, prio, data): 
		entry = [prio, data, True]
		self.map[data.uuid] = entry
		heappush(self.queue, entry)

	def pop(self):
		while (self.queue):
			(_, data, is_viable) = heappop(self.queue)
			if (is_viable):
				del self.map[data.uuid]
				return data
		return
